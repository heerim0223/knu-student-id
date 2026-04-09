#!/usr/bin/env python3
"""
헬스장 출입 관리 시스템 메인 파일
"""

import tkinter as tk
from ui.app import GymApp
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import webbrowser
import atexit
import signal
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from services.json_service import get_is_open

print(f"DEBUG at start: get_is_open() = {get_is_open()}")

# Flask 앱 생성
app = Flask(__name__)
CORS(app)  # CORS 활성화

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        # API 서버 모드
        from services.json_service import get_counts

        @app.route('/api/status')
        def get_status():
            try:
                from services.json_service import get_counts
                current, today_total = get_counts()
                is_open = get_is_open()
                with open('debug.log', 'a') as f:
                    f.write(f"is_open = {is_open}\n")

                raw_count_text = f"{current}명" if is_open else "미운영 중 입니다."

                return jsonify({
                    "isOpen": is_open,
                    "currentPeople": current,
                    "rawCountText": raw_count_text
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        print("Starting API server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        # GUI 모드
        def main():
            root = tk.Tk()
            app = GymApp(root)
            root.mainloop()

        main()
