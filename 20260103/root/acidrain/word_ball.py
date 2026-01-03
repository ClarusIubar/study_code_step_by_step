# acidrain/word_ball.py
import random
import common.config as cfg
from common.base_ball import BaseBall

class WordBall(BaseBall):
    def __init__(self, canvas, word, level, x, y):
        conf = cfg.AcidRainConfig.Physics
        asset = cfg.AcidRainConfig.Assets.DATA.get(level, {"color": "white"})
        
        dx = random.uniform(*conf.SPEED_X)
        dy = random.uniform(*conf.SPEED_Y)
        super().__init__(canvas, conf.WORD_RADIUS, dx, dy, x, y)
        
        self.word, self.level = word, level
        self.color = asset["color"]
        
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, 
                                       fill=self.color, outline="black", tags="word")
        self.text = canvas.create_text(x, y, text=word, font=("Arial", 10, "bold"), tags="word")