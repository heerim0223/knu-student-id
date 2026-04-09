from db.connection import connect_db
from config.settings import MEMBER_DB_PATH

def lookup_member(student_id: str):
    default = {"학번": student_id, "이름": "", "학과": "", "구분": "학생"}

    try:
        conn = connect_db(MEMBER_DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "SELECT 이름, 학과, 구분 FROM 회원정보 WHERE 학번 = ?",
            (student_id,)
        )

        row = cur.fetchone()
        conn.close()

        if row:
            return {
                "학번": student_id,
                "이름": row[0],
                "학과": row[1],
                "구분": row[2]
            }

    except Exception as e:
        print(f"[회원조회 오류] {e}")

    return default