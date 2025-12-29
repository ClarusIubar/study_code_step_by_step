import tkinter as tk

class LangtonsAnt:
    def __init__(self, root):
        self.root = root
        self.root.title("Langton's Ant Simulator")
        
        # 설정값
        self.grid_size = 60  
        self.cell_size = 10  
        self.delay = 100     
        self.running = True
        
        self.canvas = tk.Canvas(root, width=self.grid_size*self.cell_size, 
                                height=self.grid_size*self.cell_size, bg="white")
        self.canvas.pack()
        
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        self.ant_x = self.grid_size // 2
        self.ant_y = self.grid_size // 2
        self.direction = 0 
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        # mx=5를 padx=5로 수정함
        tk.Button(btn_frame, text="느리게", command=lambda: self.set_speed(300)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="보통", command=lambda: self.set_speed(100)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="빠르게", command=lambda: self.set_speed(10)).pack(side=tk.LEFT, padx=5)
        
        self.update()

    def set_speed(self, speed):
        self.delay = speed

    def update(self):
        if not self.running:
            return

        # 벽 충돌 체크
        if not (0 <= self.ant_x < self.grid_size and 0 <= self.ant_y < self.grid_size):
            print("벽에 부딪혔습니다! 정지합니다.")
            self.running = False
            return

        current_color = self.grid[self.ant_y][self.ant_x]

        if current_color == 0:  # 흰색 -> 검은색
            self.direction = (self.direction + 1) % 4
            self.grid[self.ant_y][self.ant_x] = 1
            color_str = "black"
        else:  # 검은색 -> 흰색
            self.direction = (self.direction - 1) % 4
            self.grid[self.ant_y][self.ant_x] = 0
            color_str = "white"

        x1, y1 = self.ant_x * self.cell_size, self.ant_y * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_str, outline="gray")

        if self.direction == 0: self.ant_y -= 1     
        elif self.direction == 1: self.ant_x += 1   
        elif self.direction == 2: self.ant_y += 1   
        elif self.direction == 3: self.ant_x -= 1   

        self.root.after(self.delay, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = LangtonsAnt(root)
    root.mainloop()