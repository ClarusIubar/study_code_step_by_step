from dataclasses import dataclass
from typing import List, Dict, Optional

# [1] 설정 영역: 정책이나 시스템 설정 (여기만 고치면 로직 전체가 바뀜)
SETTINGS = {
    "STORE_NAME": "욱재마트",
    "MAX_PURCHASE_LIMIT": 3,
    "EXIT_COMMAND": "q"
}

# [2] 데이터 모델: 상품이라는 객체의 규격 정의
@dataclass
class Item:
    name: str
    price: int
    count: int

    @property
    def subtotal(self) -> int:
        """소계 계산의 책임을 객체 내부로 가져옴"""
        return self.price * self.count

# [3] 비즈니스 로직: 마트 운영 시스템
class MartSystem:
    def __init__(self, products_data: List[Dict]):
        # 원본 리스트를 조회용 딕셔너리로 인덱싱 (이중 포문 제거)
        self.inventory = {p['name']: p['price'] for p in products_data}
        self.cart: List[Item] = []

    def _get_valid_input(self, index: int) -> Optional[Item]:
        """검색대 역할: 유효한 입력만 통과시켜 객체로 반환"""
        exit_cmd = SETTINGS["EXIT_COMMAND"]
        
        while True:
            name = input(f"[{index}] 상품명 (종료: {exit_cmd}) : ").strip()
            if name.lower() == exit_cmd:
                return None
            
            if name not in self.inventory:
                print(f"  ❌ '{name}'은(는) 매장에 없는 상품입니다.")
                continue
            
            count_str = input(f"    수량 입력 : ").strip()
            if count_str.isdigit() and int(count_str) > 0:
                return Item(
                    name=name, 
                    price=self.inventory[name], 
                    count=int(count_str)
                )
            
            print("  ❌ 수량은 1 이상의 숫자로 입력해주세요.")

    def run(self):
        """메인 실행 루프"""
        print(f"\n✨ {SETTINGS['STORE_NAME']} 키오스크를 시작합니다.")
        
        for i in range(1, SETTINGS["MAX_PURCHASE_LIMIT"] + 1):
            item = self._get_valid_input(i)
            if not item:  # 'q'를 누르면 중도 종료
                break
            self.cart.append(item)
        
        self.print_receipt()

    def print_receipt(self):
        """출력 책임 분리"""
        if not self.cart:
            return print("\n구매 내역이 없습니다. 이용해주셔서 감사합니다.")

        print(f"\n{'='*30}")
        print(f"       {SETTINGS['STORE_NAME']} 영수증")
        print(f"{'='*30}")
        
        for item in self.cart:
            # f-string 포맷팅을 사용해 가독성 확보
            print(f"{item.name:10} | {item.count:3}개 | {item.subtotal:10,}원")
        
        total = sum(i.subtotal for i in self.cart)
        print(f"{'-'*30}")
        print(f"총 합계:{total:21,}원")
        print(f"{'='*30}")
        print("감사합니다! 또 오세요~")

# --- 메인 실행부 ---
if __name__ == "__main__":
    # 원본 데이터 (리스트 형태)
    products = [
        {"name": "신라면", "price": 1350, "stock": 50, "category": "라면"},
        {"name": "진라면", "price": 1200, "stock": 45, "category": "라면"},
        {"name": "삼다수", "price": 1000, "stock": 100, "category": "음료"},
        {"name": "코카콜라", "price": 1800, "stock": 30, "category": "음료"},
        {"name": "새우깡", "price": 1500, "stock": 25, "category": "과자"},
        {"name": "포카칩", "price": 1700, "stock": 20, "category": "과자"},
        {"name": "바나나우유", "price": 1400, "stock": 40, "category": "음료"},
        {"name": "삼각김밥", "price": 1200, "stock": 15, "category": "간편식"},
        {"name": "컵라면", "price": 1100, "stock": 60, "category": "라면"},
        {"name": "초코파이", "price": 4500, "stock": 18, "category": "과자"}
    ]

    # 시스템 가동
    mart = MartSystem(products)
    mart.run()