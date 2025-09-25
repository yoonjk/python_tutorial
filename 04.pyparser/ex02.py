import re
import json
from collections import defaultdict

# ----------------------------
# 1) COBOL Paragraph / Section 추출
# ----------------------------
# COBOL에서 문단명: 보통 "XXXX-YYYY SECTION." 또는 "XXXX-YYYY." 형태
PARA_RE = re.compile(r'^\s*(?P<name>[A-Za-z0-9\-]+)\s+(SECTION\.)?', re.MULTILINE)

# ----------------------------
# 2) 호출 구문 추출 (PERFORM, CALL)
# ----------------------------
PERFORM_RE = re.compile(r'\bPERFORM\s+([A-Za-z0-9\-]+)', re.IGNORECASE)
CALL_RE = re.compile(r'\bCALL\s+["\']?([A-Za-z0-9\-]+)["\']?', re.IGNORECASE)

def extract_cobol_units(code: str):
    """COBOL 문단/섹션 목록 추출"""
    units = {}
    for m in PARA_RE.finditer(code):
        name = m.group("name")
        start = m.end()
        units[name] = {"start": start, "body": ""}
    # body 추출 (단순: 다음 파라그래프 시작 전까지)
    names = list(units.keys())
    for i, name in enumerate(names):
        start = units[name]["start"]
        end = len(code) if i == len(names)-1 else units[names[i+1]]["start"]
        units[name]["body"] = code[start:end]
    return units

def extract_cobol_call_graph(code: str):
    units = extract_cobol_units(code)
    edges = set()
    calls = defaultdict(set)
    called_by = defaultdict(set)

    for caller, info in units.items():
        body = info["body"]
        # PERFORM 호출
        for m in PERFORM_RE.finditer(body):
            callee = m.group(1)
            if callee in units:  # 소스 내부 문단만 인정
                edges.add((caller, callee))
                calls[caller].add(callee)
                called_by[callee].add(caller)
        # CALL 호출 (외부 프로그램 호출도 캡처 가능)
        for m in CALL_RE.finditer(body):
            callee = m.group(1)
            edges.add((caller, callee))
            calls[caller].add(callee)
            called_by[callee].add(caller)

    return sorted(edges), {k: sorted(v) for k,v in calls.items()}, {k: sorted(v) for k,v in called_by.items()}

# ----------------------------
# 3) Demo COBOL Source
# ----------------------------
if __name__ == "__main__":
    cobol_src = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CUSTOMER-MGMT.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CUSTOMER-FILE ASSIGN TO 'cust.dat'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  CUSTOMER-FILE.
       01  CUSTOMER-REC.
           05  CUST-ID        PIC 9(5).
           05  CUST-NAME      PIC X(30).
           05  CUST-BALANCE   PIC 9(7)V99.

       WORKING-STORAGE SECTION.
       01  WS-EOF            PIC X VALUE 'N'.
       01  WS-TOTAL          PIC 9(9)V99 VALUE 0.
       01  WS-COUNT          PIC 9(5) VALUE 0.
       01  WS-SQLCODE        PIC S9(9) COMP.

       EXEC SQL
           INCLUDE SQLCA
       END-EXEC.

       PROCEDURE DIVISION.
       MAIN-PARA.
           OPEN INPUT CUSTOMER-FILE
           PERFORM READ-CUSTOMERS UNTIL WS-EOF = 'Y'
           PERFORM CALC-AVERAGE
           CALL "EXT-REPORT" USING WS-TOTAL WS-COUNT
           CLOSE CUSTOMER-FILE
           STOP RUN.

       READ-CUSTOMERS.
           READ CUSTOMER-FILE
               AT END MOVE 'Y' TO WS-EOF
           END-READ
           IF WS-EOF NOT = 'Y'
              ADD 1 TO WS-COUNT
              ADD CUST-BALANCE TO WS-TOTAL
              PERFORM DB-UPDATE
           END-IF
           EXIT.

       CALC-AVERAGE.
           IF WS-COUNT > 0
               COMPUTE WS-TOTAL = WS-TOTAL / WS-COUNT
           ELSE
               MOVE 0 TO WS-TOTAL
           END-IF
           EXIT.

       DB-UPDATE.
           EXEC SQL
               UPDATE CUSTOMER_TABLE
                  SET BALANCE = :CUST-BALANCE
                WHERE ID = :CUST-ID
           END-EXEC
           IF SQLCODE NOT = 0
              DISPLAY "DB ERROR OCCURRED, SQLCODE=" SQLCODE
           END-IF
           EXIT.

       REPORT-PARA SECTION.
           EXEC SQL
               DECLARE CUSTCUR CURSOR FOR
                   SELECT ID, NAME, BALANCE
                     FROM CUSTOMER_TABLE
           END-EXEC
           EXEC SQL
               OPEN CUSTCUR
           END-EXEC
           PERFORM FETCH-LOOP
           EXEC SQL
               CLOSE CUSTCUR
           END-EXEC
           EXIT.

       FETCH-LOOP.
           EXEC SQL
               FETCH CUSTCUR INTO :CUST-ID, :CUST-NAME, :CUST-BALANCE
           END-EXEC
           IF SQLCODE = 0
              DISPLAY "CUSTOMER:" CUST-ID CUST-NAME CUST-BALANCE
              PERFORM FETCH-LOOP
           END-IF
           EXIT.

    """

    edges, calls, called_by = extract_cobol_call_graph(cobol_src)

    print("=== Edges (caller → callee) ===")
    for c, d in edges:
        print(f"{c} -> {d}")

    print("\n=== Calls (caller → [callees]) ===")
    print(json.dumps(calls, indent=2, ensure_ascii=False))

    print("\n=== Called By (callee ← [callers]) ===")
    print(json.dumps(called_by, indent=2, ensure_ascii=False))
