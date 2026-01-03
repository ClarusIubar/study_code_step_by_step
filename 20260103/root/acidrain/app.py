import tkinter as tk
import json
import random
import os
import common.config as cfg
from common.physics import Physics_Core
from acidrain.word_ball import WordBall
# from acidrain.storage import AcidRainStorage # 별도 생성 필요

class AcidRainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("전략적 산성비")
        
        # 1. 초기 세팅
        self.physics_core = Physics_Core(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
        # self.storage = AcidRainStorage()
        self.load_words()
        
        # 2. 게임 상태 변수
        self.score = 0
        self.life = 5
        self.current_max_level = 2
        self.spawn_interval = 1000 # 1초 시작
        self.elapsed_time = 0      # 경과 시간(ms)
        self.active_balls = []
        self.is_running = True
        
        # 3. UI 구성
        self.canvas = tk.Canvas(root, width=cfg.WINDOW_WIDTH, height=500, bg="#222")
        self.canvas.pack(fill="both", expand=True)
        
        # 입력창 (Entry)
        self.entry = tk.Entry(root, font=("Arial", 14), justify="center")
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.handle_input) # 엔터키 바인딩
        self.entry.focus_set()
        
        # 점수/생명력 표시
        self.status_label = tk.Label(root, text=f"Score: 0 | Life: {'❤️'*5}", font=("Arial", 12))
        self.status_label.pack()

        self.win_y = 480 # 생명력 감소 경계선
        self.start_game()

    def load_words(self):
        json_path = os.path.join(os.path.dirname(__file__), "words.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.word_data = json.load(f)

    def start_game(self):
        self.spawn_word()
        self.run_physics()
        self.update_difficulty()

    def spawn_word(self):
        """ 레벨에 맞는 단어를 랜덤하게 생성"""
        if not self.is_running: return
        
        # 현재 도달한 레벨까지의 단어들을 합침
        pool = []
        for lv in range(2, self.current_max_level + 1):
            pool.extend([(w, lv) for w in self.word_data[f"level{lv}"]])
            
        word, level = random.choice(pool)
        x = random.randint(50, cfg.WINDOW_WIDTH - 50)
        ball = WordBall(self.canvas, word, level, x, -30)
        self.active_balls.append(ball)
        
        # 난이도에 따라 생성 간격 조절 (최소 400ms)
        self.spawn_interval = max(400, self.spawn_interval - 10)
        self.root.after(self.spawn_interval, self.spawn_word)

    def handle_input(self, event):
        """ 입력된 단어와 일치하는 모든 볼 제거 (중복 허용)"""
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        to_remove = [b for b in self.active_balls if b.word == user_input]
        
        for ball in to_remove:
            # 레벨별 점수 가산
            score_map = {2: 10, 3: 15, 4: 20}
            self.score += score_map.get(ball.level, 0)
            
            # 시각적 소멸
            self.canvas.delete(ball.oval)
            self.canvas.delete(ball.text)
            self.active_balls.remove(ball)
            
        self.update_status()

    def run_physics(self):
        """ 물리 연산 및 하단 충돌 체크"""
        if not self.is_running: return
        
        self.physics_core.collision(self.active_balls)
        for ball in self.active_balls[:]:
            ball.update()
            
            # 하단 영역 닿음 -> 생명력 감소
            if ball.check_collision(self.win_y):
                self.life -= 1
                self.canvas.delete(ball.oval)
                self.canvas.delete(ball.text)
                self.active_balls.remove(ball)
                self.update_status()
                
                if self.life <= 0:
                    self.game_over()
                    return

        self.root.after(cfg.FRAME_RATE_MS, self.run_physics)

    def update_difficulty(self):
        """ 1분마다 레벨 상승"""
        if not self.is_running: return
        self.elapsed_time += 1000
        
        if self.elapsed_time >= 120000: # 2분 경과
            self.current_max_level = 4
        elif self.elapsed_time >= 60000: # 1분 경과
            self.current_max_level = 3
            
        self.root.after(1000, self.update_difficulty)

    def update_status(self):
        hearts = "❤️" * self.life
        self.status_label.config(text=f"Score: {self.score} | Life: {hearts}")

    def game_over(self):
        self.is_running = False
        self.storage.save_score(self.score) # 점수 저장
        # TODO: GameOverPopup 띄우기 (로또의 ResultPopup 상속 응용)
        print(f"GAME OVER! 최종 점수: {self.score}")