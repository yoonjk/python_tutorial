import re
import json
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# ----------------------------
# 1) 전처리: 주석/문자열 제거
# ----------------------------
def strip_comments_and_strings(code: str) -> str:
    # 블록 주석 제거
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    # 라인 주석 제거
    code = re.sub(r"//.*?$", "", code, flags=re.MULTILINE)
    # 문자열/문자 리터럴 제거(괄호 매칭 방해 요소 완화)
    code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
    code = re.sub(r"'(?:\\.|[^'\\])*'", "''", code)
    return code

# ----------------------------
# 2) 함수 정의 시그니처 검출
#    - 수식어(static/inline/extern/...) 허용
#    - 반환형: int/long/unsigned int/unsigned long/char/char*/void/void*/struct X/struct X*
#    - 괄호/중괄호 매칭으로 본문 추출
# ----------------------------
SIG_RE = re.compile(r"""
    (?P<qualifiers>(?:\b(?:static|inline|extern|const|volatile|register)\b\s+)*)   # optional qualifiers
    (?P<ret>
        (?:unsigned\s+long\s+long|unsigned\s+long|unsigned\s+int|
           long\s+long|long|int|
           char\s*\*|char|
           void\s*\*|void|
           struct\s+\w+(?:\s*\*)?)
    )
    \s+
    (?P<name>[A-Za-z_]\w*)
    \s*
    \(
""", re.VERBOSE)

def _find_matching(code: str, start_idx: int, open_ch: str, close_ch: str) -> int | None:
    """start_idx 위치의 open_ch부터 매칭되는 close_ch 인덱스를 반환"""
    depth = 0
    i = start_idx
    n = len(code)
    while i < n:
        ch = code[i]
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i
        elif ch == '"':  # 문자열 건너뛰기
            i += 1
            while i < n and code[i] != '"':
                if code[i] == '\\': i += 1
                i += 1
        elif ch == "'":  # 문자 리터럴 건너뛰기
            i += 1
            while i < n and code[i] != "'":
                if code[i] == '\\': i += 1
                i += 1
        elif ch == '/' and i + 1 < n and code[i+1] == '*':  # 블록 주석 건너뛰기
            end = code.find('*/', i + 2)
            if end == -1: return None
            i = end + 1
        elif ch == '/' and i + 1 < n and code[i+1] == '/':  # 라인 주석 건너뛰기
            end = code.find('\n', i + 2)
            if end == -1: return n - 1
            i = end
        i += 1
    return None

def extract_functions(code: str) -> Dict[str, Dict[str, str]]:
    """
    반환: { func_name: {'signature': str, 'body': str} }
    """
    txt = strip_comments_and_strings(code)
    functions: Dict[str, Dict[str, str]] = {}

    for m in SIG_RE.finditer(txt):
        name = m.group("name")
        # 여는 괄호 '(' 위치
        p_open = m.end() - 1
        # 파라미터 닫는 괄호 ')'
        p_close = _find_matching(txt, p_open, '(', ')')
        if p_close is None:
            continue

        # ')' 다음의 '{' 확인
        j = p_close + 1
        while j < len(txt) and txt[j].isspace():
            j += 1
        if j >= len(txt) or txt[j] != '{':
            # 함수 정의가 아니라 프로토타입/매크로일 수 있음
            continue

        b_open = j
        b_close = _find_matching(txt, b_open, '{', '}')
        if b_close is None:
            continue

        signature = txt[m.start():p_close + 1].strip()
        body = txt[b_open:b_close + 1]
        functions[name] = {'signature': signature, 'body': body}

    return functions

# ----------------------------
# 3) 함수 호출 추출
# ----------------------------
CALL_RE = re.compile(r'\b([A-Za-z_]\w*)\s*\(')
RESERVED = {"if", "for", "while", "switch", "return", "sizeof"}

