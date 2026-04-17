"""
services/qr_service_img.py
이미지 파일로 QR 인식 테스트
"""

from pyzbar.pyzbar import decode
import cv2
import re
import mysql.connector
from datetime import datetime

# DB 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rkddnjs55@",
    database="gym_db"
)
cursor = conn.cursor()


def process_scan(student_id):
    today    = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    # 1) students 조회
    cursor.execute("SELECT 이름 FROM students WHERE 학번 = %s", (student_id,))
    student = cursor.fetchone()

    if not student:
        print(f"[미등록] 학번: {student_id}")
        return

    name = student[0]

    # 2) 오늘 입실 중인 레코드 확인
    cursor.execute("""
        SELECT id FROM access_log
        WHERE 학번 = %s AND 입실일자 = %s AND 퇴실시간 = ''
        ORDER BY id DESC LIMIT 1
    """, (student_id, today))
    row = cursor.fetchone()

    if row:
        cursor.execute("""
            UPDATE access_log
            SET 퇴실일자 = %s, 퇴실시간 = %s, 구분 = '퇴실'
            WHERE id = %s
        """, (today, now_time, row[0]))
        conn.commit()
        print(f"[퇴실] {name} ({student_id}) | {now_time}")
    else:
        cursor.execute("""
            INSERT INTO access_log (학번, 이름, 구분, 입실일자, 입실시간)
            VALUES (%s, %s, '입실', %s, %s)
        """, (student_id, name, today, now_time))
        conn.commit()
        print(f"[입실] {name} ({student_id}) | {now_time}")

    # 3) 현재 인원
    cursor.execute("""
        SELECT COUNT(*) FROM access_log
        WHERE 입실일자 = %s AND 퇴실시간 = ''
    """, (today,))
    current_count = cursor.fetchone()[0]
    print(f"[현재 인원] {current_count}명")


# 이미지에서 QR 인식
IMG_PATH = "qrcode.png"   # 경로 확인

img = cv2.imread(IMG_PATH)

if img is None:
    print(f"[오류] 이미지를 찾을 수 없어요: {IMG_PATH}")
else:
    decoded = decode(img)

    if not decoded:
        print("[오류] QR 코드를 인식하지 못했어요 — 이미지가 흐리거나 여백이 부족할 수 있어요")
    else:
        for d in decoded:
            data  = d.data.decode()
            match = re.search(r'\d{8}', data)

            if match:
                student_id = match.group()
                print(f"[QR 인식] 학번: {student_id}")
                process_scan(student_id)
            else:
                print(f"[QR 인식] 학번 패턴 없음 — 데이터: {data}")

cursor.close()
conn.close()