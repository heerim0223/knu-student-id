import re
from datetime import datetime

QR_PATTERN = re.compile(
    r"^_KW(\d+?)(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\d+$"
)

def parse_qr(raw: str):
    m = QR_PATTERN.match(raw.strip())
    if not m:
        return None

    student_id = m.group(1)
    dt_str = f"{m.group(2)}-{m.group(3)}-{m.group(4)} {m.group(5)}:{m.group(6)}:{m.group(7)}"

    try:
        qr_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return student_id, qr_dt