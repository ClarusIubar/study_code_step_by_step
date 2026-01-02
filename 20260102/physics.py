
class Physics_Core:
    def __init__(self, temp):
        self.temp = temp

    # 충돌 연산
    def collision(self):
        return
    # 볼 끼리 충돌하면 속도를 변환하여 튕겨나가는 효과를 일으킴.

    # 중력 연산
    def gravity(self):
        return
    # 아래로 자연스럽게 이동하게 만드는 모멘텀.

    # 벽면 제한
    def wall_limit(self):
        return
    # 이전에 공이 튕겼을 때, 화면 밖으로 나가지 않도록 제한.
    # 필요 : canvas.WIDTH, canvas.HEIGHT -> boundary
    # * collision을 사용해서 연산해야 하는가? 아니면 position만 알면 동작하도록 분리?