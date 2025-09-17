import re

def extract_c_functions(c_source: str):
    """
    Extract function definitions and bodies from C source code.

    :param c_source: string, full C source code
    :return: list of dict { 'signature': ..., 'body': ... }
    """

    # 정규식: 함수 정의 부분 캡처
    func_pattern = re.compile(
        r"""
        (?P<signature>                           # 함수 시그니처 그룹
            \b(?:int|long|unsigned\s+int|unsigned\s+long|char|char\s*\*|struct\s+\w+|void)\b   # 반환 타입
            \s+                                   # 공백
            \w+                                   # 함수 이름
            \s*                                   # 공백 가능
            \(
                [^)]*                             # 파라미터 (괄호 안)
            \)
        )
        \s*                                       # 공백
        (?P<body>\{(?:[^{}]|\{[^{}]*\})*\})       # 중괄호 블록(body)
        """,
        re.VERBOSE | re.MULTILINE | re.DOTALL
    )

    results = []
    for match in func_pattern.finditer(c_source):
        signature = match.group("signature").strip()
        body = match.group("body").strip()
        results.append({
            "signature": signature,
            "body": body
        })
    return results


if __name__ == "__main__":
    # 테스트용 C 코드
    c_code = r"""
 /*
** =================================================================================================
**  �ý���  �� : spa (SCAN) 
**  ���α׷�ID : sample001
**  ���α׷��� : ���ð� ���� 
**  ���������� : ���ð� �������� ��ȸ/�Է�/���� 
** =================================================================================================
** << ���α׷� ���� ���� >> 
** ------------------------ 
**  �� �� ���� : ������ : ��     ��     ��     �� 
** -------------------------------------------------------------------------------------------------
**  YYYY-MM-DD :        : 
** =================================================================================================
*/

/* -------------------------------------------------------------------------------------------------
 *  (1) Header Define 
 * -------------------------------------------------------------------------------------------------
 */
#include    "afc_svc.h"            /* ������ �ý���    Framework OLTP Worker    Header File */
#include    "sample001.h"        /* sample001                                    Header File */

/* ����ϴ�BAM �� Header ���� --------------------------------------------------------------------*/


/* -------------------------------------------------------------------------------------------------
 *  (2) Macro Define 
 * -------------------------------------------------------------------------------------------------
 */
#ifndef SVCMAIN
#define SVCMAIN(A,B)
#endif

#define MAX_CNT_OUTREC1        30                /* ���񽺿��� ó���� outrec1    �ִ� �Է� �Ǽ�   */
/* -------------------------------------------------------------------------------------------------
 *  (3) Host Variable Define 
 * -------------------------------------------------------------------------------------------------
 */
/* !----------------- (Code Generator) Host Variable Define Copy&Paste -------------------------! */
EXEC SQL INCLUDE SQLCA;
EXEC SQL BEGIN DECLARE SECTION;

//static int       H_MAX_CNT                                           ; /* �ִ� ��ȸ �Ǽ� */

/* ---  inrec1         ---------------------------------------------------------------------------*/
static char           H_iprce_sect_code                           [   1 + 1]; /* ó�������ڵ� */
static char           H_irfrn_date                                [   8 + 1]; /* ��ȸ���� */
static char           H_ia_nxt_date                               [   8 + 1]; /* �������� */
static char           H_ia_nxt_sect_code                          [   1 + 1]; /* ���������ڵ� */

/* ---  inrec2         ---------------------------------------------------------------------------*/
static char           H_itrdg_date                                [   8 + 1]; /* �ŷ����� */
static char           H_ispt_ftrs_sect_code                       [   1 + 1]; /* �������������ڵ� */
static char           H_imrop_strt_time                           [   6 + 1]; /* �����۽ð� */
static char           H_iordr_end_time                            [   6 + 1]; /* �ֹ�����ð� */
static char           H_ictra_end_time                            [   6 + 1]; /* ü������ð� */


/* ---  outrec1        ---------------------------------------------------------------------------*/
static char           H_otrdg_date             [MAX_CNT_OUTREC1+1][   8 + 1]; /* �ŷ����� */
static char           H_ospt_ftrs_sect_code    [MAX_CNT_OUTREC1+1][   1 + 1]; /* �������������ڵ� */
static char           H_omrop_strt_time        [MAX_CNT_OUTREC1+1][   6 + 1]; /* �����۽ð� */
static char           H_oordr_end_time         [MAX_CNT_OUTREC1+1][   6 + 1]; /* �ֹ�����ð� */
static char           H_octra_end_time         [MAX_CNT_OUTREC1+1][   6 + 1]; /* ü������ð� */

/* ---  outrec2        ---------------------------------------------------------------------------*/
static char           H_oa_nxt_date                               [   8 + 1]; /* �������� */
static char           H_oa_nxt_sect_code                          [   1 + 1]; /* ���������ڵ� */

EXEC SQL END DECLARE SECTION;

/* -------------------------------------------------------------------------------------------------
 *  (4) Variable Define 
 * -------------------------------------------------------------------------------------------------
 */ 
static FAMMCA     *p_fammca;  /* ������ �ý���   ���� ���� ����ü                           */
static sample001_in_t   *p_in;      /* �Է� ���� ����ü ����                                      */
static sample001_out_t  *p_out;     /* ��� ���� ����ü ����                                      */
static int   req_count                  ;  /* ��ȸ ��û �Ǽ�                                     */
static char  dta_sect                   ;  /* ������ ���� ����                                   */
static char  md_sect            [   3+1];  /* ��������  ��ü���а��� ������ ����                 */
static char  lang_typ           [   1+1];  /* ��������  ����������� ������ ����                 */
static char  scrn_no            [   5+1];  /* ��������  ȭ���ȣ���� ������ ����                 */
static char  brnh_cd            [   5+1];  /* ��������  �μ��ڵ� ���� ������ ����                */
static char  acng_unit_cd       [   5+1];  /* ��������  ȸ������ڵ� ���� ������ ����            */
static char  prev_afte_rqst_sect[   1+1];  /* ����/ ���� �ڷ� ��û���� ���庯��                  */
static char  user_id            [  16+1];  /* ��������  �����ID����  ������ ����                */
static char  user_tp_addr       [  39+1];  /* �������� PC���� IP-ADDRESS����  ������ ����        */
static char  user_ip_addr_telno [  39+1];  /* �������� PEER   IP-ADDRESS����  ������ ����        */
static char  svc_id             [  15+1];  /* ��������  ���񽺸��� ������ ����                   */
static char  msg_gb                     ;  /* �޽�������( �볻��,��ܿ�)���� ������ ����         */
static char  SQLText            [10240+1] ;/* Dynamic-SQL���� ������ ����                         */
    
/* ����ϴ�BAM �� ����ü ���� --------------------------------------------------------------------*/

/* !----------------- (Code Generator) VARIABLE DEFINE SECTION Copy&Paste ----------------------! */
static sample001_inrec1          *p_inrec1           ;
static sample001_inrec2          *p_inrec2           ;
static int                      outrec1_count       ;
static sample001_outrec1         *p_outrec1          ;
static sample001_outrec2         *p_outrec2          ;

/* -------------------------------------------------------------------------------------------------
 *  (5) Function Proto Type Define 
 * -------------------------------------------------------------------------------------------------
 */
SVCMAIN(sample001,"���ð� ����");
static void sample001_main             (sample001_in_t *pIn, sample001_out_t *pOut);
static int  sample001_a000_initialize      (); /* ���� ������ �ʱ�ȭ �Ѵ�.                    */
static int  sample001_a500_input_check     (); /* INPUT DATA�� �����Ѵ�.                      */
static int  sample001_c000_event_process   (); /* ó�����к� �б�ó���Ѵ�.                    */
static int  sample001_c100_insert_process  (); /* INSERT Logic�� ó���Ѵ�.                    */
static int  sample001_c200_update_process  (); /* UPDATE Logic�� ó���Ѵ�.                    */
static int  sample001_c300_delete_process  (); /* DELETE Logic�� ó���Ѵ�.                    */
static int  sample001_c400_select_process  (); /* SELECT Logic�� ó���Ѵ�.                    */

static int  sample001_aa00_inrec1_init     ();
static int  sample001_aa01_inrec1_assign   ();
static int  sample001_aa02_inrec2_init     ();
static int  sample001_aa03_inrec2_assign   ();
static int  sample001_aa04_outrec1_init    ();
static int  sample001_aa05_outrec1_assign  ();
static int  sample001_aa06_outrec2_init    ();
static int  sample001_aa07_outrec2_assign  ();

static int  sample001_aa98_inrec2_dbglog   ();
static int  sample001_aa97_outrec1_dbglog  ();
/**************************************************************************************************/
/*                                                                                                */
/*                        M A I N       P R O G R A M     S T A R T                               */
/*                                                                                                */
/**************************************************************************************************/
/* -------------------------------------------------------------------------------------------------
 * Main.UI���� �ش� ���� ȣ���
 * -------------------------------------------------------------------------------------------------
**/
static void sample001_main(sample001_in_t *pIn, sample001_out_t *pOut)
{
    int           rc = 0     ;
    
    p_fammca = pBIZ;
    p_in     = pIn;
    p_out    = pOut; 

    
    /* ���� ���� �ʱ�ȭ */
    if ( (rc = sample001_a000_initialize()) != SUCC )
    {
        DLOG("(sample001)(A000) �ʱ�ȭ ERROR !!");
        AMM_RETURN(rc,'N');
    }

    /* ��������� INPUT DATA CHECK */
    if ( (rc = sample001_a500_input_check()) != SUCC )
    {
        DLOG("(sample001)(A500) INPUT DATA CHECK ERROR !!");
        AMM_RETURN(rc,'N');
    }
    
    /* �Է�ó�� */
    if( (rc = sample001_c000_event_process()) != SUCC )
    {
        DLOG("(sample001)(C000) PROCESS ERROR !!");
        AMM_RETURN(rc,'N');
    }
  
    AMM_RETURN(rc, 'Y');
}


/* -------------------------------------------------------------------------------------------------
 * �ʱ�ȭó��. ���� �������� �ʱ�ȭ �Ѵ�.
 * -------------------------------------------------------------------------------------------------
**/
static int sample001_a000_initialize()
{
    /*  ���������� ���� ����� ��ġ ����(SVC_START).  �ش� ��ũ�δ� �����Ұ� �մϴ�.              */
    SVC_START;

    /* �����ڵ带 "0000"�� �ʱ�ȭ */
    COPYS(p_fammca->rtrn_cd, "0000");

    /* ���� �ʱ�ȭ ����  */
    req_count = 0 ; /* ��ȸ ��û �Ǽ� �ʱ�ȭ */
    dta_sect = 'N'; /* ������ ���� ���� �ʱ�ȭ */

    ILOG("sample001_a000_initialize");
    ILOG("dta_sect : (%c)", dta_sect);
    
    /* !----------------- (Code Generator) VARIABLE INITIAL SECTION  Copy&Paste ----------------! */
    p_inrec1            = &p_in->inrec1         ;
    p_inrec2            = &p_in->inrec2         ;
    p_outrec1           =  p_out->outrec1       ;
    p_outrec2           = &p_out->outrec2       ;



    sample001_aa00_inrec1_init     ();
    sample001_aa01_inrec1_assign   ();

    
    /*   �������� ����� �ʿ��� ������ �����´�.------------------------------------------------- */
    afc_get_lang_typ(p_fammca, lang_typ)                      ;  /* �������                      */
    afc_get_scrn_no(p_fammca, scrn_no)                        ;  /* ȭ���ȣ                      */
    afc_get_brnh_cd(p_fammca, brnh_cd)                        ;  /* �μ��ڵ�                      */
    afc_get_acng_unit_cd(p_fammca, acng_unit_cd)              ;  /* ȸ������ڵ�                  */
    afc_get_prev_afte_rqst_sect(p_fammca, prev_afte_rqst_sect);  /* ����/���� �ڷ��û����        */

    /*   �ý��۰��� ����� �ʿ��� ������ �����´�.----------------------------------------------- */
    afc_get_md_sect(p_fammca, md_sect)                        ;  /* ��ü����                      */
    afc_get_user_id(p_fammca, user_id)                        ;  /* User-ID                       */
    afc_get_user_ip_addr(p_fammca, user_tp_addr)              ;  /* PC���� ip �ּ�                */
    afc_get_user_ip_addr_telno(p_fammca, user_ip_addr_telno)  ;  /* CLIENT( ����) IP �ּ�         */
    afc_get_svc_id(p_fammca, svc_id)                          ;  /* Service-ID                    */

    afc_get_msg_typ(p_fammca, &msg_gb);  /* ��ü������  üũ�Ͽ� �޽��������� �����Ѵ�.    */
      
      
    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * INPUT����. INPUT DATA�� �����Ѵ�.
 * -------------------------------------------------------------------------------------------------
**/
static int sample001_a500_input_check()
{
    /*  ���������� ���� ����� ��ġ ����(SVC_START).  �ش� ��ũ�δ� �����Ұ� �մϴ�.              */
    SVC_START;   
    
    /* �Էµ����Ϳ� ���� �����۾��� ���� */
    
    
    SVC_RETURN_SUCC;
}

/* -------------------------------------------------------------------------------------------------
 * ����ó��. �������μ������� ���� �ش�ó�� �Լ��� ȣ���մϴ�.
 * -------------------------------------------------------------------------------------------------
**/
static int sample001_c000_event_process()
{
    /*  ���������� ���� ����� ��ġ ����(SVC_START).  �ش� ��ũ�δ� �����Ұ� �մϴ�.              */
    SVC_START;
    
    /* �̺�Ʈ���п� ���� ó��. �̺�Ʈ�����ڵ�� INPUT ������ �����ؾ� �Ѵ� 
     *    ���� : (1)(I) ���
     *           (2)(U) ����
     *           (3)(D) ����
     *           (4)(S) ��ȸ
     */
    switch( p_inrec1->prce_sect_code )
    {
        case '1' :
                if( sample001_c100_insert_process() != SUCC )
                {
                    SVC_RETURN_FAIL; 
                }
                break;
        case '3' :
                if( sample001_c300_delete_process() != SUCC )
                {
                    SVC_RETURN_FAIL; 
                }
                break;
        case '4' :
                if( sample001_c400_select_process() != SUCC )
                {
                    SVC_RETURN_FAIL; 
                }
                break;
        default:
                SET_MSG(_ERR_BIZ, "3216", ""); /* ó�������� Ȯ���Ͻñ� �ٶ��ϴ�. */
                ELOG("ó�� ���а�(%d)�� �˼� �����ϴ�.", p_inrec1->prce_sect_code);
                
                SVC_RETURN_FAIL; 
    }

    SVC_RETURN_SUCC;
}


/* -------------------------------------------------------------------------------------------------
 * ���ó��. ���ó���� �����մϴ�. 
 * -------------------------------------------------------------------------------------------------
**/
static int sample001_c100_insert_process()
{
    /*  ���������� ���� ����� ��ġ ����(SVC_START).  �ش� ��ũ�δ� �����Ұ� �մϴ�.              */
    SVC_START; 

    sample001_aa02_inrec2_init();
    sample001_aa03_inrec2_assign();
    
    /* Data Insert. */
    EXEC SQL
    INSERT INTO SSP.SPAD_MROP_TIME_MNGN_DTLD
    (
         TRDG_DATE
        ,SFO_SECT_CODE
        ,MROP_STRT_TIME
        ,ORDR_END_TIME
        ,CTRA_END_TIME
        ,PCPR_ID
        ,PCPR_IP
        ,PRCE_CHNL_SECT_CODE
        ,PRCE_DATE_TIME
    )
    VALUES
    (
         :H_itrdg_date
        ,:H_ispt_ftrs_sect_code
        ,:H_imrop_strt_time
        ,:H_iordr_end_time
        ,:H_ictra_end_time
        ,:user_id
        ,:user_tp_addr
        ,:md_sect
        ,CURRENT_TIMESTAMP
    )
    ;
      
    /* Insert ����ó��. */
    switch(SQLCODE)
    {
        case  SQLOK          :  SET_MSG(_ERR_BIZ,  "0021", ""); /* ����� �Ϸ�Ǿ����ϴ�.*/
                                break;
        case  SQLDUP         :  DLOG(" SQL MESSAGE : (%s)", SQLMESG );  
                                SET_MSG(_ERR_BIZ,  "0020", ""); /* �̹� ��ϵǾ� �ֽ��ϴ�. */
                                break;
        default              :  ELOG(" SQL MESSAGE : (%s)", SQLMESG );
                                SET_MSG(_ERR_DB,  "0168", ""); /* DB �Է¿����Դϴ�. */
                                SVC_RETURN_FAIL;
    }
        
    SVC_RETURN_SUCC;
}


/* -------------------------------------------------------------------------------------------------
 * ����ó��. ����ó���� �����մϴ�. 
 * -------------------------------------------------------------------------------------------------
**/
static int sample001_c300_delete_process()
{
    /*  ���������� ���� ����� ��ġ ����(SVC_START).  �ش� ��ũ�δ� �����Ұ� �մϴ�.              */
    SVC_START; 

    sample001_aa02_inrec2_init();
    sample001_aa03_inrec2_assign();
    
    /* Data Delete. */
    EXEC SQL
    DELETE FROM SSP.SPAD_MROP_TIME_MNGN_DTLD
    WHERE TRDG_DATE = :H_itrdg_date
    /* AND SFO_SECT_CODE = :H_ispt_ftrs_sect_code */
    ;
    
    /* Delete ����ó��. */
    switch(SQLCODE)
    {
        case  SQLOK             :  SET_MSG(_ERR_BIZ,  "0023", ""); /* ������ �Ϸ�Ǿ����ϴ�.*/
                                   break;
        case  SQLNOTFOUND       :  DLOG(" SQL MESSAGE : (%s)", SQLMESG );
                                   SET_MSG(_ERR_BIZ,  "0134", ""); /* ������ ������ �����ϴ�. */
                                   break;
        default                 :  ELOG(" SQL MESSAGE : (%s)", SQLMESG );
                                   SET_MSG(_ERR_DB,  "0170", ""); /* DB Delete�����Դϴ�. */
                                   SVC_RETURN_FAIL;
    }
    
    SVC_RETURN_SUCC;
}


/* -------------------------------------------------------------------------------------------------
 * ��ȸó��. ��ȸó���� �����մϴ�. 
 * -------------------------------------------------------------------------------------------------
**/
static int sample001_c400_select_process()
{
    /*  ���������� ���� ����� ��ġ ����(SVC_START).  �ش� ��ũ�δ� �����Ұ� �մϴ�.              */
    SVC_START; 

    sample001_aa04_outrec1_init();
    sample001_aa06_outrec2_init();
    
    if( req_count == 0 || req_count > MAX_CNT_OUTREC1 )
    {
        req_count = MAX_CNT_OUTREC1;
    }


    EXEC SQL
    DECLARE CUR_sample001_01 CURSOR FOR
    SELECT
         TRDG_DATE                  /* �ŷ����� */
        ,SFO_SECT_CODE              /* �����Ļ������ڵ� */
        ,MROP_STRT_TIME             /* �� ���۽ð� */
        ,ORDR_END_TIME              /* �ֹ� ����ð� */
        ,CTRA_END_TIME              /* ü�� ����ð� */
    FROM SSP.SPAD_MROP_TIME_MNGN_DTLD /* ���ð� ��������_T */
    /* NEXT KEY */
    WHERE
    (    TRDG_DATE < :H_ia_nxt_date
     OR (TRDG_DATE = :H_ia_nxt_date AND SFO_SECT_CODE <= :H_ia_nxt_sect_code   ))
    ORDER BY 1 DESC, 2 DESC
    ;
    
    /* Ŀ���� OPEN �մϴ�. */
    EXEC SQL
    OPEN CUR_sample001_01;

    /* Ŀ�� OPEN ����ó��. */
    if (SQLCODE != SQLOK)
    {
        DLOG("");
        DLOG("***********************************************************************");
        DLOG("* CUR_sample001_01 Ŀ���� OPEN �� �� �����ϴ�.");
        DLOG("*---------------------------------------------------------------------*");
        DLOG("* SQLCODE (%d), SQLMESG (%s)",SQLCODE, SQLMESG);
        DLOG("***********************************************************************");
        DLOG("");
        SET_MSG(_ERR_DB,  "0174", ""); /* Ŀ��Open���� �Դϴ� */
        SVC_RETURN_FAIL;
    }

    /* Ŀ�� FETCH. */
    EXEC SQL
    FETCH CUR_sample001_01
    INTO
     :H_otrdg_date
    ,:H_ospt_ftrs_sect_code
    ,:H_omrop_strt_time
    ,:H_oordr_end_time
    ,:H_octra_end_time
    ;

    outrec1_count = SQLCNT;
    ILOG("SQLCNT = (%d)", SQLCNT);

    if ( SQLCODE != SQLNOTFOUND && outrec1_count == 0 )
    {
        ELOG("SQLCODE : (%d) SQL MESSAGE : (%s)", SQLCODE, SQLMESG );
        SET_MSG(_ERR_DB,  "0175", ""); /* Ŀ��Fetch�����Դϴ� */
        EXEC SQL CLOSE CUR_sample001_01;
        SVC_RETURN_FAIL;
    }

    /* Ŀ���� CLOSE �մϴ�. */
    EXEC SQL
    CLOSE CUR_sample001_01;

    /* Ŀ�� CLOSE ����ó��. */
    if (SQLCODE != SQLOK)
    {
        DLOG("***********************************************************************");
        DLOG("* UV_�޽��� (CSSF_MSG) TABLE SELECT ERROR !!!");
        DLOG("* SQLCODE (%d), SQLMESG (%s)",SQLCODE, SQLMESG);
        DLOG("***********************************************************************");
        SET_MSG(_ERR_DB,  "0176", ""); /* Ŀ��Close�����Դϴ� */
        SVC_RETURN_FAIL;
    }

    /* �׸��� ��ȸ��� assign */
    sample001_aa05_outrec1_assign();


    /* �����ڷ� ���� �޽���.*/
    if( dta_sect == 'Y' )     
    {
        SET_MSG(_ERR_BIZ,  "0002", "");                       /* ��ȸ�� ��ӵ˴ϴ�.      */
    }
    /* �ڷ������ �޽���. */
    else if( outrec1_count == 0 )
    {
        SET_MSG(_ERR_BIZ,  "0003", "");                       /* ��ȸ�� ����(�ڷ�)�� �����ϴ�.   */
    }
    /* �������� �޽���. */
    else
    {
        SET_MSG(_ERR_BIZ,  "0001", "");                       /* ��ȸ �Ϸ�Ǿ����ϴ�.    */
    }

    /* �ٰ���ȸ Next Key ����. */
    if( outrec1_count > 0 )
    {
        /* �ڷ����� �÷��� ����. �ٰ���ȸ�� ��� ����/���� �ڷ����� �÷��׸� �����Ѵ�.  --------- */
        /* -------------------------------------------------------------------------------------- */
        /*    �Ʒ��κ��� �ڷ����� �÷��� "����/�����ڷ����,�����ڷ�����"�� ����ϴ� ����̸�     */
        /*    �ڷ����� �÷��� "����/�����ڷ����,�����ڷ�����,�����ڷ�����,����/�����ڷ�����"��   */
        /*    ��� ����ؾ� �ϴ� ���� �Ʒ��κ��� �����ؾ� �մϴ�.                               */
        /*              RESP_DISABLE('0') - ����/���� �ڷ� ����                                   */
        /*              RESP_PREV   ('1') - �����ڷ�  ����                                        */
        /*              RESP_NEXT   ('2') - �����ڷ�  ����                                        */
        /*              RESP_ALL    ('3') - ����/���� ����                                        */
        /* -------------------------------------------------------------------------------------- */
        if( dta_sect == 'Y' ) /* ���� �ڷᰡ �ִ� ���   */
        {
            p_fammca->prev_afte_dta_sect = RESP_NEXT;
            
            /* next key �� ���� */
            COPYS(H_oa_nxt_date                       , H_otrdg_date[outrec1_count]);
            COPYS(H_oa_nxt_sect_code                  , H_ospt_ftrs_sect_code[outrec1_count]);
            sample001_aa07_outrec2_assign();
        }
    }

    SVC_RETURN_SUCC;
}
/* -------------------------------------------------------------------------------------------------
 * inrec1 �ʱ�ȭ. inrec1 �� HOST ������ �ʱ�ȭ �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa00_inrec1_init ()
{
    SVC_START;

    memset(H_iprce_sect_code            , NULL, sizeof(H_iprce_sect_code           ));
    memset(H_irfrn_date                 , NULL, sizeof(H_irfrn_date                ));
    memset(H_ia_nxt_date                , NULL, sizeof(H_ia_nxt_date               ));
    memset(H_ia_nxt_sect_code           , NULL, sizeof(H_ia_nxt_sect_code          ));

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * inrec1 HOST���� ����. inrec1 �� ���� �ش� HOST ������ ���� �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa01_inrec1_assign ()
{
    SVC_START;

    H_iprce_sect_code                   [0] = p_inrec1->prce_sect_code      ;
    COPYS(H_irfrn_date                      , p_inrec1->rfrn_date            );

    if ( afc_is_space(p_inrec1->a_nxt_date) == TRUE )
    {
        COPYS( p_inrec1->a_nxt_date , "99991231"  );
    }
    if ( afc_is_space(p_inrec1->a_nxt_sect_code) == TRUE )
    {
        COPYS( p_inrec1->a_nxt_sect_code , "0"  );
    }
    COPYS(H_ia_nxt_date                     , p_inrec1->a_nxt_date           );
    H_ia_nxt_sect_code                  [0] = p_inrec1->a_nxt_sect_code     ;

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * inrec2 �ʱ�ȭ. inrec2 �� HOST ������ �ʱ�ȭ �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa02_inrec2_init ()
{
    SVC_START;

    memset(H_itrdg_date                 , NULL, sizeof(H_itrdg_date                ));
    memset(H_ispt_ftrs_sect_code        , NULL, sizeof(H_ispt_ftrs_sect_code       ));
    memset(H_imrop_strt_time            , NULL, sizeof(H_imrop_strt_time           ));
    memset(H_iordr_end_time             , NULL, sizeof(H_iordr_end_time            ));
    memset(H_ictra_end_time             , NULL, sizeof(H_ictra_end_time            ));

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * inrec2 HOST���� ����. inrec2 �� ���� �ش� HOST ������ ���� �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa03_inrec2_assign ()
{
    SVC_START;

    COPYS(H_itrdg_date                      , p_inrec2->trdg_date            );
    H_ispt_ftrs_sect_code               [0] = p_inrec2->spt_ftrs_sect_code  ;
    COPYS(H_imrop_strt_time                 , p_inrec2->mrop_strt_time       );
    COPYS(H_iordr_end_time                  , p_inrec2->ordr_end_time        );
    COPYS(H_ictra_end_time                  , p_inrec2->ctra_end_time        );

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * outrec1 �ʱ�ȭ. outrec1 �� HOST ������ �ʱ�ȭ �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa04_outrec1_init ()
{
    SVC_START;

    int   i;

    for( i = 0; i < MAX_CNT_OUTREC1+1; i++ )
    {
        memset(H_otrdg_date             [i] , NULL, sizeof(H_otrdg_date             [i]));
        memset(H_ospt_ftrs_sect_code    [i] , NULL, sizeof(H_ospt_ftrs_sect_code    [i]));
        memset(H_omrop_strt_time        [i] , NULL, sizeof(H_omrop_strt_time        [i]));
        memset(H_oordr_end_time         [i] , NULL, sizeof(H_oordr_end_time         [i]));
        memset(H_octra_end_time         [i] , NULL, sizeof(H_octra_end_time         [i]));
    }

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * outrec1 �� ����.  outrec1 �� HOST������ ���� ����ü outrec1 �� ���� �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa05_outrec1_assign ()
{
    SVC_START;

    int   i;

    if( outrec1_count   > req_count       )
    {
        dta_sect        = 'Y';
        outrec1_count   = req_count ;
    }
    if( outrec1_count   > MAX_CNT_OUTREC1 )
    {
        dta_sect        = 'Y';
        outrec1_count   = req_count ;
    }
    p_out->outrec1_count = outrec1_count;

    for( i = 0; i < outrec1_count; i++ )
    {
        COPYS(p_outrec1[i].trdg_date                 , H_otrdg_date             [i] );
        p_outrec1[i].spt_ftrs_sect_code              = H_ospt_ftrs_sect_code    [i][0];
        COPYS(p_outrec1[i].mrop_strt_time            , H_omrop_strt_time        [i] );
        COPYS(p_outrec1[i].ordr_end_time             , H_oordr_end_time         [i] );
        COPYS(p_outrec1[i].ctra_end_time             , H_octra_end_time         [i] );
    }

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * outrec2 �ʱ�ȭ. outrec2 �� HOST ������ �ʱ�ȭ �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa06_outrec2_init ()
{
    SVC_START;

    memset(H_oa_nxt_date                , NULL, sizeof(H_oa_nxt_date               ));
    memset(H_oa_nxt_sect_code           , NULL, sizeof(H_oa_nxt_sect_code          ));

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * outrec2 �� ����.  outrec2 �� HOST������ ���� ����ü outrec2 �� ���� �Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa07_outrec2_assign ()
{
    SVC_START;

    COPYS(p_outrec2->a_nxt_date                  , H_oa_nxt_date                );
    p_outrec2->a_nxt_sect_code                   = H_oa_nxt_sect_code          [0];

    SVC_RETURN_VOID;
}
/* -------------------------------------------------------------------------------------------------
 * inrec2 DEBUGLOG. inrec2 �� ���� ����Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa98_inrec2_dbglog ()
{
    SVC_START;

    DLOG("p_inrec2->trdg_date                 = (%-30s)",    p_inrec2->trdg_date                );
    DLOG("p_inrec2->spt_ftrs_sect_code        = (%c)",    p_inrec2->spt_ftrs_sect_code       );
    DLOG("p_inrec2->mrop_strt_time            = (%-30s)",    p_inrec2->mrop_strt_time           );
    DLOG("p_inrec2->ordr_end_time             = (%-30s)",    p_inrec2->ordr_end_time            );
    DLOG("p_inrec2->ctra_end_time             = (%-30s)",    p_inrec2->ctra_end_time            );

    SVC_RETURN_VOID;
}

/* -------------------------------------------------------------------------------------------------
 * outrec1 DEBUGLOG. outrec1 �� ���� ����Ѵ�.
 * -------------------------------------------------------------------------------------------------
 **/
static int  sample001_aa97_outrec1_dbglog ()
{
    SVC_START;

    int   i;

    for( i = 0; i < p_out->outrec1_count ; i++ )
    {
        DLOG("---------------------------------------------------------------------------");
        DLOG("p_outrec1[%d].trdg_date                 = (%-30s)", i, p_outrec1[i].trdg_date                );
        DLOG("p_outrec1[%d].spt_ftrs_sect_code        = (%c)", i, p_outrec1[i].spt_ftrs_sect_code       );
        DLOG("p_outrec1[%d].mrop_strt_time            = (%-30s)", i, p_outrec1[i].mrop_strt_time           );
        DLOG("p_outrec1[%d].ordr_end_time             = (%-30s)", i, p_outrec1[i].ordr_end_time            );
        DLOG("p_outrec1[%d].ctra_end_time             = (%-30s)", i, p_outrec1[i].ctra_end_time            );
    }
    DLOG("---------------------------------------------------------------------------");

    SVC_RETURN_VOID;
}
/**************************************************************************************************/
/*                             E  N  D      O  F      P  R  O  G  R  A  M                         */
/**************************************************************************************************/

    """

    functions = extract_c_functions(c_code)
    for f in functions:
        print("=== Function Signature ===")
        print(f["signature"])
        print("=== Function Body ===")
        print(f["body"])
        print()
