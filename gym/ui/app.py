import re
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image
from PIL import ImageTk
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.settings import USE_MOCK, USE_JSON

if USE_JSON:
    from services.json_service import process_qr_scan, get_all_records, get_counts, get_today_records, delete_record, set_is_open
    from services.json_service import GUI_LOCK_FILE
    import os
elif USE_MOCK:
    from services.mock_entry_service import process_qr_scan, get_all_records, get_counts, get_today_records, delete_record
else:
    from services.entry_service import process_qr_scan, get_all_records, get_counts, get_today_records, delete_record

from pyzbar.pyzbar import decode
import cv2


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


def format_duration(start_date, start_time, end_date, end_time) -> str:
    if not (start_date and start_time and end_date and end_time):
        return ""
    try:
        start_dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        end_dt   = datetime.strptime(f"{end_date} {end_time}",   "%Y-%m-%d %H:%M:%S")
        total    = int((end_dt - start_dt).total_seconds())
        h, m     = total // 3600, (total % 3600) // 60
        return f"{h}시간 {m}분" if h else f"{m}분"
    except ValueError:
        return ""


# 색상 팔레트 
BLUE_DARK   = "#0f4c81"
BLUE_MID    = "#1a6dbd"
BLUE_LIGHT  = "#e8f2fc"
WHITE       = "#ffffff"
TEXT_DARK   = "#1a1a2e"
TEXT_MUTED  = "#5a6a85"
GREEN       = "#1d7a4f"
GREEN_BG    = "#e6f4ed"
RED         = "#b03a2e"
RED_BG      = "#fdf0ee"
BORDER      = "#d0dce8"
ROW_ALT     = "#f4f8fd"
HEADER_FG   = "#ffffff"


