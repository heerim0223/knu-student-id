from datetime import datetime
from services.member_service import lookup_member

def process_qr_scan(conn, student_id: str):
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
        # 퇴실
        cur.execute(
            "UPDATE 출입기록 SET 퇴실일자=?, 퇴실시간=? WHERE ID=?",
            (now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), row[0])
        )
        conn.commit()
        return "out"

    else:
        # 입실
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
        return "in"