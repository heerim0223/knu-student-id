from datetime import datetime

from config.settings import GYM_DB_PATH
from db.connection import connect_db
from db.schema import ensure_table
from services.member_service import lookup_member


def process_qr_scan(student_id: str):
    conn = connect_db(GYM_DB_PATH)
    ensure_table(conn)
    today = datetime.now().strftime("%Y-%m-%d")
    cur = conn.cursor()

    cur.execute(
        "SELECT ID FROM 출입기록 "
        "WHERE 학번 = ? AND 입실일자 = ? AND (퇴실시간 IS NULL OR 퇴실시간 = '')",
        (student_id, today)
    )

    row = cur.fetchone()
    now = datetime.now()

    if row:
        cur.execute(
            "UPDATE 출입기록 SET 퇴실일자=?, 퇴실시간=? WHERE ID=?",
            (now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), row[0])
        )
        conn.commit()
        conn.close()
        return "out"

    info = lookup_member(student_id)

    cur.execute(
        "INSERT INTO 출입기록 (학번,이름,학과,구분,입실일자,입실시간,퇴실일자,퇴실시간) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (
            info["학번"], info["이름"], info["학과"], info["구분"],
            now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), "", ""
        )
    )
    conn.commit()
    conn.close()
    return "in"


def get_all_records():
    conn = connect_db(GYM_DB_PATH)
    ensure_table(conn)
    cur = conn.cursor()

    cur.execute(
        "SELECT ID, 학번, 이름, 학과, 구분, 입실일자, 입실시간, 퇴실일자, 퇴실시간, 이용구분, 비고 "
        "FROM 출입기록 ORDER BY ID DESC"
    )

    records = [
        {
            "ID": row[0],
            "학번": row[1],
            "이름": row[2],
            "학과": row[3],
            "구분": row[4],
            "입실일자": row[5],
            "입실시간": row[6],
            "퇴실일자": row[7],
            "퇴실시간": row[8],
            "이용구분": row[9] or "",
            "비고": row[10] or ""
        }
        for row in cur.fetchall()
    ]

    conn.close()
    return records


def get_counts():
    conn = connect_db(GYM_DB_PATH)
    ensure_table(conn)
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    cur.execute(
        "SELECT COUNT(*) FROM 출입기록 "
        "WHERE 입실일자 = ? AND (퇴실시간 IS NULL OR 퇴실시간 = '')",
        (today,)
    )
    current = cur.fetchone()[0] or 0

    cur.execute(
        "SELECT COUNT(*) FROM 출입기록 WHERE 입실일자 = ?",
        (today,)
    )
    today_total = cur.fetchone()[0] or 0

    conn.close()
    return current, today_total
