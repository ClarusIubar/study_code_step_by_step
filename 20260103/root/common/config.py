
class WindowConfig:
    WIDTH, HEIGHT, WIN_ZONE_RATIO = 600, 650, 0.85

class PhysicsConfig:
    FRAME_RATE_MS, BOUNCE_FACTOR = 15, 0.7

class LottoConfig:
    GRAVITY, BALL_RADIUS = 0.2, 12
    COLORS = {"yellow": "#fbc400", "blue": "#69cfff", "red": "#ff7272", "gray": "#aaaaaa", "green": "#b0d840"}

class AcidRainConfig:
    GRAVITY, LIFE = 0.005, 5
    WORD_RADIUS = 25
    
    SPEED_X_RANGE = (-0.5, 0.5) # 좌우 흔들림 범위
    SPEED_Y_RANGE = (0.8, 1.5)  # 하강 속도 범위
    
    SPAWN_INITIAL_MS, SPAWN_MIN_MS, LEVEL_UP_MS = 1000, 400, 60000
    SCORES = {2: 10, 3: 15, 4: 20}

class PopupConfig:
    RESULT_SIZE, RECORD_SIZE, CONFIRM_SIZE = (300, 180), (450, 350), (280, 130)