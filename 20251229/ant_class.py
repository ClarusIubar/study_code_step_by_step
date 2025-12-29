import tkinter as tk

class SpeedController:
    """속도 데이터를 관리하고 조절 버튼을 생성하는 클래스"""
    def __init__(self, master):
        self.delay = 100
        self.frame = tk.Frame(master)
        self.frame.pack(pady=5)
        
        tk.Button(self.frame, text="x2 빠르게 (1/2 Delay)", command=self.speed_up).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame, text="x2 느리게 (x2 Delay)", command=self.speed_down).pack(side=tk.LEFT, padx=5)

    def speed_up(self):
        if self.delay > 1:
            self.delay //= 2
            print(f"현재 지연시간: {self.delay}ms")

    def speed_down(self):
        if self.delay < 2000:
            self.delay *= 2
            print(f"현재 지연시간: {self.delay}ms")

class Grid:
    """격자 데이터 관리 및 캔버스 드로잉 전담 클래스"""
    def __init__(self, canvas, size, cell_size):
        self.canvas = canvas
        self.size = size
        self.cell_size = cell_size
        # 0: 흰색, 1: 검은색
        self.data = [[0 for _ in range(size)] for _ in range(size)]

    def toggle_and_draw(self, x, y):
        """좌표의 상태를 반전시키고 사각형을 그림"""
        # 상태 변경 (0 -> 1, 1 -> 0)
        self.data[y][x] = 1 - self.data[y][x]
        
        # 색상 결정
        color = "black" if self.data[y][x] == 1 else "white"
        
        # 캔버스에 그리기
        x1, y1 = x * self.cell_size, y * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        
        return self.data[y][x]

class Ant:
    """개미의 위치, 방향 및 이동 로직 전담 클래스"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # 0:북, 1:동, 2:남, 3:서

    def turn_and_move(self, current_color_state):
        """현재 칸의 색상 상태에 따라 회전 후 이동"""
        # 랭턴의 개미 규칙: 
        # 흰색(0)이면 오른쪽(시계방향) 90도 회전
        # 검은색(1)이면 왼쪽(반시계방향) 90도 회전
        if current_color_state == 0:
            self.direction = (self.direction + 1) % 4
        else:
            self.direction = (self.direction - 1) % 4
            
        # 이동
        if self.direction == 0: self.y -= 1    # 북
        elif self.direction == 1: self.x += 1  # 동
        elif self.direction == 2: self.y += 1  # 남
        elif self.direction == 3: self.x -= 1  # 서

class App:
    """전체 시스템을 조립하고 메인 루프를 실행하는 클래스"""
    def __init__(self, root):
        self.root = root
        self.root.title("Langton's Ant - OOP Architecture")
        
        # 설정값
        GRID_SIZE = 250
        CELL_SIZE = 5
        
        # 컴포넌트 초기화
        self.canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE, bg="white")
        self.canvas.pack()
        
        self.grid = Grid(self.canvas, GRID_SIZE, CELL_SIZE)
        self.ant = Ant(GRID_SIZE // 2, GRID_SIZE // 2)
        self.controller = SpeedController(root)
        
        # 실행 시작
        self.update()

    def update(self):
        """시뮬레이션 한 단계 진행 루프"""
        # 1. 범위 체크 (벽 충돌)
        if 0 <= self.ant.x < self.grid.size and 0 <= self.ant.y < self.grid.size:
            # 2. 현재 칸 상태 변경 및 그리기
            new_state = self.grid.toggle_and_draw(self.ant.x, self.ant.y)
            # 3. 개미 이동 로직 수행
            self.ant.turn_and_move(new_state)
            # 4. 다음 루프 예약 (Controller에서 관리하는 delay 사용)
            self.root.after(self.controller.delay, self.update)
        else:
            print("개미가 경계를 벗어났습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()