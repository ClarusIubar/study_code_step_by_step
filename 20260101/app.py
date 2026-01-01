import tkinter as tk
import math
import random
import lottoball
import controller
import storage

class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("이단아의 진짜 물리 6/45 CRUD")
        self.root.geometry("600x650")
        self.storage = storage.LottoStorage()

        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.win_y = 450
        self.canvas.create_rectangle(0, self.win_y, 600, 500, fill="#FFD700", outline="")
        self.canvas.create_text(300, 475, text="WINNING ZONE", font=("Arial", 12, "bold"))

        self.controller = controller.LottoController(root, self.start_draw, self.show_records)
        self.controller.pack(fill="x", side="bottom")
        self.balls = []; self.winners = []; self.is_animating = False

    def start_draw(self):
        if self.is_animating: return
        self.canvas.delete("ball")
        self.winners = []
        # 상단 밖에서 떨어지는 연출 (끼임 로직 수정으로 이제 정상 작동)
        self.balls = [lottoball.LottoBall(self.canvas, i, random.randint(50, 550), random.randint(-150, -30)) for i in range(1, 46)]
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
        pop = tk.Toplevel(self.root); pop.title("결과"); pop.grab_set()
        w, h = 300, 150
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - (w//2)
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - (h//2)
        pop.geometry(f"{w}x{h}+{x}+{y}")
        res = sorted(self.winners)
        tk.Label(pop, text=f"당첨 번호: {res}\n저장하시겠습니까?").pack(pady=20)
        f = tk.Frame(pop); f.pack()
        tk.Button(f, text="저장", width=10, command=lambda: [self.storage.save(res), pop.destroy()]).pack(side="left", padx=10)
        tk.Button(f, text="삭제", width=10, command=pop.destroy).pack(side="right", padx=10)

    def show_records(self):
        data = self.storage.get_random_5()
        v = tk.Toplevel(self.root); v.title("랜덤 5개")
        if not data: tk.Label(v, text="데이터 없음", pady=50).pack(); return
        for r in data: tk.Label(v, text=f"[{r['id']}] {r['nums']} ({r['time']})").pack(pady=5)
