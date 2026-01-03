import math

## 수학적인 것은 위임하였음. 그러나 동작방식을 위해 파악은 해야함.
class Physics_Core:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def collision(self, objects):
        """
        볼끼리 충돌하면 속도를 변환하여 튕겨나가는 효과를 일으킴.
        엔진은 리스트 내 객체가 어떤 상태인지 모르며, 준수된 인터페이스만 사용함.
        """
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                obj1, obj2 = objects[i], objects[j]
                
                x1, y1 = obj1.get_pos() # x1, y1 좌표
                x2, y2 = obj2.get_pos() # x2, y2 좌표
                dx, dy = x2 - x1, y2 - y1 # x요소, y요소 diff
                dist = math.sqrt(dx**2 + dy**2) # 거리 계산 공식
                
                min_dist = obj1.radius + obj2.radius
                if 0 < dist < min_dist:
                    # 1. 위치 보정: 겹침(overlap) 해소
                    overlap = min_dist - dist
                    nx, ny = dx/dist, dy/dist # 법선 벡터
                    
                    obj1.move_by(-nx * overlap / 2, -ny * overlap / 2)
                    obj2.move_by( nx * overlap / 2,  ny * overlap / 2)

                    # 2. 속도 변환: 탄성 충돌 로직
                    p = (obj1.dx * nx 
                         + obj1.dy * ny 
                         - obj2.dx * nx 
                         - obj2.dy * ny)
                    obj1.dx -= p * nx
                    obj1.dy -= p * ny
                    obj2.dx += p * nx
                    obj2.dy += p * ny

    def gravity(self, obj, g=0.2):
        """아래로 자연스럽게 이동하게 만드는 모멘텀 적용."""
        obj.dy += g

    def wall_limit(self, obj, bounce=0.7):
        """
        화면 밖으로 나가지 않도록 제한.
        객체의 position과 boundary 정보만으로 독립적으로 동작함.
        """
        x, y = obj.get_pos()
        
        # 좌우 벽 충돌
        if x - obj.radius < 0:
            obj.dx = abs(obj.dx) * bounce
        elif x + obj.radius > self.width:
            obj.dx = -abs(obj.dx) * bounce
            
        # 천장 충돌 (화면 안으로 들어온 상태에서만 작동하도록 끼임 방지)
        if y - obj.radius < 0 and y > obj.radius:
            obj.dy = abs(obj.dy) * bounce