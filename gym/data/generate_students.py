import random

last_names = ["김","이","박","최","정","강","조","윤","장","임"]
first_names = ["민준","서연","지훈","하은","도윤","지우","서준","유진","현우","지민"]

colleges = ["IT대학","공과대학","자연과학대학"]
departments = ["컴퓨터공학과","소프트웨어학과","전자공학과","기계공학과","수학과"]

data = []

for i in range(11, 50):
    student = {
        "id": i,
        "학번": f"2023{str(i).zfill(4)}",
        "이름": random.choice(last_names) + random.choice(first_names),
        "대학": random.choice(colleges),
        "학과": random.choice(departments)
    }
    data.append(student)

import json
print(json.dumps(data, ensure_ascii=False, indent=2))