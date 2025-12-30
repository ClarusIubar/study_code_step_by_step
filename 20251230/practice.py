import tkinter as tk

# constant
WIDTH = 400
HEIGHT = 400
COLOR = "white"
TITLE = "킨터를 가지고 놀래요."
TEXT = "안녕하세요."
FONT = ("Ariel",15)
OUTLINE = "black" # not used

# basic structure
root = tk.Tk()
root.title(TITLE)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLOR)
canvas.pack()

class Ball:
    def __init__(self, x1, y1, x2, y2, fill):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.fill = fill
    
    def get_coords(self):
        return (self.x1, self.y1, self.x2, self.y2)


ball = Ball(40, 40, 80, 80, "Yellow")
# 추상적으로는 볼이라는 객체를 주면, 알아서 값이 전달될 것이라고 생각했지만,
# args형태로 작성되어 있지 않아서 직접 전달값을 담아서 전달해야한다.

deploy_1 = canvas.create_oval(*ball.get_coords(), fill=ball.fill) 

def move_loop(object):
    global VELOCITY_X, VELOCITY_Y
    # 볼 자체의 좌표
    x1, y1, x2, y2 = canvas.coords(object)

    # 좌우 벽 충돌 검사
    # 충돌시, x축 속도 반전
    if x1 <= 0 or x2 >= WIDTH:
        VELOCITY_X = -VELOCITY_X # 반전을 해야하기 때문에 명시적으로 변경해야함.

    # 상하 벽 충돌 검사
    # 충돌시, 속도 반전
    if y1 <= 0 or y2 >= HEIGHT:
        VELOCITY_Y = -VELOCITY_Y
    # ball 객체를 상수항만큼 이동
    canvas.move(object, VELOCITY_X, VELOCITY_Y)
    # 반복적으로 불러오기
    root.after(20, move_loop) # 단위 : 20ms

# 4. 루프 시작
move_loop(deploy_1)
root.mainloop()