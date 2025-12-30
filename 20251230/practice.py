import tkinter as tk

WIDTH, HEIGHT = 400, 400
COLOR = "white"

class Ball:
    def __init__(self, canvas, x1, y1, x2, y2, vx, vy, fill="yellow"):
        self.canvas = canvas
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.vx, self.vy = vx, vy
        self.fill = fill
        self.id = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.fill)

    def move(self):
        # 데이터(좌표) 갱신
        self.x1 += self.vx
        self.x2 += self.vx
        self.y1 += self.vy
        self.y2 += self.vy

        # 캔버스에 닿으면, 속도 반전을 해서 튕겨 나가는 것처럼 보이게 한다.
        if self.x1 <= 0 or self.x2 >= WIDTH:
            self.vx = -self.vx
        if self.y1 <= 0 or self.y2 >= HEIGHT:
            self.vy = -self.vy
            
        self.canvas.coords(self.id, self.x1, self.y1, self.x2, self.y2)


root = tk.Tk()
root.title("공이 살아 움직여요")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLOR)
canvas.pack()

balls = []
ball_1 = Ball(canvas, 40, 40, 80, 80, 5, 10, "yellow")
ball_2 = Ball(canvas, 120, 120, 160, 160, 8, 7, "blue")
balls.append(ball_1)
balls.append(ball_2)

def move_loop():
    for ball in balls:
        ball.move() # 움직여
    root.after(20, move_loop) # 20ms마다, 계속

# 루프 시작
move_loop()
root.mainloop()