from db.connection import get_connection
from datetime import datetime

def process_qr_scan(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    try:
        # 1) students 조회
        cursor.execute("SELECT 이름, 학과 FROM students WHERE 학번 = %s", (student_id,))
        student = cursor.fetchone()

        if not student:
            raise ValueError(f"미등록 학번: {student_id}")

        name, department = student

        # 2) 오늘 입실 중인 레코드 확인
        cursor.execute("""
            SELECT id FROM access_log
            WHERE 학번 = %s AND 입실일자 = %s AND 퇴실시간 = ''
            ORDER BY id DESC LIMIT 1
        """, (student_id, today))
        row = cursor.fetchone()

        if row:
            # 퇴실
            cursor.execute("""
                UPDATE access_log
                SET 퇴실일자 = %s, 퇴실시간 = %s, 구분 = '퇴실'
                WHERE id = %s
            """, (today, now_time, row[0]))
            conn.commit()
            return "out"
        else:
            # 입실
            cursor.execute("""
                INSERT INTO access_log (학번, 이름, 학과, 구분, 입실일자, 입실시간)
                VALUES (%s, %s, %s, '입실', %s, %s)
            """, (student_id, name, department, today, now_time))
            conn.commit()
            return "in"
    finally:
        cursor.close()
        conn.close()

def get_all_records():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id as ID, 입실일자, 입실시간, 퇴실일자, 퇴실시간, 학번, 이름, 학과, 구분, 이용구분, 비고
            FROM access_log
            WHERE 퇴실시간 = ''
            ORDER BY 입실시간 ASC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_today_records():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        cursor.execute("""
            SELECT id as ID, 입실일자, 입실시간, 퇴실일자, 퇴실시간, 학번, 이름, 학과, 구분, 이용구분, 비고
            FROM access_log
            WHERE 입실일자 = %s
            ORDER BY 입실시간 ASC
        """, (today,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_counts():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        # 현재 인원
        cursor.execute("""
            SELECT COUNT(*) FROM access_log
            WHERE 입실일자 = %s AND 퇴실시간 = ''
        """, (today,))
        current = cursor.fetchone()[0]

        # 오늘 누적
        cursor.execute("""
            SELECT COUNT(DISTINCT 학번) FROM access_log
            WHERE 입실일자 = %s
        """, (today,))
        today_total = cursor.fetchone()[0]

        return current, today_total
    finally:
        cursor.close()
        conn.close()

def delete_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM access_log WHERE id = %s", (record_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()