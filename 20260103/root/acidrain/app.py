import tkinter as tk
import json, random, os
import common.config as cfg
from common.physics import Physics_Core
from acidrain.word_ball import WordBall
from acidrain.storage import AcidRainStorage
from acidrain.controller import AcidRainController
from acidrain.game_over_popup import GameOverPopup
from acidrain.score_record_popup import ScoreRecordPopup

class AcidRainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("산성눈")
        
        self.physics_core = Physics_Core(cfg.WindowConfig.WIDTH, cfg.WindowConfig.HEIGHT)
        self.storage = AcidRainStorage()
        self.load_words()
        
        # 초기 상태 설정
        self.score = 0
        self.life = cfg.AcidRainConfig.LIFE
        self.elapsed_time = 0 # [수정] 경과 시간 초기화
        self.active_balls = []
        self.is_running = False
        
        self.canvas = tk.Canvas(root, width=cfg.WindowConfig.WIDTH, height=500, bg="#222")
        self.canvas.pack(fill="both", expand=True)
        
        self.entry = tk.Entry(root, font=("Arial", 14), justify="center")
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.handle_input)
        
        self.controller = AcidRainController(root, on_start=self.start_game, on_read=self.show_records)
        self.controller.pack(fill="x", side="bottom")
        
        self.status_label = tk.Label(root, text="시작 버튼을 누르세요", font=("Arial", 12))
        self.status_label.pack()
        self.win_y = 480

    def load_words(self):
        json_path = os.path.join(os.path.dirname(__file__), "words.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.word_data = json.load(f)

    def start_game(self):
        if self.is_running: return
        
        # 게임 상태 리셋
        self.score = 0
        self.life = cfg.AcidRainConfig.LIFE
        self.elapsed_time = 0 # 시간 리셋
        self.active_balls = []
        self.canvas.delete("word")
        self.is_running = True
        self.spawn_interval = cfg.AcidRainConfig.SPAWN_INITIAL_MS
        self.current_max_level = 2
        
        self.entry.focus_set()
        self.spawn_word()
        self.run_physics()
        self.update_difficulty() # [중요] 누락되었던 메서드 호출 추가
        self.update_status()

    def spawn_word(self):
        if not self.is_running: return
        pool = []
        for level in range(2, self.current_max_level + 1):
            pool.extend([(word, level) for word in self.word_data[f"level{level}"]])
        
        word, level = random.choice(pool)
        x = random.randint(50, cfg.WindowConfig.WIDTH - 50)
        self.active_balls.append(WordBall(self.canvas, word, level, x, -30))
        
        self.spawn_interval = max(cfg.AcidRainConfig.SPAWN_MIN_MS, self.spawn_interval - 10)
        self.root.after(self.spawn_interval, self.spawn_word)

    def handle_input(self, event):
        if not self.is_running: return
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        target_balls = [ball for ball in self.active_balls if ball.word == user_input]
        for ball in target_balls:
            self.score += cfg.AcidRainConfig.SCORES.get(ball.level, 0)
            self.canvas.delete(ball.oval)
            self.canvas.delete(ball.text)
            self.active_balls.remove(ball)
        self.update_status()

    def run_physics(self):
        if not self.is_running: return
        self.physics_core.collision(self.active_balls)
        for ball in self.active_balls[:]:
            self.physics_core.gravity(ball, cfg.AcidRainConfig.GRAVITY)
            self.physics_core.wall_limit(ball) # 벽 충돌 로직
            ball.update()
            
            if ball.check_collision(self.win_y):
                self.life -= 1
                self.canvas.delete(ball.oval)
                self.canvas.delete(ball.text)
                self.active_balls.remove(ball)
                self.update_status()
                if self.life <= 0:
                    self.game_over()
                    return
        self.root.after(cfg.PhysicsConfig.FRAME_RATE_MS, self.run_physics)

    # [수리] 완전히 빠져있던 난이도 조절 메서드 추가
    def update_difficulty(self):
        if not self.is_running: return
        
        self.elapsed_time += 1000 # 1초마다 누적
        
        # config에 정의한 LEVEL_UP_MS(20000) 기준으로 레벨업
        if self.elapsed_time >= cfg.AcidRainConfig.LEVEL_UP_MS * 2:
            if self.current_max_level < 4:
                self.current_max_level = 4
        elif self.elapsed_time >= cfg.AcidRainConfig.LEVEL_UP_MS:
            if self.current_max_level < 3:
                self.current_max_level = 3
                
        self.root.after(1000, self.update_difficulty)

    def update_status(self):
        self.status_label.config(text=f"Score: {self.score} | Life: {'❤️'*self.life}")

    def game_over(self):
        self.is_running = False
        GameOverPopup(self.root, self.score, self.storage.save_score)

    def show_records(self):
        ScoreRecordPopup(self.root, self.storage)