class GymApp:
    def __init__(self, root):
        if USE_JSON:
            set_is_open(True)
            with open(GUI_LOCK_FILE, 'w') as f:
                f.write('')
        self.root = root
        self.root.title("체력단련실 출입 관리 시스템")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        self._build_header()
        self._build_input_panel()
        self._build_status_bar()
        self._build_table()

        self.refresh_records()
        self.update_summary()
        self._tick_clock()

    # 정렬 기능
    def sort_by_column(self, col):
        if not self.current_records:
            return
        key_funcs = {
            "입실일자": lambda r: r.get("입실일자", ""),
            "입실시간": lambda r: r.get("입실시간", ""),
            "퇴실일자": lambda r: r.get("퇴실일자", ""),
            "퇴실시간": lambda r: r.get("퇴실시간", ""),
            "이용시간": lambda r: self._duration_to_seconds(r),
            "학번": lambda r: int(r.get("학번", "0") or "0"),
            "이름": lambda r: r.get("이름", ""),
            "학과": lambda r: r.get("학과", ""),
            "구분": lambda r: r.get("구분", ""),
        }
        if col in key_funcs:
            reverse = getattr(self, f'_sort_{col}_reverse', False)
            self.current_records.sort(key=key_funcs[col], reverse=reverse)
            setattr(self, f'_sort_{col}_reverse', not reverse)
            self._refresh_tree()

    def _duration_to_seconds(self, r):
        start_date = r.get("입실일자", "")
        start_time = r.get("입실시간", "")
        end_date = r.get("퇴실일자", "")
        end_time = r.get("퇴실시간", "")
        if not (start_date and start_time):
            return 0
        try:
            start_dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
            if end_date and end_time:
                end_dt = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M:%S")
                return (end_dt - start_dt).total_seconds()
            else:
                return (datetime.now() - start_dt).total_seconds()
        except:
            return 0

    def _refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, r in enumerate(self.current_records):
            duration = format_duration(
                r.get("입실일자", ""), r.get("입실시간", ""),
                r.get("퇴실일자", ""), r.get("퇴실시간", "")
            )
            tags = []
            if i % 2 == 1:
                tags.append("alt")
            if r.get("구분") == "입실":
                tags.append("entry")
            elif r.get("구분") == "퇴실":
                tags.append("exit")
            display_id = i + 1
            real_id = r.get('ID', r.get('id', ''))
            tags.append(f"id_{real_id}")
            values = (
                display_id,
                r.get("입실일자", ""), r.get("입실시간", ""),
                r.get("퇴실일자", ""), r.get("퇴실시간", ""),
                duration,
                r.get("학번", ""),  r.get("이름", ""),
                r.get("학과", ""),  r.get("구분", ""),
                r.get("이용구분", ""), r.get("비고", ""),
            )
            if self.current_mode == 'today':
                values += ("X",)
            self.tree.insert("", "end", tags=tags, values=values)

    # 헤더
    def _build_header(self):
        hf = tk.Frame(self.root, bg=BLUE_DARK, height=100)
        hf.pack(fill="x")
        hf.pack_propagate(False)

        left = tk.Frame(hf, bg=BLUE_DARK)
        left.pack(side="left", padx=20, pady=12)

        img_path = os.path.join(os.path.dirname(__file__), "knu.png")
        try:
            pil_img = Image.open(img_path).resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(pil_img)
            image = self.logo_img
        except:
            image = None

        tk.Label(left, text="  체력단련실 출입관리 시스템",
                 image=image, compound="left", bg=BLUE_DARK, fg=WHITE,
                 font=("Malgun Gothic", 17, "bold")).pack(anchor="w")

        self.date_label = tk.Label(left, text="",
                                   bg=BLUE_DARK, fg="#b0ccee",
                                   font=("Malgun Gothic", 10))
        self.date_label.pack(anchor="w", pady=(2, 0))

        right = tk.Frame(hf, bg=BLUE_DARK)
        right.pack(side="right", padx=24, pady=12)

        # 현재 인원 카드
        self.card_current = self._badge_card(right, "현재 이용자", "0명", BLUE_LIGHT, BLUE_DARK)
        self.card_current.pack(side="right", padx=(10, 0))

        # 오늘 누적 카드
        self.card_today = self._badge_card(right, "오늘 누적", "0명", GREEN_BG, GREEN)
        self.card_today.pack(side="right")

    def _badge_card(self, parent, label_text, value_text, bg, fg):
        frame = tk.Frame(parent, bg=bg, padx=14, pady=6,
                         relief="flat", bd=0)
        tk.Label(frame, text=label_text, bg=bg, fg=TEXT_MUTED,
                 font=("Malgun Gothic", 9)).pack()
        val = tk.Label(frame, text=value_text, bg=bg, fg=fg,
                       font=("Malgun Gothic", 15, "bold"))
        val.pack()
        frame._value_label = val
        return frame

    # 입력 패널
    def _build_input_panel(self):
        pf = tk.Frame(self.root, bg=WHITE, pady=12,
                      relief="flat", bd=0,
                      highlightbackground=BORDER, highlightthickness=1)
        pf.pack(fill="x", padx=16, pady=(12, 0))

        tk.Label(pf, text="QR 코드 / 학번 입력",
                 bg=WHITE, fg=TEXT_MUTED,
                 font=("Malgun Gothic", 9, "bold")).pack(anchor="w", padx=16)

        row = tk.Frame(pf, bg=WHITE)
        row.pack(fill="x", padx=16, pady=(4, 8))

        self.entry = tk.Entry(row, font=("Malgun Gothic", 12),
                              width=34, relief="solid", bd=1,
                              highlightthickness=2,
                              highlightcolor=BLUE_MID,
                              highlightbackground=BORDER)
        self.entry.pack(side="left", ipady=4)
        self.entry.bind("<Return>", lambda e: self.on_scan())

        tk.Button(row, text="입  력", font=("Malgun Gothic", 11),
                  bg=BLUE_DARK, fg=WHITE, activebackground=BLUE_MID,
                  activeforeground=WHITE, relief="flat", bd=0,
                  padx=18, pady=4, cursor="hand2",
                  command=self.on_scan).pack(side="left", padx=(10, 6))

        tk.Button(row, text="이미지 QR 인식", font=("Malgun Gothic", 11),
                  bg=BLUE_DARK, fg=WHITE, activebackground=BLUE_MID,
                  activeforeground=WHITE, relief="flat", bd=0,
                  padx=18, pady=4, cursor="hand2",
                  command=self.on_image_scan).pack(side="left", padx=(10, 6))

        tk.Button(row, text="오늘 로그 보기", font=("Malgun Gothic", 11),
                  bg=BLUE_DARK, fg=WHITE, activebackground=BLUE_MID,
                  activeforeground=WHITE, relief="flat", bd=0,
                  padx=18, pady=4, cursor="hand2",
                  command=self.on_show_today_logs).pack(side="left", padx=(10, 6))

        tk.Button(row, text="조  회", font=("Malgun Gothic", 11),
                  bg=WHITE, fg=BLUE_DARK, activebackground=BLUE_LIGHT,
                  relief="solid", bd=1, padx=18, pady=4, cursor="hand2",
                  command=self.on_query).pack(side="left")

    # 상태 바 
    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="")
        sf = tk.Frame(self.root, bg="#f0f4f8")
        sf.pack(fill="x", padx=16, pady=(6, 2))
        self.status_label = tk.Label(sf, textvariable=self.status_var,
                                     bg="#f0f4f8", fg=GREEN,
                                     font=("Malgun Gothic", 10, "bold"),
                                     anchor="w")
        self.status_label.pack(fill="x")

    # 테이블
    def _build_table(self):
        tf = tk.Frame(self.root, bg="#f0f4f8")
        tf.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview.Heading",
                        background=BLUE_DARK, foreground=WHITE,
                        font=("Malgun Gothic", 10, "bold"),
                        relief="flat")
        style.map("Custom.Treeview.Heading", background=[("active", BLUE_MID)])
        style.configure("Custom.Treeview",
                        font=("Malgun Gothic", 10),
                        rowheight=26,
                        fieldbackground=WHITE,
                        background=WHITE,
                        foreground=TEXT_DARK,
                        borderwidth=0)
        style.map("Custom.Treeview",
                  background=[("selected", BLUE_LIGHT)],
                  foreground=[("selected", BLUE_DARK)])

        columns = ["ID", "입실일자", "입실시간", "퇴실일자", "퇴실시간",
                   "이용시간", "학번", "이름", "학과", "구분", "이용구분", "비고", "삭제"]

        self.tree = ttk.Treeview(tf, columns=columns, show="headings",
                                 height=20, style="Custom.Treeview")

        col_widths = {
            "ID": 48, "입실일자": 100, "입실시간": 90, "퇴실일자": 100,
            "퇴실시간": 90, "이용시간": 80, "학번": 100, "이름": 110,
            "학과": 120, "구분": 72, "이용구분": 80, "비고": 120, "삭제": 50,
        }
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=col_widths.get(col, 90), anchor="center")

        self.tree.tag_configure("alt",    background=ROW_ALT)
        self.tree.tag_configure("entry",  foreground=GREEN)
        self.tree.tag_configure("exit",   foreground=RED)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        vsb = ttk.Scrollbar(tf, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tf, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    # 이벤트 핸들러
    def on_scan(self):
        raw = self.entry.get()
        sid = parse_qr_input(raw)
        if not sid:
            messagebox.showwarning("입력 오류", "QR 코드 또는 학번을 입력하세요.")
            return
        try:
            result = process_qr_scan(sid)
            action = "입실" if result == "in" else "퇴실"
            color  = GREEN if result == "in" else RED
            self.status_label.config(fg=color)
            self.status_var.set(f"✔  {sid}  {action} 처리 완료  —  {datetime.now().strftime('%H:%M:%S')}")
            self.entry.delete(0, tk.END)
            self.refresh_records()
            self.update_summary()
        except Exception as exc:
            messagebox.showerror("처리 오류", f"DB 처리 중 오류:\n{exc}")

    def on_image_scan(self):
        file_path = filedialog.askopenfilename(
            title="QR 코드 이미지 선택",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not file_path:
            return
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("오류", "이미지를 읽을 수 없습니다.")
            return
        decoded = decode(img)
        if not decoded:
            messagebox.showwarning("QR 인식 실패", "QR 코드를 찾을 수 없습니다.")
            return
        for d in decoded:
            data = d.data.decode()
            match = re.search(r'\d{8}', data)
            if match:
                student_id = match.group()
                try:
                    result = process_qr_scan(student_id)
                    action = "입실" if result == "in" else "퇴실"
                    color = GREEN if result == "in" else RED
                    self.status_label.config(fg=color)
                    self.status_var.set(f"✔  {student_id}  {action} 처리 완료 (이미지)  —  {datetime.now().strftime('%H:%M:%S')}")
                    self.refresh_records()
                    self.update_summary()
                except Exception as exc:
                    messagebox.showerror("처리 오류", f"DB 처리 중 오류:\n{exc}")
            else:
                messagebox.showwarning("학번 인식 실패", f"QR 데이터에서 학번을 찾을 수 없습니다: {data}")
    def on_show_today_logs(self):
        try:
            records = get_today_records()
        except Exception:
            records = []

        self.current_records = records
        self.current_mode = 'today'
        self._refresh_tree()

        self.status_label.config(fg=TEXT_MUTED)
        self.status_var.set(f"오늘 로그 조회 완료  —  {datetime.now().strftime('%H:%M:%S')}")

    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#13":  # 삭제 컬럼 (1-based, #1 is ID, #13 is 삭제)
                item = self.tree.identify_row(event.y)
                if item:
                    tags = self.tree.item(item, "tags")
                    real_id = None
                    for tag in tags:
                        if tag.startswith("id_"):
                            real_id = int(tag[3:])
                            break
                    if real_id and messagebox.askyesno("삭제 확인", "이 기록을 삭제하시겠습니까?"):
                        try:
                            delete_record(real_id)
                            self.on_show_today_logs()  # 다시 로드
                            self.status_var.set(f"기록 삭제 완료  —  {datetime.now().strftime('%H:%M:%S')}")
                        except Exception as exc:
                            messagebox.showerror("삭제 오류", f"삭제 중 오류:\n{exc}")

    def on_query(self):
        self.refresh_records()
        self.update_summary()
        self.status_label.config(fg=TEXT_MUTED)
        self.status_var.set(f"조회 완료  —  {datetime.now().strftime('%H:%M:%S')}")

    # 데이터 갱신
    def update_summary(self):
        try:
            current, today_total = get_counts()
        except Exception:
            current, today_total = 0, 0
        self.card_current._value_label.config(text=f"{current}명")
        self.card_today._value_label.config(text=f"{today_total}명")

    def refresh_records(self):
        try:
            records = get_all_records()
        except Exception:
            records = []

        self.current_records = records
        self.current_mode = 'current'
        self._refresh_tree()

    # 시계 자동 갱신 
    def _tick_clock(self):
        self.date_label.config(
            text=datetime.now().strftime("%Y년 %m월 %d일  %A  %H:%M:%S")
        )
        self.root.after(1000, self._tick_clock)

    def on_closing(self):
        if USE_JSON:
            set_is_open(False)
            if os.path.exists(GUI_LOCK_FILE):
                os.remove(GUI_LOCK_FILE)
        self.root.destroy()


# 진입점 
if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()