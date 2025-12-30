import tkinter as tk

# constant
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
VELOCITY_X = 5
VELOCITY_Y = 10

# basic structure
root = tk.Tk()
root.title(TITLE)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLOR)
canvas.pack()

# object generate
# canvas.create_rectangle(50, 50, 150, 150, fill=FILL_RECT)
ball = canvas.create_oval(40, 40, 80, 80, fill=FILL_OVAL)
# canvas.create_text(300, 350, text=TEXT, font=FONT, fill=FILL_TEXT)

def move_loop():
    global VELOCITY_X, VELOCITY_Y
    # 볼 자체의 좌표
    x1, y1, x2, y2 = canvas.coords(ball)

    # 좌우 벽 충돌 검사
    # 충돌시, x축 속도 반전
    if x1 <= 0 or x2 >= WIDTH:
        VELOCITY_X = -VELOCITY_X # 반전을 해야하기 때문에 명시적으로 변경해야함.

    # 상하 벽 충돌 검사
    # 충돌시, 속도 반전
    if y1 <= 0 or y2 >= HEIGHT:
        VELOCITY_Y = -VELOCITY_Y
    # ball 객체를 상수항만큼 이동
    canvas.move(ball, VELOCITY_X, VELOCITY_Y)
    # 반복적으로 불러오기
    root.after(20, move_loop) # 단위 : 20ms

# 4. 루프 시작
move_loop()
root.mainloop()