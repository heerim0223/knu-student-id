import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rkddnjs55@",
    database="gym_db"        # 없으면 먼저 CREATE DATABASE gym_db; 실행
)
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    학번   VARCHAR(100) UNIQUE,
    이름   VARCHAR(100),
    대학   VARCHAR(100),
    학과   VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS access_log (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    학번     VARCHAR(100),
    이름     VARCHAR(100),
    학과     VARCHAR(100),
    구분     VARCHAR(50),
    입실일자 VARCHAR(10),
    입실시간 VARCHAR(8),
    퇴실일자 VARCHAR(10) DEFAULT '',
    퇴실시간 VARCHAR(8)  DEFAULT '',
    이용구분 VARCHAR(50) DEFAULT '',
    비고     VARCHAR(255) DEFAULT ''
)
""")