from datetime import datetime

class AcidRainStorage:
    def __init__(self):
        self.data = []
        self.last_id = 0

    def save_score(self, score):
        self.last_id += 1
        record = {
            "id": self.last_id,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data.append(record)
        return record

    def read_all(self):
        # 점수 높은 순서로 정렬
        return sorted(self.data, key=lambda x: x['score'], reverse=True)