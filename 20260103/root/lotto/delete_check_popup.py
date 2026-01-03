# delete_check_popup.py
import tkinter as tk
from common.base_popup import BasePopup

class DeleteCheckPopup(BasePopup):
    def __init__(self, root, record_id, on_confirm):
        self.record_id = record_id
        self.on_confirm = on_confirm
        super().__init__(root, "삭제 확인", width=280, height=130)

    def _build_ui(self):
        """추상 메서드 구현: 확인 문구 및 예/아니오 버튼"""
        msg = f"ID:{self.record_id} 기록을\n정말로 삭제하시겠습니까?"
        tk.Label(self, text=msg, font=("Arial", 10), pady=15).pack()
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        # '예' 버튼: 실제 삭제 수행
        tk.Button(btn_frame, text="예", width=10, bg="#ff7272", fg="white",
                  command=self._handle_confirm).pack(side="left", padx=10)
        
        # '아니오' 버튼: 취소
        tk.Button(btn_frame, text="아니오", width=10, 
                  command=self.destroy).pack(side="right", padx=10)

    def _handle_confirm(self):
        """승인 시 콜백 호출 후 소멸"""
        if self.on_confirm:
            self.on_confirm(self.record_id)
        self.destroy()