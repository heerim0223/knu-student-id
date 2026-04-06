from db.connection import connect_db
from db.schema import ensure_table
from config.settings import GYM_DB_PATH

from services.qr_service import parse_qr
from services.entry_service import process_qr_scan
from services.member_service import lookup_member

from utils.time_utils import calc_diff