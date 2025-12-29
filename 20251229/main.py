import tkinter as tk

WIDTH = 400
HEIGHT = 400
COLOR = "white"
TITLE = "킨터를 가지고 놀래요."

root = tk.Tk()
root.title(TITLE)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLOR)
canvas.pack()
root.mainloop()