import tkinter as tk
import heapq
import time
import random

# 1. 데이터 에셋 (물리 정보만 보유)
class Ball:
    def __init__(self, bid, x, y, vx, vy, r):
        self.bid = bid
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.r = r
        self.coll_count = 0

# 2. 사건 기반 물리 엔진 (이벤트 예측 및 강제 경계 보정)
class EventEngine:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.pq = []
        self.now = 0.0

    def predict(self, a, balls):
        if a is None: return
        
        # 수평/수직 벽 충돌 시간 계산
        if a.vx > 0:
            dt = (self.width - a.r - a.x) / a.vx
            heapq.heappush(self.pq, (self.now + dt, id(a), a, None, a.coll_count, 0))
        elif a.vx < 0:
            dt = (a.r - a.x) / a.vx
            heapq.heappush(self.pq, (self.now + dt, id(a), a, None, a.coll_count, 0))
            
        if a.vy > 0:
            dt = (self.height - a.r - a.y) / a.vy
            heapq.heappush(self.pq, (self.now + dt, id(a), None, a, 0, a.coll_count))
        elif a.vy < 0:
            dt = (a.r - a.y) / a.vy
            heapq.heappush(self.pq, (self.now + dt, id(a), None, a, 0, a.coll_count))

        # 공끼리 충돌 예측 (수학적 근의 공식)
        # 1000개일 때 이 부분은 초기 1회만 고통스럽고, 이후엔 충돌 공만 재계산함
        for b in balls:
            if a == b: continue
            dt = self.get_collision_time(a, b)
            if dt > 0:
                heapq.heappush(self.pq, (self.now + dt, id(a), a, b, a.coll_count, b.coll_count))

    def get_collision_time(self, a, b):
        dx, dy = b.x - a.x, b.y - a.y
        dvx, dvy = b.vx - a.vx, b.vy - a.vy
        dvdr = dx*dvx + dy*dvy
        if dvdr >= 0: return -1
        dvdv = dvx**2 + dvy**2
        drdr = dx**2 + dy**2
        sigma = a.r + b.r
        d = (dvdr**2) - dvdv * (drdr - sigma**2)
        if d < 0: return -1
        return -(dvdr + d**0.5) / dvdv

    def update(self, balls, dt):
        end_time = self.now + dt
        
        while self.pq and self.pq[0][0] <= end_time:
            t, _, a, b, ca, cb = heapq.heappop(self.pq)
            if (a and a.coll_count != ca) or (b and b.coll_count != cb): continue

            move_dt = t - self.now
            for ball in balls:
                ball.x += ball.vx * move_dt
                ball.y += ball.vy * move_dt
            self.now = t

            if a and b: # 공-공 충돌
                dvx, dvy = b.vx - a.vx, b.vy - a.vy
                dx, dy = b.x - a.x, b.y - a.y
                dist = a.r + b.r
                j = (dvx*dx + dvy*dy) / dist
                jx, jy = j * dx / dist, j * dy / dist
                a.vx += jx; a.vy += jy; b.vx -= jx; b.vy -= jy
                a.coll_count += 1; b.coll_count += 1
                self.predict(a, balls); self.predict(b, balls)
            elif a: # X벽
                a.vx *= -1; a.coll_count += 1; self.predict(a, balls)
            elif b: # Y벽
                b.vy *= -1; b.coll_count += 1; self.predict(b, balls)

        remaining = end_time - self.now
        for ball in balls:
            ball.x += ball.vx * remaining
            ball.y += ball.vy * remaining
            # 해석 공간 이탈 강제 방지 (Clamping)
            if ball.x < ball.r: ball.x = ball.r; ball.vx = abs(ball.vx)
            elif ball.x > self.width - ball.r: ball.x = self.width - ball.r; ball.vx = -abs(ball.vx)
            if ball.y < ball.r: ball.y = ball.r; ball.vy = abs(ball.vy)
            elif ball.y > self.height - ball.r: ball.y = self.height - ball.r; ball.vy = -abs(ball.vy)
            
        self.now = end_time

# 3. 통합 실행부
class Simulation:
    def __init__(self, count=1000):
        self.root = tk.Tk()
        self.w, self.h = 800, 600
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, bg='black')
        self.canvas.pack()
        self.engine = EventEngine(self.w, self.h)
        self.balls = []
        self.ball_items = []

        # 공 생성 (겹치지 않게 생성하는 로직은 생략하여 초기 겹침이 있을 수 있음)
        for i in range(count):
            r = 3
            bx = random.randint(r, self.w-r)
            by = random.randint(r, self.h-r)
            b = Ball(i, bx, by, random.uniform(-3, 3), random.uniform(-3, 3), r)
            self.balls.append(b)
            self.ball_items.append(self.canvas.create_oval(0,0,0,0, fill='cyan', outline=''))
        
        # 초기 예측 (1000개이므로 최초 실행 시 약간의 멈춤이 있을 수 있음)
        print("초기 물리 예측 중...")
        for b in self.balls:
            self.engine.predict(b, self.balls)
        print("시뮬레이션 시작")

    def animate(self):
        start_time = time.time()
        
        # 물리 업데이트 (내부 시간 배율 0.5로 설정하여 안정성 확보)
        self.engine.update(self.balls, 0.5)
        
        # 렌더링 (Tkinter Canvas 갱신)
        for i, b in enumerate(self.balls):
            self.canvas.coords(self.ball_items[i], b.x-b.r, b.y-b.r, b.x+b.r, b.y+b.r)
        
        # 성능 표시
        calc_duration = time.time() - start_time
        self.root.title(f"Balls: {len(self.balls)} | Update: {calc_duration:.4f}s")
        self.root.after(10, self.animate)

if __name__ == "__main__":
    app = Simulation(1000)
    app.animate()
    app.root.mainloop()