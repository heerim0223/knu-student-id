import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
ACCESS_LOG_FILE = os.path.join(DATA_DIR, 'access_log.json')
STATUS_FILE = os.path.join(DATA_DIR, 'status.json')
GUI_LOCK_FILE = os.path.join(DATA_DIR, 'gui_running.lock')

def _load_students():
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def _save_students(data):
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _load_access_log():
    if os.path.exists(ACCESS_LOG_FILE):
        with open(ACCESS_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def _save_access_log(data):
    with open(ACCESS_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_qr_scan(student_id):
    students = _load_students()
    # Filter out non-student entries (like comments)
    students = [s for s in students if isinstance(s, dict) and '학번' in s]
    student = next((s for s in students if s['학번'] == student_id), None)
    if not student:
        raise ValueError(f"미등록 학번: {student_id}")

    name = student['이름']
    department = student['학과']

    access_log = _load_access_log()
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    # 오늘 입실 중인 레코드 확인
    active = next((r for r in access_log if r['학번'] == student_id and r['입실일자'] == today and r['퇴실시간'] == ''), None)

    if active:
        # 퇴실
        active['퇴실일자'] = today
        active['퇴실시간'] = now_time
        active['구분'] = '퇴실'
        _save_access_log(access_log)
        return "out"
    else:
        # 입실
        new_record = {
            "ID": len(access_log) + 1,
            "학번": student_id,
            "이름": name,
            "학과": department,
            "구분": "입실",
            "입실일자": today,
            "입실시간": now_time,
            "퇴실일자": "",
            "퇴실시간": "",
            "이용구분": "",
            "비고": ""
        }
        access_log.append(new_record)
        _save_access_log(access_log)
        return "in"

def get_all_records():
    access_log = _load_access_log()
    return [r for r in access_log if r['퇴실시간'] == '']

def get_today_records():
    access_log = _load_access_log()
    today = datetime.now().strftime("%Y-%m-%d")
    return [r for r in access_log if r['입실일자'] == today]

def get_counts():
    access_log = _load_access_log()
    today = datetime.now().strftime("%Y-%m-%d")
    current = sum(1 for r in access_log if r['입실일자'] == today and r['퇴실시간'] == '')
    today_total = len(set(r['학번'] for r in access_log if r['입실일자'] == today))
    return current, today_total

def delete_record(record_id):
    access_log = _load_access_log()
    access_log = [r for r in access_log if r.get('ID', r.get('id', '')) != record_id]
    _save_access_log(access_log)

def _load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"isOpen": False}

def _save_status(data):
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def set_is_open(is_open):
    status = _load_status()
    status['isOpen'] = is_open
    _save_status(status)

def get_is_open():
    return os.path.exists(GUI_LOCK_FILE)