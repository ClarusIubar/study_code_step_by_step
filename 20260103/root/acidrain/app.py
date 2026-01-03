import tkinter as tk
import json, random, os
import common.config as cfg
from common.physics import Physics_Core
from .word_ball import WordBall
from .storage import AcidRainStorage
from .controller import AcidRainController
from .game_over_popup import GameOverPopup
from .score_record_popup import ScoreRecordPopup

class AcidRainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("전략적 산성눈")
        self.physics = Physics_Core(cfg.WindowConfig.WIDTH, cfg.WindowConfig.HEIGHT)
        self.storage = AcidRainStorage()
        self._load_words()
        self._build_ui()
        self.active_balls, self.is_running = [], False

    def _build_ui(self):
        self.canvas = tk.Canvas(self.root, width=cfg.WindowConfig.WIDTH, height=500, bg="#222")
        self.canvas.pack(fill="both", expand=True)
        self.entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
        self.entry.pack(pady=10); self.entry.bind("<Return>", self.handle_input)
        self.controller = AcidRainController(self.root, on_start=self.start_game, on_read=self.show_records)
        self.controller.pack(fill="x", side="bottom")
        self.status_label = tk.Label(self.root, text="시작 버튼을 누르세요", font=("Arial", 12)); self.status_label.pack()
        self.win_y = 480

    def start_game(self):
        if self.is_running: return
        self.score, self.life, self.elapsed_time = 0, cfg.AcidRainConfig.Rules.LIFE, 0
        self.active_balls, self.is_running, self.current_max_level = [], True, 2
        self.canvas.delete("word"); self.entry.focus_set(); self.update_status()
        self.spawn_interval, self.min_interval = cfg.AcidRainConfig.Rules.SPAWN_MS
        self._run_loops()

    def _run_loops(self):
        self._spawn_loop(); self._physics_loop(); self._difficulty_loop()

    def _spawn_loop(self):
        if not self.is_running: return
        self._create_ball()
        self.spawn_interval = max(self.min_interval, self.spawn_interval - 10)
        self.root.after(self.spawn_interval, self._spawn_loop)

    def _physics_loop(self):
        if not self.is_running: return
        self.physics.collision(self.active_balls)
        for ball in self.active_balls[:]:
            self.physics.gravity(ball, cfg.AcidRainConfig.Physics.GRAVITY)
            self.physics.wall_limit(ball); ball.update()
            if ball.check_collision(self.win_y):
                self.life -= 1; self._remove_ball(ball); self.update_status()
                if self.life <= 0: self._game_over(); return
        self.root.after(cfg.PhysicsConfig.FRAME_RATE_MS, self._physics_loop)

    def _difficulty_loop(self):
        if not self.is_running: return
        self.elapsed_time += 1000
        limit = cfg.AcidRainConfig.Rules.LEVEL_UP_MS
        if self.elapsed_time >= limit * 2: self.current_max_level = 4
        elif self.elapsed_time >= limit: self.current_max_level = 3
        self.root.after(1000, self._difficulty_loop)

    def _create_ball(self):
        pool = []
        for lv in range(2, self.current_max_level + 1):
            pool.extend([(w, lv) for w in self.word_data[f"level{lv}"]])
        word, level = random.choice(pool)
        self.active_balls.append(WordBall(self.canvas, word, level, random.randint(50, 550), -30))

    def handle_input(self, e):
        if not self.is_running: return
        val = self.entry.get().strip(); self.entry.delete(0, tk.END)
        for ball in [b for b in self.active_balls if b.word == val]:
            self.score += cfg.AcidRainConfig.Assets.DATA[ball.level]["score"]
            self._remove_ball(ball)
        self.update_status()

    def _remove_ball(self, ball):
        self.canvas.delete(ball.oval); self.canvas.delete(ball.text)
        if ball in self.active_balls: self.active_balls.remove(ball)

    def _load_words(self):
        p = os.path.join(os.path.dirname(__file__), "words.json")
        with open(p, "r", encoding="utf-8") as f: self.word_data = json.load(f)

    def update_status(self): self.status_label.config(text=f"Score: {self.score} | Life: {'❤️'*self.life}")
    def _game_over(self): self.is_running = False; GameOverPopup(self.root, self.score, self.storage.save_score)
    def show_records(self): ScoreRecordPopup(self.root, self.storage)