
# controller.py
import tkinter as tk

class Controller(tk.Frame):
    def __init__(self, root, on_draw, on_read): # 필요한 액션(on_draw)만 주입받음 # 트리거
        super().__init__(root, bg="#333", pady=10) # root를 상속받아야 함. 버튼은 tk모듈에 종속적
        
        self.draw_button = tk.Button(self, text="6/45 공 투입 (Create)", # 액션에 따라 버튼을 동작.
                                    command=on_draw, width=20, height=2).pack(side="left", padx=20) 
                                    # chaining pack to assign left
        
        
        self.read_button = tk.Button(self, text="저장 목록 조회 (Read)", 
                                    command=on_read, width=20, height=2).pack(side="right", padx=20) 
                                    # chaining pack to assign right
