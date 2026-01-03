# config.py

# 1. 창 및 레이아웃 설정
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
WIN_ZONE_RATIO = 0.85  # 전체 높이 대비 당첨 영역 시작 비율

# 2. 물리 엔진 상수
GRAVITY = 0.2
BOUNCE_FACTOR = 0.7
FRAME_RATE_MS = 15

# 3. 볼 관련 설정
BALL_RADIUS = 12
BALL_COLORS = {
    "yellow": "#fbc400",  # 1-10
    "blue": "#69cfff",    # 11-20
    "red": "#ff7272",     # 21-30
    "gray": "#aaaaaa",    # 31-40
    "green": "#b0d840"    # 41-45
}

# 4. 팝업 크기 설정
POPUP_RESULT_SIZE = (300, 180)
POPUP_RECORD_SIZE = (450, 350)
POPUP_CONFIRM_SIZE = (280, 130)