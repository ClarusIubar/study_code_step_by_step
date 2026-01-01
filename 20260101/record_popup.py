import tkinter as tk

class RecordViewPopup(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("랜덤 5개 조회")
        
        # 위치 정합성 (부모 중앙 배치)
        self._align_to_center(parent)
        
        if not data:
            tk.Label(self, text="데이터 없음", font=("Arial", 11), pady=50).pack()
        else:
            for r in data:
                text = f"[{r['id']}] {r['nums']} ({r['time']})"
                tk.Label(self, text=text, font=("Consolas", 10), pady=5).pack()
        
        tk.Button(self, text="닫기", width=10, command=self.destroy).pack(pady=10)

    def _align_to_center(self, parent):
        self.update_idletasks()
        w, h = 350, 250
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")