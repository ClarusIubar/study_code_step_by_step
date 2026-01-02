
class LottoBall:
    def __init__(self, x, y, temp): # 생성자
        self.x = x
        self.y = y
        self.pos = temp

    # 볼 위치
    def position(self):
        return
    # position(pos) 2차원이니까, x,y가 필요함.
    # x1, y1 - x2, y2
    
    # 볼 색상
    def color(self):
        return
    # if조건에 따라서 볼의 색상을 다르게 함.
    # 실제 로또에서도 1~10, 11~20, 21~30, 31~40, 40~45까지 색이 다름.

    # 볼 움직임
    def move(self):
        return
    # x,y <- physics 연동.

    # 볼 충돌
    def collision(self):
        return
    # x,y끼리 좌표를 확인해서 속도를 변환.


# --- physics --- 

    def get_pos(self):
        """현재 중심 좌표 반환 (엔진의 R 관점)"""
        # canvas.coords가 좌표를 기반으로 동작하는 메서드
        coords = self.canvas.coords(self.oval)
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

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