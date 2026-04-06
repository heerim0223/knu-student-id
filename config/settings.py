import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

GYM_DB_PATH = os.getenv("GYM_DB_PATH")
MEMBER_DB_PATH = os.getenv("MEMBER_DB_PATH")