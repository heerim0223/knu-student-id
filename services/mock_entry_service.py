from datetime import datetime

_mock_db = []

def process_qr_scan(student_id: str):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    for r in _mock_db:
        if r["학번"] == student_id and r["입실일자"] == today and not r["퇴실시간"]:
            r["퇴실일자"] = today
            r["퇴실시간"] = now.strftime("%H:%M:%S")
            return "out"

    _mock_db.append({
        "ID": len(_mock_db) + 1,
        "학번": student_id,
        "이름": "테스트",
        "학과": "컴공",
        "구분": "학생",
        "입실일자": today,
        "입실시간": now.strftime("%H:%M:%S"),
        "퇴실일자": "",
        "퇴실시간": "",
        "이용구분": "",
        "비고": ""
    })
    return "in"


def get_all_records():
    return list(reversed(_mock_db))


def get_counts():
    today = datetime.now().strftime("%Y-%m-%d")
    current = sum(1 for r in _mock_db if r["입실일자"] == today and not r["퇴실시간"])
    today_total = sum(1 for r in _mock_db if r["입실일자"] == today)
    return current, today_total
