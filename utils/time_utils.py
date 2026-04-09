from datetime import datetime

def calc_diff(d1, t1, d2, t2):
    if not d2 or not t2:
        return "-"

    try:
        a = datetime.strptime(f"{d1} {t1}", "%Y-%m-%d %H:%M:%S")
        b = datetime.strptime(f"{d2} {t2}", "%Y-%m-%d %H:%M:%S")

        minutes = int((b - a).total_seconds() // 60)
        return f"{minutes//60}시간 {minutes%60}분"

    except:
        return "-"