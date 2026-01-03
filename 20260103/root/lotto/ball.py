import random
import common.config as cfg

class LottoBall():
    def __init__(self, canvas, number, x, y):
        self.canvas = canvas
        self.number = number
        
        # 물리 엔진이 참조할 필수 인터페이스 속성
        self.radius = cfg.BALL_RADIUS
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(3, 6)
        
        # 시각적 요소 생성
        self.color = self._get_color(number) # 숫자 구간별로 색깔을 선택하는 로직
        self.oval = canvas.create_oval(x-self.radius, y-self.radius, 
                                       x+self.radius, y+self.radius, 
                                       fill=self.color, outline="black", tags="ball")
        self.text = canvas.create_text(x, y, text=str(number), 
                                       font=("Arial", 8, "bold"), tags="ball")

    # 볼 위치
    def get_pos(self):
        """현재 중심 좌표 반환 (엔진의 R 관점)"""
        # canvas.coords가 좌표를 기반으로 동작하는 메서드
        coords = self.canvas.coords(self.oval)
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    
    # 볼 색상
    # if조건에 따라서 볼의 색상을 다르게 함.
    # 실제 로또에서도 1~10, 11~20, 21~30, 31~40, 40~45까지 색이 다름.
    def _get_color(self, n):
        """[상수 주입] config의 색상 팔레트를 기반으로 번호대별 색상 할당"""
        colors = cfg.BALL_COLORS
        if n <= 10: return colors["yellow"]
        if n <= 20: return colors["blue"]
        if n <= 30: return colors["red"]
        if n <= 40: return colors["gray"]
        return colors["green"]

    def move_by(self, tx, ty):
        """엔진의 물리 연산 결과에 따라 실제 좌표 이동 (엔진의 U 관점)"""
        # 공과 숫자표시가 따로 놀지 않도록 변화량에 따라서 같이 적용되도록 움직여야 함.
        self.canvas.move(self.oval, tx, ty)
        self.canvas.move(self.text, tx, ty)

    def update(self):
        """매 프레임 자신의 속도(dx, dy)만큼 이동"""
        self.move_by(self.dx, self.dy) 
        # distance = velocity * time
        # x = dx*dt, y = dy*dt 
        # dt = 정해진 ms, frame(프로그램 내부 동작 시간까지 지금은 알 필요 없음.)

    def check_collision(self, win_y):
        """당첨 영역(y좌표) 도달 여부 확인"""
        _, y = self.get_pos() # y축 충돌로 결정되니까 좌표값을 가져와서,
        return y + self.radius >= win_y # 침범하면 충돌 판정 


# --- physics --- 

    # def get_pos(self):
    #     """현재 중심 좌표 반환 (엔진의 R 관점)"""
    #     # canvas.coords가 좌표를 기반으로 동작하는 메서드
    #     coords = self.canvas.coords(self.oval)
    #     return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    # def move_by(self, tx, ty):
    #     """엔진의 물리 연산 결과에 따라 실제 좌표 이동 (엔진의 U 관점)"""
    #     # 공과 숫자표시가 따로 놀지 않도록 변화량에 따라서 같이 적용되도록 움직여야 함.
    #     self.canvas.move(self.oval, tx, ty)
    #     self.canvas.move(self.text, tx, ty)

    # def update(self):
    #     """매 프레임 자신의 속도(dx, dy)만큼 이동"""
    #     self.move_by(self.dx, self.dy) 
    #     # distance = velocity * time
    #     # x = dx*dt, y = dy*dt 
    #     # dt = 정해진 ms, frame(프로그램 내부 동작 시간까지 지금은 알 필요 없음.)