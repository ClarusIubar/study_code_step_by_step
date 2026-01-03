
class BaseBall:
    def __init__(self, canvas, radius, dx, dy, x, y):
        self.canvas = canvas
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.oval = None
        self.text = None

    def get_pos(self):
        """엔진이 참조하는 좌표 인터페이스"""
        coords = self.canvas.coords(self.oval)
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    def move_by(self, tx, ty):
        """엔진이 명령하는 이동 인터페이스"""
        self.canvas.move(self.oval, tx, ty)
        if self.text: self.canvas.move(self.text, tx, ty)

    def update(self):
        """매 프레임 이동 로직"""
        self.move_by(self.dx, self.dy)

    def check_collision(self, win_y):
        """충돌 판정 인터페이스"""
        _, y = self.get_pos()
        return y + self.radius >= win_y