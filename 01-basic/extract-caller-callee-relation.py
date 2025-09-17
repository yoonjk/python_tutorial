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


if __name__ == "__main__":
    # 테스트 C 코드
    c_code = r"""
    static int helper(int x){
        if (x>0) return x-1;
        return x;
    }

    int add(int a, int b)
    {
        int c = helper(a);
        return c + b;
    }

    static inline void logData(struct Data* d){
        putchar('x');       // 제외: 접두어 'put'
        helper(d->id);      // 내부 정의 함수
        add(1,2);           // callee가 다시 caller가 되는 예
        mycall();           // 내부 정의 함수
    }

    void mycall(){
        helper(10);
        logData(0);
    }
    """

    functions = extract_functions(c_code)
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

    print("\n=== Called By (callee ← [callers]) ===")
    print(json.dumps(called_by, indent=2, ensure_ascii=False))
