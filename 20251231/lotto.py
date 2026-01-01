import tkinter as tk
import random
import time
import math

# 1. [LottoBall] 공의 물리와 렌더링
class LottoBall:
    def __init__(self, canvas, number, x, y):
        self.canvas = canvas
        self.number = number
        self.radius = 12
        self.is_captured = False
        self.color = self._get_color(number)
        
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, 
                                       fill=self.color, outline="black", tags="ball")
        self.text = canvas.create_text(x, y, text=str(number), font=("Arial", 8, "bold"), tags="ball")
        
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(3, 6) # 초기 낙하 속도 보장
        self.gravity = 0.2

    def _get_color(self, n):
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

# 2. [LottoStorage] 데이터 저장 및 랜덤 조회
class LottoStorage:
    def __init__(self):
        self.records = []
    def save(self, nums):
        self.records.append({"id": len(self.records)+1, "nums": nums, "time": time.strftime("%H:%M:%S")})
    def get_random_5(self):
        return random.sample(self.records, min(len(self.records), 5))

# 3. [LottoController] 버튼 인터페이스
class LottoController(tk.Frame):
    def __init__(self, master, on_draw, on_read):
        super().__init__(master, bg="#333", pady=10)
        tk.Button(self, text="6/45 공 투입 (Create)", command=on_draw, width=20, height=2).pack(side="left", padx=20)
        tk.Button(self, text="무작위 5개 조회 (Read)", command=on_read, width=20, height=2).pack(side="left", padx=20)

# 4. [LottoApp] 메인 로직 및 애니메이션
class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("이단아의 진짜 물리 6/45 CRUD")
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

# 5. [Main] 실행
if __name__ == "__main__":
    root = tk.Tk(); app = LottoApp(root); root.mainloop()