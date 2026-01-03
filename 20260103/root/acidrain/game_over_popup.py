import tkinter as tk
from common.base_popup import BasePopup
import common.config as cfg

class GameOverPopup(BasePopup):
    def __init__(self, root, score, on_save):
        self.score = score
        self.on_save = on_save
        super().__init__(root, "게임 종료!", *cfg.PopupConfig.RESULT_SIZE)

    def _build_ui(self):
        tk.Label(self, text="GAME OVER", font=("Arial", 14, "bold"), fg="red").pack(pady=10)
        tk.Label(self, text=f"최종 점수: {self.score}", font=("Arial", 12)).pack(pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="점수 저장", width=10, 
                  command=self._handle_save).pack(side="left", padx=10)
        tk.Button(btn_frame, text="닫기", width=10, 
                  command=self.destroy).pack(side="right", padx=10)

    def _handle_save(self):
        if self.on_save: self.on_save(self.score)
        self.destroy()