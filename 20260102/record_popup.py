# record_popup.py
import tkinter as tk

class RecordViewPopup(tk.Toplevel):
    def __init__(self, root, data):
        super().__init__(root)
        self.title("전체 저장 기록 조회")
        
        # 위치 정합성 (부모 중앙 배치)
        self._align_to_center(root)
        
        # 상단 타이틀
        tk.Label(self, text="[ 로또 추출 이력 ]", font=("Arial", 12, "bold"), pady=10).pack()
        
        # 데이터 렌더링 영역 (스크롤이 없는 단순 버전이므로 Label로 순회)
        if not data:
            tk.Label(self, text="저장된 데이터가 없습니다.", font=("Arial", 11), pady=50, fg="gray").pack()
        else:
            for r in data:
                # [교정] storage.py의 키값(id, numbers, date)과 일치시킴
                text = f"ID:{r['id']:02d} | {r['numbers']} | {r['date']}"
                tk.Label(self, text=text, font=("Consolas", 9), pady=2).pack()
        
        tk.Button(self, text="닫기", width=10, command=self.destroy).pack(pady=15)

    def _align_to_center(self, root):
        self.update_idletasks()
        w, h = 450, 350 # 가로 길이를 데이터 출력에 맞춰 확장
        px, py = root.winfo_rootx(), root.winfo_rooty()
        pw, ph = root.winfo_width(), root.winfo_height()
        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")