# app.py
import tkinter as tk
import random
import common.config as cfg
from common.physics import Physics_Core
from lotto.ball import LottoBall
from lotto.storage import LottoStorage
from lotto.controller import Controller
from lotto.result_popup import LottoResultPopup
from lotto.record_popup import RecordViewPopup

class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("모든 것이 랜덤인 로또") # 제목
        self.root.geometry(f"{cfg.WINDOW_WIDTH}x{cfg.WINDOW_HEIGHT}")          # 창 크기 결정

        # 1. 물리 엔진 및 저장소 초기화
        self.physics_core = Physics_Core(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT) 
        self.storage = LottoStorage()              # 앱을 실행하면서, 저장소도 초기화
        
        # 2. UI 레이아웃
        self.canvas = tk.Canvas(root, bg="white") # 그릴 캔버스 소환
        self.canvas.pack(fill="both", expand=True) # root랑 canvas는 pack으로 붙여줘야 동작
        
        # # 3. 당첨 영역 설정(하단)
        # * 동적 생성시에는 하드코딩하면 이상현상 생기니 생성자 초기화 하면 안됨.
        # self.win_y = 450 # (0~450은 물리엔진동작 영역, 450~600은 당첨 영역)
        # self.canvas.create_rectangle(0, self.win_y, 600, 500, fill="#FFD700", outline="") 
        # # 하단에 닿는 영역(사각형) -> 닿으면 공이 선택되도록 영역
        
        # 4. 버튼(하단) : Controller를 호출
        self.controller = Controller(root, on_draw=self.start_draw, on_read=self.show_records) 
                                            # 버튼이 늘어나면, 여기도 매개변수를 추가해줘야함. 
                                            # 여러 곳에서 수정해야 하는 문제 아닌가?
        self.controller.pack(fill="x", side="bottom")

        # 5. 상태 관리 리스트
        self.active_balls = []    # 활성화된 공이 담기는 리스트
        self.winners = []         # 선택된 공만 담기는 리스트
        self.is_animating = False # 기본값은 비활성화

    def sync_dimensions(self):
        """
        물리 엔진의 벽(height)과 시각적 영역(Rectangle)을 
        한 곳에서 동기화하여 데이터 정합성을 유지
        """
        self.root.update_idletasks() # 실제 렌더링 수치 확정
        curr_w = self.canvas.winfo_width()
        curr_h = self.canvas.winfo_height()
        
        # 1. 비율에 따른 당첨 기준선(Floor) 계산
        self.win_y = int(curr_h * cfg.WIN_ZONE_RATIO) 
        
        # 2. 물리 엔진의 경계를 현재 캔버스 크기에 맞춤
        self.physics_core.width = curr_w
        self.physics_core.height = self.win_y
        
        # 3. 시각적 당첨 영역 재배치 (기존 것을 지우고 새로 그려 위치 오차 방지)
        self.canvas.delete("win_zone")
        self.canvas.create_rectangle(0, self.win_y, curr_w, curr_h, 
                                     fill="#FFD700", outline="", tags="win_zone")
        self.canvas.tag_lower("win_zone") # 공 뒤로 보냄
        
        return curr_w    

    def start_draw(self):
        if self.is_animating: return # 애니메이션이 활성화 되어 있으면, 동작하지 마라.
        
        # * 창 너비를 동적으로 가져오는 것을 여기서 해야함 
        width = self.sync_dimensions()
        self.canvas.delete("ball") # 기존 공 제거
        self.winners = []          # 빈 리스트로 초기화
        
        # [Create] 공 객체 생성 및 관리 리스트 추가
        # 볼 객체는 스스로를 캔버스에 그리지만, 제어권은 active_balls가 가짐
        for i in range(1, 46): # 1번부터 45번까지 
            x = random.randint(50, width - 50)   # 좌표 랜덤 할당
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
            # self.storage.save(self.winners) # 저장하는 로직이 있어서 poup에서 결정을 못함 -> 저장을 팝업에서 할 수 있게 바꿔야 함.
            self.pop_up() # 500ms이후에, 팝업을 띄운다. -> # 지연에 의해서 reset된 빈값을 반환해서 root.after 삭제
            self.reset_game() # 초기화 상태로 전이

    def handle_winner(self, ball): 
        self.winners.append(ball.number) # 선택된 공의 번호를 append
        # 시각적 피드백: 선택된 공에 빨강 아웃라인
        self.canvas.itemconfig(ball.oval, outline="red", width=3)

    def reset_game(self):
        """상태 초기화(Reset): 다음 드로우를 위한 준비"""
        self.winners = []
        self.active_balls = []
        self.canvas.delete("ball")

    def pop_up(self):
        # 1. 확정된 번호를 가져옴
        selected_numbers = sorted(self.winners)
        LottoResultPopup(self.root, selected_numbers, self.storage.save)

        # print(f"최종 당첨 번호 표출: {selected_numbers}")

    def show_records(self):
        """데이터 대신 storage 객체 자체를 넘겨 조작 가능하게 함"""
        RecordViewPopup(self.root, self.storage)