from enum import Enum

class Position(str, Enum):
    CASHIER = "캐셔"
    INVENTORY = "재고관리"
    MANAGER = "매니저"
    DISPLAY = "진열"
    DELIVERY = "배달"
    SUB_MANAGER = "부매니저"

class Shift(str, Enum):
    MORNING = "오전"
    AFTERNOON = "오후"
    NIGHT = "야간"
    FULL_TIME = "풀타임"

class Category(str, Enum):
    NOODLE = "라면"
    BEVERAGE = "음료"
    SNACK = "과자"
    RETORT = "간편식"