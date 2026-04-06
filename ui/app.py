import re
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

from config.settings import USE_MOCK

if USE_MOCK:
    from services.mock_entry_service import process_qr_scan, get_all_records, get_counts
else:
    from services.entry_service import process_qr_scan, get_all_records, get_counts


def parse_qr_input(raw_value: str) -> str:
    raw_value = raw_value.strip()
    if not raw_value:
        return ""

    if raw_value.upper().startswith("_KW"):
        match = re.match(r"^_KW(\d{6,20})", raw_value)
        if match:
            return match.group(1)

    digits = re.sub(r"\D", "", raw_value)
    return digits if digits else raw_value


def format_duration(start_date: str, start_time: str, end_date: str, end_time: str) -> str:
    if not (start_date and start_time and end_date and end_time):
        return ""

    try:
        start_dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M:%S")
        elapsed = end_dt - start_dt
        total_seconds = int(elapsed.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours:
            return f"{hours}시간 {minutes}분"
        return f"{minutes}분"
    except ValueError:
        return ""


class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("체육관 출입 관리")
        self.root.geometry("1120x640")
        self.root.resizable(False, False)

        self.create_widgets()
        self.refresh_records()
        self.update_summary()

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#0f4c81", height=80)
        header.pack(fill="x")

        tk.Label(
            header,
            text="체육관 출입관리 시스템",
            bg="#0f4c81",
            fg="white",
            font=("Malgun Gothic", 18, "bold")
        ).place(x=18, y=20)

        self.date_label = tk.Label(
            header,
            text=self._current_date_text(),
            bg="#0f4c81",
            fg="white",
            font=("Malgun Gothic", 11)
        )
        self.date_label.place(x=18, y=50)

        summary_frame = tk.Frame(header, bg="#0f4c81")
        summary_frame.place(x=760, y=18)

        self.current_count_label = tk.Label(
            summary_frame,
            text="현재이용자: 0명",
            bg="#0f4c81",
            fg="white",
            font=("Malgun Gothic", 12, "bold")
        )
        self.current_count_label.pack(anchor="e")

        self.today_count_label = tk.Label(
            summary_frame,
            text="오늘이용자: 0명",
            bg="#0f4c81",
            fg="white",
            font=("Malgun Gothic", 12, "bold")
        )
        self.today_count_label.pack(anchor="e", pady=(4, 0))

        control_frame = tk.LabelFrame(self.root, text="QR 입력", padx=12, pady=12, font=("Malgun Gothic", 11))
        control_frame.pack(fill="x", padx=14, pady=(12, 0))

        tk.Label(control_frame, text="QR 코드 또는 학번:", font=("Malgun Gothic", 11)).grid(row=0, column=0, sticky="w")
        self.student_id_entry = tk.Entry(control_frame, font=("Malgun Gothic", 11), width=36)
        self.student_id_entry.grid(row=0, column=1, padx=(8, 12), pady=2)

        scan_button = tk.Button(control_frame, text="입력", font=("Malgun Gothic", 11), width=12, command=self.on_scan)
        scan_button.grid(row=0, column=2, padx=(0, 8))

        query_button = tk.Button(control_frame, text="조회", font=("Malgun Gothic", 11), width=12, command=self.on_query)
        query_button.grid(row=0, column=3)

        self.status_label = tk.Label(self.root, text="", font=("Malgun Gothic", 11), fg="#1f3c88")
        self.status_label.pack(fill="x", padx=18, pady=(6, 0))

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=14, pady=10)

        columns = [
            "ID", "입실일자", "입실시간", "퇴실일자", "퇴실시간",
            "시간", "학번", "이름", "학과", "구분", "이용구분", "비고"
        ]

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Malgun Gothic", 10, "bold"))
        style.configure("Treeview", font=("Malgun Gothic", 10), rowheight=24)

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=96, anchor="center")

        self.tree.column("이름", width=120)
        self.tree.column("학과", width=105)
        self.tree.column("구분", width=90)
        self.tree.column("입실일자", width=100)
        self.tree.column("퇴실일자", width=100)
        self.tree.column("입실시간", width=95)
        self.tree.column("퇴실시간", width=95)
        self.tree.column("비고", width=140)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def _current_date_text(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %A")

    def on_scan(self):
        raw_value = self.student_id_entry.get()
        student_id = parse_qr_input(raw_value)
        if not student_id:
            messagebox.showwarning("입력 오류", "QR 코드 또는 학번을 입력하세요.")
            return

        try:
            result = process_qr_scan(student_id)
            action = "입실" if result == "in" else "퇴실"
            self.status_label.config(text=f"{student_id}님 {action}이 완료되었습니다.")
            self.student_id_entry.delete(0, tk.END)
            self.refresh_records()
            self.update_summary()
        except Exception as exc:
            messagebox.showerror("처리 오류", f"DB 처리 중 오류가 발생했습니다: {exc}")

    def on_query(self):
        self.refresh_records()
        self.update_summary()
        self.status_label.config(text="기록 조회가 완료되었습니다.")

    def update_summary(self):
        try:
            current, today_total = get_counts()
        except Exception:
            current, today_total = 0, 0

        self.current_count_label.config(text=f"현재이용자: {current}명")
        self.today_count_label.config(text=f"오늘이용자: {today_total}명")
        self.date_label.config(text=self._current_date_text())

    def refresh_records(self):
        try:
            records = get_all_records()
        except Exception:
            records = []

        for item in self.tree.get_children():
            self.tree.delete(item)

        for record in records:
            duration = format_duration(
                record.get("입실일자", ""),
                record.get("입실시간", ""),
                record.get("퇴실일자", ""),
                record.get("퇴실시간", "")
            )
            self.tree.insert("", "end", values=(
                record.get("ID", ""),
                record.get("입실일자", ""),
                record.get("입실시간", ""),
                record.get("퇴실일자", ""),
                record.get("퇴실시간", ""),
                duration,
                record.get("학번", ""),
                record.get("이름", ""),
                record.get("학과", ""),
                record.get("구분", ""),
                record.get("이용구분", ""),
                record.get("비고", ""),
            ))
