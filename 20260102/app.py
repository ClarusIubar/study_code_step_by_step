# app.py
import tkinter as tk
import random
from physics import Physics_Core
from ball import LottoBall
from storage import LottoStorage
from controller import Controller

class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("모든 것이 랜덤인 로또") # 제목
        self.root.geometry("600x650")          # 창 크기 결정

        # 1. 물리 엔진 및 저장소 초기화
        self.physics_core = Physics_Core(600, 450) # TODO 위에 geometry랑 동기화 해야함. 하드 코딩 X
        self.storage = LottoStorage()              # 앱을 실행하면서, 저장소도 초기화
        
        # 2. UI 레이아웃
        self.canvas = tk.Canvas(root, width=600, height=500, bg="white") # 그릴 캔버스 소환
        self.canvas.pack(fill="both", expand=True) # root랑 canvas는 pack으로 붙여줘야 동작
        
        # 3. 당첨 영역 설정(하단)
        self.win_y = 450 # (0~450은 물리엔진동작 영역, 450~600은 당첨 영역)
        self.canvas.create_rectangle(0, self.win_y, 600, 500, fill="#FFD700", outline="") 
        # 하단에 닿는 영역(사각형) -> 닿으면 공이 선택되도록 영역
        
        # 4. 버튼(하단) : Controller를 호출
        self.controller = Controller(root, on_draw=self.start_draw)
        self.controller.pack(fill="x", side="bottom")

        # 5. 상태 관리 리스트
        self.active_balls = []    # 활성화된 공이 담기는 리스트
        self.winners = []         # 선택된 공만 담기는 리스트
        self.is_animating = False # 기본값은 비활성화

    def start_draw(self):
        if self.is_animating: return # 애니메이션이 활성화 되어 있으면, 동작하지 마라.
        
        self.canvas.delete("ball") # 기존 공 제거
        self.winners = []          # 빈 리스트로 초기화
        
        # [Create] 공 객체 생성 및 관리 리스트 추가
        # 볼 객체는 스스로를 캔버스에 그리지만, 제어권은 active_balls가 가짐
        for i in range(1, 46): # 1번부터 45번까지 
            x = random.randint(50, 550)   # 좌표 랜덤 할당
            y = random.randint(-150, -30) # 좌표 랜덤 할당
            ball = LottoBall(self.canvas, i, x, y) # 캔버스에 번호, x좌표, y좌표 전달.
            self.active_balls.append(ball) # 활성화된 공을 리스트에 추가
            
        self.is_animating = True # 애니메이션을 활성화
        self.run_physics()       # 물리 엔진 작동

    def run_physics(self):
        if not self.is_animating: return # 애니메이션이 활성화 되지 않으면, 아무것도 하지마라.

        # 1. 물리 엔진에게 현재 '유효한' 리스트만 전달 (위임)
        self.physics_core.collision(self.active_balls) # 활성화된 공
        
        for ball in self.active_balls[:]:
            self.physics_core.gravity(ball)    # 중력 적용(아래로 이동하는 모멘텀)
            self.physics_core.wall_limit(ball) # 경계 체크(canvas밖으로 이탈을 막아야 함)
            ball.update()                      # 실제 좌표 반영
            
            # 2. 게임 규칙 판정 (App의 책임)
            if ball.check_collision(self.win_y): # 하단영역의 y좌표에 볼이 닿으면,
                if len(self.winners) < 6: # 5개까지는 활성화 상태, 6개면 작동하면 안됨. (6개까지 골라야 하니까)
                    self.handle_winner(ball) # 일반공을 선택된 공으로 변환하는 함수 호출
                
                # [상태 관리] 리스트에서 제거하여 물리 연산 대상에서 제외
                self.active_balls.remove(ball)

        # root.after(ms마다 동작하도록 loop)
        if len(self.winners) < 6: # 아직 공이 6개 선택이 안 된 동안에는,
            self.root.after(15, self.run_physics) # 15ms마다 계속 물리엔진을 호출
        else: # 공이 6개가 골라지면,
            self.is_animating = False  # 볼 애니메이션을 중지. 
            self.root.after(500, self.pop_up) # 500ms이후에, 팝업을 띄운다. 

    def handle_winner(self, ball): 
        self.winners.append(ball.number) # 선택된 공의 번호를 append
        # 시각적 피드백: 선택된 공에 빨강 아웃라인
        self.canvas.itemconfig(ball.oval, outline="red", width=3)

    def pop_up(self):
        # 결과 저장 및 팝업 표출 (기존 로직 활용)
        selected_numbers = sorted(self.winners) # ASC기본
        # LottoResultPopup(self.root, selected_numbers, self.storage.save)
        print(f"최종 당첨 번호: {selected_numbers}")