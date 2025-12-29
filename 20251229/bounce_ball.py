import tkinter as tk

def move_ball():
    global vx, vy
    # 1. 현재 공의 좌상단(x1, y1), 우하단(x2, y2) 좌표를 한 번에 가져옴
    x1, y1, x2, y2 = canvas.coords(ball)

    # 2. 벽에 부딪히면 속도 반전 (0보다 작거나 400보다 크면)
    if x1 <= 0 or x2 >= 400: vx = -vx
    if y1 <= 0 or y2 >= 400: vy = -vy

    # 3. 실제 이동 및 무한 루프
    canvas.move(ball, vx, vy)
    root.after(20, move_ball)

root = tk.Tk()
root.title("핑퐁")
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

ball = canvas.create_oval(190, 190, 210, 210, fill="red")
vx, vy = 5, 3 # x축, y축 속도 설정

move_ball()
root.mainloop()