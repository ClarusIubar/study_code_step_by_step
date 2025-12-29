import tkinter as tk

WIDTH = 400
HEIGHT = 400
COLOR = "white"
TITLE = "킨터를 가지고 놀래요."
TEXT = "안녕하세요."
FONT = ("Ariel",15)
FILL_RECT = "blue"
FILL_OVAL = "yellow"
FILL_TEXT = "black"
OUTLINE = "black" # not used

root = tk.Tk()
root.title(TITLE)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLOR)
canvas.pack()

canvas.create_rectangle(50, 50, 150, 150, fill=FILL_RECT)
canvas.create_oval(200, 200, 300, 300, fill=FILL_OVAL)
canvas.create_text(300, 350, text=TEXT, font=FONT, fill=FILL_TEXT)

root.mainloop()