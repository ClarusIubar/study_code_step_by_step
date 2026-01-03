# delete_check_popup.py
import tkinter as tk

class DeleteCheckPopup(tk.Toplevel):
    def __init__(self, root, record_id, on_confirm):
        super().__init__(root)
        self.withdraw() # 배치 전까지 숨김
        
        self.title("삭제 확인")
        self.record_id = record_id
        self.on_confirm = on_confirm # '예'를 눌렀을 때 실행할 함수
        
        self._align_to_center(root)
        self._build_ui()
        
        self.transient(root)
        self.grab_set()
        self.deiconify()

    def _align_to_center(self, root):
        self.update_idletasks()
        w, h = 280, 130
        px, py = root.winfo_rootx(), root.winfo_rooty()
        pw, ph = root.winfo_width(), root.winfo_height()
        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # 안내 문구
        msg = f"ID:{self.record_id} 기록을\n정말로 삭제하시겠습니까?"
        tk.Label(self, text=msg, font=("Arial", 10), pady=15).pack()
        
        # 버튼 영역
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        # '예' 버튼: 넘겨받은 삭제 로직 실행
        tk.Button(btn_frame, text="예", width=10, bg="#ff7272", fg="white",
                  command=self._handle_yes).pack(side="left", padx=10)
        
        # '아니오' 버튼: 그냥 닫기
        tk.Button(btn_frame, text="아니오", width=10, 
                  command=self.destroy).pack(side="right", padx=10)

    def _handle_yes(self):
        """삭제 승인 시 콜백 함수를 실행하고 팝업을 닫음"""
        if self.on_confirm:
            self.on_confirm(self.record_id)
        self.destroy()