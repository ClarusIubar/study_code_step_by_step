
class WindowConfig:
    WIDTH, HEIGHT, WIN_ZONE_RATIO = 600, 650, 0.85

class PhysicsConfig:
    FRAME_RATE_MS, BOUNCE_FACTOR = 15, 0.7

class LottoConfig:
    GRAVITY, BALL_RADIUS = 0.2, 12
    COLORS = {
        "yellow": "#fbc400", "blue": "#69cfff", "red": "#ff7272", 
        "gray": "#aaaaaa", "green": "#b0d840"
    }

class AcidRainConfig:
    class Physics:
        GRAVITY = 0.005
        WORD_RADIUS = 25
        SPEED_X = (-0.3, 0.3)
        SPEED_Y = (0.8, 1.3)
        
    class Rules:
        LIFE = 5
        LEVEL_UP_MS = 20000 
        SPAWN_MS = (1500, 500) # (초기값, 최소값)
        
    class Assets:
        DATA = {
            2: {"score": 10, "color": "#fbc400"},
            3: {"score": 15, "color": "#69cfff"},
            4: {"score": 20, "color": "#ff7272"}
        }

class PopupConfig:
    RESULT_SIZE, RECORD_SIZE, CONFIRM_SIZE = (300, 180), (450, 350), (280, 130)