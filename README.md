# 🏋️ Gym Check-in System

QR 코드를 이용한 체력단련실 출입 관리 시스템입니다.
Python (Tkinter) 기반 GUI와 MS Access 데이터베이스를 사용하여 출입 기록을 관리합니다.

---

## 📌 주요 기능

* QR 코드 스캔을 통한 자동 입/퇴실 처리
* 회원 정보 조회 (학번 기반)
* 현재 이용자 / 오늘 이용자 수 표시
* 이용 시간 자동 계산
* 수동 입실 등록 기능
* 실시간 출입 기록 테이블 조회 및 검색

---

## 🛠️ 기술 스택

* Python 3.x
* Tkinter (GUI)
* pyodbc (DB 연결)
* MS Access (.accdb)
* python-dotenv (.env 환경 변수 관리)

---

## 📁 프로젝트 구조

```
gym-checkin-system/
│
├─ config/        # 환경 설정 (.env)
├─ db/            # DB 연결 및 스키마
├─ services/      # 비즈니스 로직 (QR, 회원조회, 출입처리)
├─ ui/            # Tkinter UI
├─ utils/         # 유틸 함수
├─ logs/          # 로그 파일
│
├─ main.py        # 실행 파일
├─ .env.example   # 환경 변수 예시
└─ requirements.txt
```

---

## ⚙️ 실행 방법

### 1. 저장소 클론

```
git clone https://github.com/KangwonUNIV-GYMApp/gym-checkin-system.git
cd gym-checkin-system
```

### 2. 패키지 설치

```
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 생성 후 경로 설정

```
GYM_DB_PATH=경로\gym.accdb
MEMBER_DB_PATH=경로\members.accdb
```

### 4. 실행

```
python main.py
```

---

## 🧾 QR 코드 형식

```
_KW{학번}{YYYY}{MM}{DD}{HH}{mm}{SS}{XXX}
```

예:

```
_KW202313522026040619405716
```

---

## 📌 참고 사항

* MS Access 드라이버가 설치되어 있어야 합니다.
* DB 테이블이 없을 경우 자동 생성됩니다.
* `.env` 파일은 보안을 위해 Git에 포함되지 않습니다.

---