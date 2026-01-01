import tkinter as tk

class LottoController(tk.Frame):
    def __init__(self, root, on_draw, on_read):
        super().__init__(root, bg="#333", pady=10)
        tk.Button(self, text="6/45 공 투입 (Create)", command=on_draw, width=20, height=2).pack(side="left", padx=20)
        tk.Button(self, text="무작위 5개 조회 (Read)", command=on_read, width=20, height=2).pack(side="left", padx=20)
