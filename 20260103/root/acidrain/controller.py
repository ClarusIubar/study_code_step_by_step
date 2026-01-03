import tkinter as tk

class AcidRainController(tk.Frame):
    def __init__(self, root, on_start, on_read):
        super().__init__(root, bg="#333", pady=10)
        
        # [정합성] 로또와 동일하게 Create(시작)와 Read(조회) 버튼 배치
        self.start_button = tk.Button(self, text="산성눈 방어 시작 (Start)", 
                                     command=on_start, width=20, height=2)
        self.start_button.pack(side="left", padx=20)
        
        self.read_button = tk.Button(self, text="랭킹 목록 조회 (Read)", 
                                    command=on_read, width=20, height=2)
        self.read_button.pack(side="right", padx=20)