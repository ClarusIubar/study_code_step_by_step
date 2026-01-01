import tkinter as tk

class LottoResultPopup(tk.Toplevel):
    def __init__(self, root, numbers, on_save):
        super().__init__(root)
        # 1. 생성 즉시 화면에서 숨김 (번쩍거림 방지 핵심)
        self.withdraw() 
        
        self.title("Draw Result")
        self.numbers = numbers
        self.on_save = on_save

        # 2. 위치 계산 및 UI 구성 (이때 창은 여전히 숨겨진 상태)
        self._align_to_center(root)
        self._build_ui()

        # 3. 설정 완료 후 부모 위에 고정하고 화면에 표시
        self.transient(root)
        self.grab_set()
        self.deiconify() # 이제 완성된 상태로 '짠'하고 나타남

    def _align_to_center(self, root):
        # 윈도우 크기 확정 및 렌더링 갱신
        self.update_idletasks()
        w, h = 300, 180
        
        # winfo_rootx()를 통해 부모의 실제 화면 좌표 정밀 획득
        px, py = root.winfo_rootx(), root.winfo_rooty()
        pw, ph = root.winfo_width(), root.winfo_height()
        
        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)
        
        # 위치를 먼저 지정한 뒤 (이 시점에도 withdraw 상태라 안 보임)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        tk.Label(self, text="[ 당첨 번호 ]", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Label(self, text=f"{self.numbers}", font=("Arial", 14), fg="red").pack(pady=10)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="저장", width=10, command=self._handle_save).pack(side="left", padx=10)
        tk.Button(btn_frame, text="삭제", width=10, command=self.destroy).pack(side="right", padx=10)

    def _handle_save(self):
        if self.on_save:
            self.on_save(self.numbers)
        self.destroy()