def ensure_table(conn):
    cur = conn.cursor()
    tables = [row.table_name for row in cur.tables(tableType="TABLE")]

    if "출입기록" not in tables:
        cur.execute("""
            CREATE TABLE 출입기록 (
                ID AUTOINCREMENT PRIMARY KEY,
                학번 TEXT,
                이름 TEXT,
                학과 TEXT,
                구분 TEXT,
                입실일자 TEXT,
                입실시간 TEXT,
                퇴실일자 TEXT DEFAULT '',
                퇴실시간 TEXT DEFAULT '',
                이용구분 TEXT DEFAULT '',
                비고 TEXT DEFAULT ''
            )
        """)
        conn.commit()