import tkinter as tk
import math
import random
from lottoball import LottoBall
from controller import LottoController
from storage import LottoStorage
from record_popup import RecordViewPopup
from result_popup import LottoResultPopup

class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("생성, 조회마저도 `랜덤`인 이단 6/45 로또")
        self.root.geometry("600x650")
        self.storage = LottoStorage()

        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.win_y = 450
        self.canvas.create_rectangle(0, self.win_y, 600, 500, fill="#FFD700", outline="")
        self.canvas.create_text(300, 475, text="WINNING ZONE", font=("Arial", 12, "bold"))

        self.controller = LottoController(root, self.start_draw, self.show_records)
        self.controller.pack(fill="x", side="bottom")
        self.balls = []; self.winners = []; self.is_animating = False

    def start_draw(self):
        if self.is_animating: return
        self.canvas.delete("ball")
        self.winners = []
        # 상단 밖에서 떨어지는 연출 (끼임 로직 수정으로 이제 정상 작동)
        self.balls = [LottoBall(self.canvas, i, random.randint(50, 550), random.randint(-150, -30)) for i in range(1, 46)]
        self.is_animating = True
        self.run_physics()

    def run_physics(self):
        if not self.is_animating: return
        # 충돌 해소
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                b1, b2 = self.balls[i], self.balls[j]
                if b1.is_captured or b2.is_captured: continue
                x1, y1 = b1.get_pos(); x2, y2 = b2.get_pos()
                dx, dy = x2 - x1, y2 - y1
                dist = math.sqrt(dx**2 + dy**2)
                if 0 < dist < (b1.radius + b2.radius):
                    overlap = (b1.radius + b2.radius) - dist
                    nx, ny = dx/dist, dy/dist
                    self.canvas.move(b1.oval, -nx*overlap/2, -ny*overlap/2)
                    self.canvas.move(b1.text, -nx*overlap/2, -ny*overlap/2)
                    self.canvas.move(b2.oval, nx*overlap/2, ny*overlap/2)
                    self.canvas.move(b2.text, nx*overlap/2, ny*overlap/2)
                    p = (b1.dx * nx + b1.dy * ny - b2.dx * nx - b2.dy * ny)
                    b1.dx -= p * nx; b1.dy -= p * ny
                    b2.dx += p * nx; b2.dy += p * ny
        # 이동 및 채택
        for b in self.balls:
            b.move(600, self.win_y)
            if len(self.winners) < 6 and b.check_collision(self.win_y):
                self.winners.append(b.number)
                self.canvas.itemconfig(b.oval, outline="red", width=3)
        if len(self.winners) < 6: self.root.after(15, self.run_physics)
        else:
            self.is_animating = False
            self.root.after(500, self.popup)

    def popup(self):
        # 팝업 생성 시 리스크 분산: 
        # 1. numbers를 소팅해서 전달 (데이터 정합성)
        # 2. 저장 로직(callback)만 넘겨서 popup이 storage를 직접 참조하지 않게 함(DIP 원칙)
        res = sorted(self.winners)
        LottoResultPopup(self.root, res, self.storage.save)

    def show_records(self):
        data = self.storage.get_random_5()
        RecordViewPopup(self.root, data)
