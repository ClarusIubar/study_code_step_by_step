
from datetime import datetime

class LottoStorage:
    def __init__(self):
        self.data = []

    def save(self, numbers):
        """
        데이터 생성 (Create)
        WORM 정책에 따라 한 번 생성된 ID와 번호는 수정할 수 없음.
        """
        # Auto Increment: 현재 리스트 길이를 기반으로 순차적 ID 부여
        new_id = len(self.data) + 1
        
        record = {
            "id": new_id,                   # 시스템 식별용 (1, 2, 3...)
            "numbers": sorted(numbers),     # 로또 번호 집합 (정렬하여 저장)
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 출력용 날짜
        }
        
        self.data.append(record)
        print(f"[Storage] 데이터 저장 완료: ID {new_id}")
        return record

    def read_all(self):
        """데이터 조회 (Read): 전체 기록 반환"""
        return self.data

    def delete_by_id(self, selected_id):
        """
        데이터 삭제 (Delete)
        사용자가 인터페이스에서 '명시적으로 선택한' selected_id를 인자로 받습니다.
        """
        before_count = len(self.data)
        
        # 사용자가 고른 ID(selected_id)와 일치하지 않는 기록들만 필터링하여 
        # 새로운 리스트를 만듭니다. 결과적으로 사용자가 선택한 그 아이디만 소멸됩니다.
        self.data = [record for record in self.data if record['id'] != selected_id]
        
        # 삭제 성공 여부 반환 (데이터 개수가 줄어들었다면 성공)
        return len(self.data) < before_count

