import tkinter as tk
import random
import time
import math

# --- 1. [LottoBall 클래스] : 물리 속성 및 개별 충돌 로직 ---
class LottoBall:
    def __init__(self, canvas, number, x, y):
        self.canvas = canvas
        self.number = number
        self.radius = 12
        self.is_captured = False
        self.color = self._get_color(number)
        
        # 렌더링
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill=self.color, outline="black", tags="ball")
        self.text = canvas.create_text(x, y, text=str(number), font=("Arial", 8, "bold"), tags="ball")
        
        # 물리 초기화
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-4, 4)
        self.gravity = 0.2  # 중력 가속도 추가

    def _get_color(self, n):
        if n <= 10: return "#fbc400"
        if n <= 20: return "#69cfff"
        if n <= 30: return "#ff7272"
        if n <= 40: return "#aaaaaa"
        return "#b0d840"

    def get_pos(self):
        """공의 중심 좌표 반환"""
        coords = self.canvas.coords(self.oval)
        if not coords: return 0, 0
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    def move(self, w, win_y):
        if self.is_captured: return
        
        self.dy += self.gravity # 중력 적용
        self.canvas.move(self.oval, self.dx, self.dy)
        self.canvas.move(self.text, self.dx, self.dy)
        
        x, y = self.get_pos()
        # 벽 반사 (에너지 손실 0.8 적용)
        if x - self.radius <= 0 or x + self.radius >= w:
            self.dx *= -0.8
            # 벽 끼임 방지 보정
            self.canvas.move(self.oval, (1 if x - self.radius <= 0 else -1), 0)
        if y - self.radius <= 0:
            self.dy *= -0.8

    def check_collision(self, win_y):
        if self.is_captured: return False
        _, y = self.get_pos()
        if y + self.radius >= win_y:
            self.is_captured = True
            return True
        return False

# --- 2. [LottoStorage 클래스] : 데이터 관리 (CRUD - R/S) ---
class LottoStorage:
    def __init__(self):
        self.records = []

    def save_result(self, nums):
        data = {"id": len(self.records) + 1, "nums": nums, "time": time.strftime("%H:%M:%S")}
        self.records.append(data)

    def get_random_5(self):
        if not self.records: return []
        count = min(len(self.records), 5)
        return random.sample(self.records, count)

# --- 3. [LottoController 클래스] : UI 인터페이스 ---
class LottoController(tk.Frame):
    def __init__(self, master, draw_cmd, view_cmd):
        super().__init__(master, bg="#333", pady=10)
        tk.Button(self, text="6/45 공 투입 (Create)", command=draw_cmd, width=20, height=2, bg="#555", fg="white").pack(side="left", padx=20)
        tk.Button(self, text="무작위 5개 조회 (Read)", command=view_cmd, width=20, height=2, bg="#555", fg="white").pack(side="left", padx=20)

# --- 4. [LottoApp 클래스] : 메인 엔진 및 충돌 오케스트레이션 ---
class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("이단아의 진짜 물리 6/45 CRUD")
        self.root.geometry("600x650")
        
        self.storage = LottoStorage()
        self.balls = []
        self.winners = []
        self.is_animating = False

        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack(fill="both", expand=True)
        
        self.win_y = 450
        self.canvas.create_rectangle(0, self.win_y, 600, 500, fill="#FFD700", outline="")
        self.canvas.create_text(300, 475, text="WINNING ZONE (물리적 순차 채택)", font=("Arial", 12, "bold"))

        self.controller = LottoController(root, self.start_draw, self.show_records)
        self.controller.pack(fill="x", side="bottom")

    def start_draw(self):
        if self.is_animating: return
        self.canvas.delete("ball")
        # 시작 시 45개 공 생성
        self.balls = [LottoBall(self.canvas, i, random.randint(50, 550), random.randint(20, 150)) for i in range(1, 46)]
        self.winners = []
        self.is_animating = True
        self.run_physics()

    def run_physics(self):
        if not self.is_animating: return
        
        # 공 대 공 충돌 해소 (Position Correction 추가)
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                b1, b2 = self.balls[i], self.balls[j]
                if b1.is_captured or b2.is_captured: continue
                
                x1, y1 = b1.get_pos()
                x2, y2 = b2.get_pos()
                
                dx, dy = x2 - x1, y2 - y1
                dist = math.sqrt(dx**2 + dy**2)
                min_dist = b1.radius + b2.radius

                if dist < min_dist and dist > 0:
                    # 1. 위치 보정 (서로 밀어내어 겹침 및 진동 방지)
                    overlap = min_dist - dist
                    nx, ny = dx/dist, dy/dist
                    self.canvas.move(b1.oval, -nx*overlap/2, -ny*overlap/2)
                    self.canvas.move(b1.text, -nx*overlap/2, -ny*overlap/2)
                    self.canvas.move(b2.oval, nx*overlap/2, ny*overlap/2)
                    self.canvas.move(b2.text, nx*overlap/2, ny*overlap/2)
                    
                    # 2. 운동량 교환 (탄성 충돌)
                    b1.dx, b2.dx = b2.dx * 0.9, b1.dx * 0.9
                    b1.dy, b2.dy = b2.dy * 0.9, b1.dy * 0.9

        # 이동 및 당첨 존 체크
        for b in self.balls:
            b.move(600, self.win_y)
            if len(self.winners) < 6 and b.check_collision(self.win_y):
                self.winners.append(b.number)
                self.canvas.itemconfig(b.oval, outline="red", width=3)

        if len(self.winners) < 6:
            self.root.after(15, self.run_physics)
        else:
            self.is_animating = False
            self.root.after(500, self.ask_save_or_delete)

    def ask_save_or_delete(self):
        pop = tk.Toplevel(self.root)
        pop.title("결과 처리")
        pop.transient(self.root); pop.grab_set()
        
        w, h = 300, 150
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - (w//2)
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - (h//2)
        pop.geometry(f"{w}x{h}+{x}+{y}")

        res = sorted(self.winners)
        tk.Label(pop, text=f"추첨 결과: {res}\n저장하시겠습니까?", font=("Arial", 11)).pack(pady=20)
        btn_f = tk.Frame(pop); btn_f.pack()
        tk.Button(btn_f, text="저장", width=10, command=lambda: [self.storage.save_result(res), pop.destroy()]).pack(side="left", padx=10)
        tk.Button(btn_f, text="삭제", width=10, command=pop.destroy).pack(side="right", padx=10)

    def show_records(self):
        data = self.storage.get_random_5()
        view = tk.Toplevel(self.root); view.title("랜덤 5개")
        w, h = 400, 300
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - (w//2)
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - (h//2)
        view.geometry(f"{w}x{h}+{x}+{y}")

        if not data:
            tk.Label(view, text="기록 없음", pady=50).pack()
            return
        for r in data:
            tk.Label(view, text=f"[{r['id']}회차] {r['nums']} ({r['time']})").pack(pady=5)

# --- 5. [Main] ---
if __name__ == "__main__":
    root = tk.Tk()
    LottoApp(root)
    root.mainloop()