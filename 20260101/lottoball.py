import random

class LottoBall:
    def __init__(self, canvas, number, x, y):
        self.canvas = canvas
        self.number = number
        self.radius = 12
        self.is_captured = False
        self.color = self.get_color(number)
        
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, 
                                       fill=self.color, outline="black", tags="ball")
        self.text = canvas.create_text(x, y, text=str(number), font=("Arial", 8, "bold"), tags="ball")
        
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(3, 6) # 초기 낙하 속도 보장
        self.gravity = 0.2

    def get_color(self, n):
        if n <= 10: return "#fbc400"
        if n <= 20: return "#69cfff"
        if n <= 30: return "#ff7272"
        if n <= 40: return "#aaaaaa"
        return "#b0d840"

    def get_pos(self):
        c = self.canvas.coords(self.oval)
        if not c: return 0, 0
        return (c[0]+c[2])/2, (c[1]+c[3])/2

    def move(self, w, win_y):
        if self.is_captured: return
        self.dy += self.gravity
        self.canvas.move(self.oval, self.dx, self.dy)
        self.canvas.move(self.text, self.dx, self.dy)
        
        x, y = self.get_pos()
        # 좌우 벽 반사
        if x - self.radius < 0 or x + self.radius > w: self.dx *= -0.7
        # 천장 반사: 화면 안(y > radius)으로 들어온 후에만 작동하게 수정 (끼임 방지 핵심)
        if y - self.radius < 0 and y > self.radius: self.dy *= -0.7

    def check_collision(self, win_y):
        if self.is_captured: return False
        _, y = self.get_pos()
        if y + self.radius >= win_y:
            self.is_captured = True
            return True
        return False