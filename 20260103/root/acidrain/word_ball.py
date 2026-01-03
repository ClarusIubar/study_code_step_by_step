import random
import common.config as cfg

class WordBall:
    def __init__(self, canvas, word, level, x, y):
        self.canvas, self.word, self.level = canvas, word, level
        self.radius = cfg.AcidRainConfig.WORD_RADIUS
        
        # [정합성] config의 SPEED_RANGE를 언팩킹하여 적용
        self.dx = random.uniform(*cfg.AcidRainConfig.SPEED_X_RANGE)
        self.dy = random.uniform(*cfg.AcidRainConfig.SPEED_Y_RANGE)
        
        color_map = {2: "#fbc400", 3: "#69cfff", 4: "#ff7272"}
        self.color = color_map.get(level, "white")
        
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, 
                                       fill=self.color, outline="black", tags="word")
        self.text = canvas.create_text(x, y, text=word, font=("Arial", 10, "bold"), tags="word")

    def get_pos(self):
        coords = self.canvas.coords(self.oval)
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    def move_by(self, tx, ty):
        self.canvas.move(self.oval, tx, ty); self.canvas.move(self.text, tx, ty)

    def update(self): self.move_by(self.dx, self.dy)

    def check_collision(self, win_y):
        _, y = self.get_pos()
        return y + self.radius >= win_y