def extract_call_graph(
    functions: Dict[str, Dict[str, str]],
    exclude_prefixes: List[str] | None = None,
    only_defined_callees: bool = False,
    include_self_calls: bool = False,
):
    """
    호출 그래프 구성
    - exclude_prefixes: 제외할 callee 접두어 목록
    - only_defined_callees: True면, 소스 내 정의된 함수에 한해 callee로 인정
    - include_self_calls: 자기 자신 호출(A->A) 포함 여부
    반환:
      edges: List[Tuple[caller, callee]]
      calls: Dict[caller, Set[callee]]
      called_by: Dict[callee, Set[caller]]
    """
    if exclude_prefixes is None:
        exclude_prefixes = []

    defined = set(functions.keys())

    edges: Set[Tuple[str, str]] = set()
    calls: Dict[str, Set[str]] = defaultdict(set)
    called_by: Dict[str, Set[str]] = defaultdict(set)

    for caller, info in functions.items():
        body = info['body']
        for m in CALL_RE.finditer(body):
            callee = m.group(1)

            # 예약어/키워드 제외
            if callee in RESERVED:
                continue
            # 접두어 제외
            if any(callee.startswith(p) for p in exclude_prefixes):
                continue
            # 자기호출 제외 옵션
            if not include_self_calls and callee == caller:
                continue
            # 정의된 함수만 인정 옵션
            if only_defined_callees and callee not in defined:
                continue

            edges.add((caller, callee))
            calls[caller].add(callee)
            called_by[callee].add(caller)

    # 정렬된 결과 반환
    edges_sorted = sorted(edges)
    calls_sorted = {k: sorted(v) for k, v in calls.items()}
    called_by_sorted = {k: sorted(v) for k, v in called_by.items()}
    return edges_sorted, calls_sorted, called_by_sorted

