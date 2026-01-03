# result_popup.py
import tkinter as tk
from base_popup import BasePopup

class LottoResultPopup(BasePopup):
    def __init__(self, root, numbers, on_save):
        self.numbers = numbers
        self.on_save = on_save
        # 부모 생성자 호출 (제목, 가로, 세로) -> 내부에서 _build_ui 실행됨
        super().__init__(root, "추출 결과", width=300, height=180)

    def _build_ui(self):
        """추상 메서드 구현: 결과 안내 및 버튼 배치"""
        tk.Label(self, text="[ 이번 주 추천 번호 ]", font=("Arial", 10, "bold")).pack(pady=10)
        
        # 당첨 번호 표시
        tk.Label(self, text=f"{self.numbers}", font=("Arial", 14), fg="red").pack(pady=10)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        
        # 저장 버튼: on_save 콜백 실행
        tk.Button(btn_frame, text="저장", width=10, 
                  command=self._handle_save).pack(side="left", padx=10)
        
        # 삭제 버튼: 저장 없이 창 닫기
        tk.Button(btn_frame, text="삭제", width=10, 
                  command=self.destroy).pack(side="right", padx=10)

    def _handle_save(self):
        """저장 로직 실행 후 팝업 소멸"""
        if self.on_save:
            self.on_save(self.numbers)
        self.destroy()