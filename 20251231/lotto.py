import tkinter as tk
import random
import time

# --- 1. [LottoBall 클래스] : 개별 공의 물리 좌표와 렌더링 관리 ---
class LottoBall:
    def __init__(self, canvas, number, x, y):
        self.canvas = canvas
        self.number = number
        self.radius = 12
        self.is_captured = False
        self.color = self._get_color(number)
        
        # 공 및 번호 생성
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill=self.color, outline="black", tags="ball")
        self.text = canvas.create_text(x, y, text=str(number), font=("Arial", 8, "bold"), tags="ball")
        
        # 물리 속도 (X는 튕기기, Y는 아래로 떨어지는 힘 중심)
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(2, 5)

    def _get_color(self, n):
        if n <= 10: return "#fbc400"
        if n <= 20: return "#69cfff"
        if n <= 30: return "#ff7272"
        if n <= 40: return "#aaaaaa"
        return "#b0d840"

    def move(self, w, win_y):
        if self.is_captured: return
        
        self.canvas.move(self.oval, self.dx, self.dy)
        self.canvas.move(self.text, self.dx, self.dy)
        
        pos = self.canvas.coords(self.oval)
        # 벽 반사 로직
        if pos[0] <= 0 or pos[2] >= w: self.dx *= -1
        if pos[1] <= 0: self.dy *= -1 # 천장 반사

    def check_collision(self, win_y):
        """공의 바닥이 당첨 존(win_y)에 닿았는지 판정"""
        if self.is_captured: return False
        pos = self.canvas.coords(self.oval)
        if pos[3] >= win_y:
            self.is_captured = True
            return True
        return False

# --- 2. [LottoStorage 클래스] : 데이터 저장 및 랜덤 조회(CRUD - R/S) ---
class LottoStorage:
    def __init__(self):
        self.records = []

    def save_result(self, nums):
        data = {"id": len(self.records) + 1, "nums": nums, "time": time.strftime("%H:%M:%S")}
        self.records.append(data)
        return data

    def get_random_5(self):
        # 저장된 전체 데이터 중 랜덤으로 최대 5개만 골라냄 (이단적 조회)
        if not self.records: return []
        count = min(len(self.records), 5)
        return random.sample(self.records, count)

# --- 3. [LottoController 클래스] : 버튼 인터페이스 전담 UI ---
class LottoController(tk.Frame):
    def __init__(self, master, draw_cmd, view_cmd):
        super().__init__(master, bg="#333", pady=10)
        self.draw_btn = tk.Button(self, text="6/45 공 투입 (Create)", command=draw_cmd, width=20, height=2)
        self.draw_btn.pack(side="left", padx=20)
        
        self.view_btn = tk.Button(self, text="무작위 5개 조회 (Read)", command=view_cmd, width=20, height=2)
        self.view_btn.pack(side="left", padx=20)

# --- 4. [LottoApp 클래스] : 렌더링, 애니메이션 루프 및 팝업 제어 ---
class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("6/45 진짜 물리 CRUD")
        self.root.geometry("600x650")
        
        self.storage = LottoStorage()
        self.balls = []
        self.winners = []
        self.is_animating = False

        # 캔버스 영역
        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack(fill="both", expand=True)
        
        # 당첨 존(Winning Zone) 시각화
        self.win_y = 450
        self.canvas.create_rectangle(0, self.win_y, 600, 500, fill="#FFD700", outline="")
        self.canvas.create_text(300, 475, text="WINNING ZONE (닿는 순서대로 채택)", font=("Arial", 12, "bold"))

        # 컨트롤러 배치
        self.controller = LottoController(root, self.start_draw, self.show_records)
        self.controller.pack(fill="x", side="bottom")

    def start_draw(self):
        if self.is_animating: return
        self.canvas.delete("ball")
        self.balls = []
        self.winners = []
        self.is_animating = True
        
        # 45개 공 생성
        for i in range(1, 46):
            b = LottoBall(self.canvas, i, random.randint(50, 550), random.randint(20, 100))
            self.balls.append(b)
        
        self.run_physics()

    def run_physics(self):
        if not self.is_animating: return
        
        for b in self.balls:
            b.move(600, self.win_y)
            # 물리적 충돌 판정: 당첨 존에 먼저 닿는 6개만 선발
            if len(self.winners) < 6 and b.check_collision(self.win_y):
                self.winners.append(b.number)
                self.canvas.itemconfig(b.oval, outline="red", width=3) # 당첨 표시

        if len(self.winners) < 6:
            self.root.after(20, self.run_physics)
        else:
            self.is_animating = False
            self.root.after(500, self.ask_save_or_delete)

    def ask_save_or_delete(self):
        """메인 창 정중앙에 뜨는 모달 팝업"""
        pop = tk.Toplevel(self.root)
        pop.title("추첨 결과 처리")
        pop.transient(self.root)
        pop.grab_set() # 메인 창 조작 방지

        # 위치 계산
        w, h = 300, 150
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - (w//2)
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - (h//2)
        pop.geometry(f"{w}x{h}+{x}+{y}")

        res = sorted(self.winners)
        tk.Label(pop, text=f"추첨 결과: {res}\n저장하시겠습니까?", font=("Arial", 11)).pack(pady=20)
        
        btn_f = tk.Frame(pop)
        btn_f.pack()
        tk.Button(btn_f, text="저장 (Save)", width=10, command=lambda: [self.storage.save_result(res), pop.destroy()]).pack(side="left", padx=10)
        tk.Button(btn_f, text="삭제 (Delete)", width=10, command=pop.destroy).pack(side="right", padx=10)

    def show_records(self):
        data = self.storage.get_random_5()
        view = tk.Toplevel(self.root)
        view.title("랜덤 조회 (Max 5)")
        
        # 위치 계산
        w, h = 400, 300
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - (w//2)
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - (h//2)
        view.geometry(f"{w}x{h}+{x}+{y}")

        if not data:
            tk.Label(view, text="저장된 데이터가 없습니다.", pady=50).pack()
            return
        
        for r in data:
            tk.Label(view, text=f"[{r['id']}회차] {r['nums']} ({r['time']})", pady=5).pack()

# --- 5. [Main 실행부] ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LottoApp(root)
    root.mainloop()