# ----------------------------
# 4) 데모
# ----------------------------
if __name__ == "__main__":
    demo = r"""
/*********************************************************************************************************************************
 * 1. SERVICE ID    : AATSCTL00020T03
 * 2. SERVICE ����  : ���ý��� ���� �ŷ� ����
 * 3. �ۼ�����      : 2017/03/15 18:57:25
 * 4. �ۼ���        : aatdd057967                                                      
 * 5. ȣ���Լ���
 *    1) proframe   : ����                                                           
 *    2) tmax       : ����                                                          
 *    3) ����� ����: ����                                                          
 *
 *    history ������ ���� ���� �߰�                                                    
 *                                                                                     
 *    ����      : ����     : ����                : �ٰ� �ڷ�     : ���� ����                      
 *    ---------- ---------- --------------------- --------------- ----------------------------------------------------------------
 *    ����      : aatdd057967   : 2017/03/15 18:57:25 : new ���� ���� : ���α׷� spec ���� (��缭 �ۼ�)
 *    ver1.00   : aatdd057967   : 2017/03/15 18:57:25 : new ���� ���� : �ű� ����
 *                                                                                      
 * 6. Ư�� �� ���� ����                                                                 
 ********************************************************************************************************************************/

/* --------------------------------------- include files ---------------------------------------------------------------------- */
#include <pfmcom.h>
#include <pfmutil.h>
#include <pfmerr.h>
#include <pfmcbuf.h>
#include <pfmdbio.h>
#include <pfmioframe.h>

/* TODO: Add I/O header files here  */
#include <pio_aatsctl00020t03_in.h>                /* �Է� ����ü ���� */
#include <pio_aatsctl00020t03_ins_01.h>            /* �Է� ����ü�� sub ����ü�� ���� */

/* DBIO header file here */
#include <pdb_zaat_emcy_sys_except_tx_lst_d0001.h>        /* ���� ó���� DBIO ����ü 3.���� */

/* -------------------------------- constant, macro definitions --------------------------------------------------------------- */
#define INPUT    ((aatsctl00020t03_in_t *)XXXINPT_1)       /* �Է� ����ü ���� �� ��� Macro API INPUT ���� */
#define INPUT_1  ((aatsctl00020t03_ins_01_t *)INPUT->ins)  /* INPUT ����ü�� sub ����ü�� ����              */

/* ----------------------------------- structure definitions ------------------------------------------------------------------ */
struct aatsctl00020t03_ctx_s {
    long dummy;
    /* ��� data ���� */
};
typedef struct aatsctl00020t03_ctx_s aatsctl00020t03_ctx_t;

/* -------------------------------------- global variables -------------------------------------------------------------------- */
/* ------------------------------------ function prototypes ------------------------------------------------------------------- */
static long a000_init_proc                  (aatsctl00020t03_ctx_t *ctx);
static long b000_input_validation           (aatsctl00020t03_ctx_t *ctx);
static long c000_main_proc                  (aatsctl00020t03_ctx_t *ctx);
static long c100_delete_proc                (aatsctl00020t03_ctx_t *ctx, long ix);
static long z000_norm_exit_proc             (aatsctl00020t03_ctx_t *ctx);
static long z999_err_exit_proc              (aatsctl00020t03_ctx_t *ctx);

/* --------------------------------------- function body ---------------------------------------------------------------------- */
long
aatsctl00020t03(void *dummy)
{
    long            rc = RC_NRM;

    aatsctl00020t03_ctx_t    _ctx;
    aatsctl00020t03_ctx_t    *ctx = &_ctx;

    /* ���α׷� �ʱ�ȭ                               */
    PFM_TRY( a000_init_proc(ctx) );

    /* �Էµ����� ����                               */
    PFM_TRY( b000_input_validation(ctx) );

    /* ���α׷� ó��                                 */
    PFM_TRY( c000_main_proc(ctx) );

    /* ���α׷� ��������                             */
    PFM_TRY( z000_norm_exit_proc(ctx) );

    return RC_NRM;

PFM_CATCH:
    /* ���α׷� ���� ó�� */
    PFM_TRYNJ( z999_err_exit_proc(ctx) );
    return RC_ERR;
}
  
/*********************************************************************************************************************************
 *     FUNCTION ��        :  a000_init_proc                                                                                       
 *     FUNCTION ��� ���� :  ���� ���α׷� context ���� ����ü �ʱ�ȭ �� ��Ÿ �ʱ�ȭ ó��
 ********************************************************************************************************************************/
static long
a000_init_proc(aatsctl00020t03_ctx_t *ctx)
{
    /* context initialize */
    memset( ctx, 0x00, sizeof(aatsctl00020t03_ctx_t) );

    return RC_NRM;
}

/*********************************************************************************************************************************
 *     FUNCTION ��        :  b000_input_validation                                                                                
 *     FUNCTION ��� ���� :  �Էµ����� ����
 ********************************************************************************************************************************/
static long
b000_input_validation(aatsctl00020t03_ctx_t *ctx)
{
    long                ix = 0;

    /* NGM Header ���� ��� */
    PRINT_PFMNGMHDR_T( NGMHEADER );
    /* �Է� ����ü ���� ��� : sub ����ü�� ������ ���� ����Ÿ �Ǽ���ŭ ������ �ǹǷ� looping ó���ϸ� ��� ó����. */
    PRINT_AATSCTL00020T03_IN_T( INPUT );

    for( ix = 0; ix < INPUT->rec_cnt; ix++)
    {
        PRINT_AATSCTL00020T03_INS_01_T( &INPUT_1[ix] );
    }

    /* ó���� ������ ���� ���� Notify �޽����� ������ �����ϰ� ���� ó���Ѵ�. */
    if( INPUT->rec_cnt == 0 )
    {
    	PFM_MSGE(T_S, "ZNGME0009", "%T%s", "&INPUT", "ó���� ������");
        return RC_NRM;
    }
    
    for( ix = 0; ix < INPUT->rec_cnt; ix++ )
    {
		if ( mpfm_isspnull(INPUT_1[ix].tx_id) == RC_NRM )
		{
			PFM_ERRS("INPUT_1[%ld].tx_id mpfm_isspnull is RC_NRM", ix);
			PFM_MSGE(T_S, "ZNGMC1056", "%T%s", "&INPUT", "�ŷ� ID");
			return RC_ERR;
		}
    }

    return RC_NRM; 
}

/*********************************************************************************************************************************
 *     FUNCTION ��        :  c000_main_proc                                                                                       
 *     FUNCTION ��� ���� :  ���α׷� ó��
 ********************************************************************************************************************************/
static long
c000_main_proc(aatsctl00020t03_ctx_t *ctx)
{
    long rc = RC_NRM;
    long ix = 0;

    for( ix = 0; ix < INPUT->rec_cnt; ix++ )
    {
    	/* ���ý��� ���� �ŷ� ���� ó�� */
    	PFM_TRY(c100_delete_proc(ctx, ix));
    }

    return RC_NRM;
    
PFM_CATCH:
    return RC_ERR;
}


/*********************************************************************************************************************************
 *     FUNCTION ��        :  c100_delete_proc
 *     FUNCTION ��� ���� :  ���ý��� ���� �ŷ� ���� ó�� ���α׷�
 ********************************************************************************************************************************/
static long
c100_delete_proc(aatsctl00020t03_ctx_t *ctx, long ix)
{
    long                rc = RC_NRM;

    /* DBIO ����ü ���� ����  */
    zaat_emcy_sys_except_tx_lst_d0001_in_t     zaat_emcy_sys_except_tx_lst_d0001_in;

     /* DBIO input ����ü �ʱ�ȭ */
    memset(&zaat_emcy_sys_except_tx_lst_d0001_in, 0x00, sizeof(zaat_emcy_sys_except_tx_lst_d0001_in_t));

    /* INPUT �� ����Ÿ�� DBIO input ����ü�� setting */
    strncpy( zaat_emcy_sys_except_tx_lst_d0001_in.tx_id, mpfm_trim(INPUT_1[ix].tx_id  ), LEN_ZAAT_EMCY_SYS_EXCEPT_TX_LST_D0001_TX_ID_I );

    /* DBIO ��� ��ũ�θ� �̿��Ͽ� input ����ü data �� �α׿� ���       */
    PRINT_ZAAT_EMCY_SYS_EXCEPT_TX_LST_D0001_IN_T( &zaat_emcy_sys_except_tx_lst_d0001_in );

    /*  ���ߴ� �ŷ� ����ó�� (DBIO  ���� Delete ����) */
    rc = mpfmdbio("zaat_emcy_sys_except_tx_lst_d0001",&zaat_emcy_sys_except_tx_lst_d0001_in, NULL);

    if ( rc == RC_NFD )   /* data not found ������ ���� ��� */
    {
        PFM_ERRS("(%s) ���� ���� Not Found ���� �߻� : [%ld][%s]", zaat_emcy_sys_except_tx_lst_d0001_in.tx_id, mpfmdbio_errno(), mpfmdbio_errstr());
        // ZNGME0010	�ش� &ITEM �����ϴ�.
        PFM_MSGE( T_D, "ZNGME0010", "%T%s[%s]", "&ITEM", "�ŷ� ID", zaat_emcy_sys_except_tx_lst_d0001_in.tx_id );
        return RC_ERR;
    }
    else if ( rc != RC_NRM )   /* ���������� ������ ��찡 Ȯ���� DB ���� */
    {
    	PFM_ERRS("(%s) ���� ���� �� ���� �߻�: [%ld][%s]", zaat_emcy_sys_except_tx_lst_d0001_in.tx_id, mpfmdbio_errno(), mpfmdbio_errstr());
        // ZNGME0004    &ERROR ���� �߻��߽��ϴ�.
        PFM_MSGE( T_D, "ZNGME0004", "%T%s", "&ERROR", "���ý��� ���� �ŷ� ���� ��" );
        return RC_ERR;
    }

	return RC_NRM;
}

/*********************************************************************************************************************************
 *     FUNCTION ��        :  z000_norm_exit_proc                                                                                  
 *     FUNCTION ��� ���� :  ���α׷� ��������                                                                                    
 ********************************************************************************************************************************/
static long
z000_norm_exit_proc(aatsctl00020t03_ctx_t *ctx)
{
    /* ���� ó���� �޽��� ó�� Ȥ�� ��Ÿ ó�� ������ �ʿ��� ��� ���⼭ �����մϴ�. */
	PFM_MSGN( T_S, "ZNGMN0002", "%T%s", "&PROC", "���ý��� ���� �ŷ� ����" );  /*&PROC ���� ó���Ǿ����ϴ�.*/
    return RC_NRM;
}

/*********************************************************************************************************************************
 *     FUNCTION ��        :  z999_err_exit_proc                                                                                   
 *     FUNCTION ��� ���� :  ���α׷� ��������                                                                                    
 ********************************************************************************************************************************/
static long
z999_err_exit_proc(aatsctl00020t03_ctx_t *ctx)
{
    /* ���� ó���� �޽��� ó�� Ȥ�� ��Ÿ ó�� ������ �ʿ��� ��� ���⼭ �����մϴ�. */
    return RC_ERR;
}

    """

    functions = extract_functions(demo)
    edges, calls, called_by = extract_call_graph(
        functions,
        exclude_prefixes=["str", "mem", "f", "get", "put", "printf", "scanf"],  # 접두어 기반 제외
        only_defined_callees=True,   # 소스 내 정의된 함수만 callee로 인정
        include_self_calls=False     # 자기호출 제외
    )

    print("=== Edges (caller → callee) ===")
    for c, d in edges:
        print(f"{c} -> {d}")

    print("\n=== Calls (caller → [callees]) ===")
    print(json.dumps(calls, indent=2, ensure_ascii=False))

