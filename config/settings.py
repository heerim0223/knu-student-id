import os
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "True").strip().lower() in ("1", "true", "yes", "y")

GYM_DB_PATH = os.getenv("GYM_DB_PATH")
MEMBER_DB_PATH = os.getenv("MEMBER_DB_PATH")
