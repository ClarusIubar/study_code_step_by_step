import tkinter as tk
from common.base_popup import BasePopup
import common.config as cfg

class ScoreRecordPopup(BasePopup):
    def __init__(self, root, storage):
        self.storage = storage
        super().__init__(root, "최고 점수 기록", *cfg.PopupConfig.RECORD_SIZE)

    def _build_ui(self):
        self.render_list()

    def render_list(self):
        for widget in self.winfo_children(): widget.destroy()
        tk.Label(self, text="[ 산성비 랭킹 TOP 10 ]", font=("Arial", 12, "bold"), pady=10).pack()
        
        records = self.storage.read_all()
        if not records:
            tk.Label(self, text="기록이 없습니다.", pady=50, fg="gray").pack()
        else:
            # [수정] record 변수명 유지 및 i를 이용한 실제 순위 출력
            for i, record in enumerate(records[:10], 1):
                row = tk.Frame(self)
                row.pack(fill="x", padx=20, pady=2)
                # Rank 01, Rank 02... 처럼 숫자가 찍히도록 수리
                text = f"Rank {i:02d} | {record['score']}점 | {record['date']}"
                tk.Label(row, text=text, font=("Consolas", 10)).pack(side="left")

        tk.Button(self, text="닫기", width=10, command=self.destroy).pack(side="bottom", pady=15)