import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000/api/update")

def send_json(event, student_id, name, current_count):
    payload = {
        "event": event,              # "entry" / "exit"
        "student_id": student_id,
        "name": name,
        "current_count": current_count,
        "timestamp": datetime.now().isoformat()
    }

    # 로컬 JSON 파일로도 저장
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # 서버 URL 정해지면 아래 주석 해제
    # try:
    #     requests.post(SERVER_URL, json=payload, timeout=3)
    # except Exception as e:
    #     print(f"[전송 실패] {e}")

    print(f"[JSON] {payload}")