
import time
import random

class LottoStorage:
    def __init__(self):
        self.records = []
    def save(self, nums):
        self.records.append({"id": len(self.records)+1, "nums": nums, "time": time.strftime("%H:%M:%S")})
    def get_random_5(self):
        return random.sample(self.records, min(len(self.records), 5)) # 랜덤 조회