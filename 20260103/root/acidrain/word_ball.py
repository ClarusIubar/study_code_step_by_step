import random
import common.config as cfg

class WordBall:
    def __init__(self, canvas, word, level, x, y):
        self.canvas = canvas
        self.word = word
        self.level = level
        
        # 물리 인터페이스 (LottoBall과 동일하게 유지하여 엔진 호환)
        self.radius = 25 # 글자가 보여야 하므로 로또볼보다 크게 설정
        self.dx = random.uniform(-1, 1) # 산성비는 낙하 위주이므로 좌우 반동 최소화
        self.dy = random.uniform(1, 3)  # 낙하 속도
        
        # 레벨별 색상 (LottoBall의 _get_color 로직 응용)
        color_map = {2: "#fbc400", 3: "#69cfff", 4: "#ff7272"}
        self.color = color_map.get(level, "white")
        
        # 시각적 요소
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, 
                                       x+self.radius, y+self.radius, 
                                       fill=self.color, outline="black", tags="word")
        self.text = canvas.create_text(x, y, text=word, font=("Arial", 10, "bold"), tags="word")

    def get_pos(self):
        coords = self.canvas.coords(self.oval)
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    def move_by(self, tx, ty):
        self.canvas.move(self.oval, tx, ty)
        self.canvas.move(self.text, tx, ty)

    def update(self):
        self.move_by(self.dx, self.dy)

    def check_collision(self, win_y):
        _, y = self.get_pos()
        return y + self.radius >= win_y