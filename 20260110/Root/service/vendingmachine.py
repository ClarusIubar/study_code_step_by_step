import json
from domain.product import Product
from domain.memo import Memo
from repository.repository import InventoryRepository

class VendingMachineService:
    def __init__(self, json_data: str):
        self.balance = 0
        self.total_revenue = 0
        self.payment_locked = None 
        self.products = InventoryRepository[Product]()
        self.memos = InventoryRepository[Memo]()
        self._init_memos()
        self._load(json_data)

    def _load(self, json_data: str):
        try:
            items = Product.from_auto(json.loads(json_data))
            if isinstance(items, dict):
                for p in items.values(): self.products.save(p)
        except Exception as e:
            print(f"Data Load Error: {e}")

    def _init_memos(self):
        for i in range(1, 10): self.memos.save(Memo(id=i, title=""))

    def insert_cash(self, amount: int):
        """현금 투입: 카드 결제 중 차단"""
        if self.payment_locked == "CARD":
            return False, "카드 결제 중에는 현금을 투입할 수 없습니다."
        self.balance += amount
        self.payment_locked = "CASH"
        return True, f"{amount}원 투입됨"

    def tag_card(self):
        """카드 태그: 현금 투입 중 차단"""
        if self.payment_locked == "CASH":
            return False, "현금이 투입된 상태에서는 카드를 사용할 수 없습니다."
        self.payment_locked = "CARD"
        self.balance = 20000 # 20260109 규격
        return True, "카드 인증 성공 (잔액 20,000원 설정)"

    def purchase(self, p_id: int):
        p = self.products.find_by_id(p_id)
        if not p: return None, "번호 오류"
        if p.stock <= 0: return None, "품절된 상품입니다."
        if self.balance < p.price: return None, "잔액 부족"
        
        success, msg = p.process_sell(1)
        if success: 
            self.balance -= p.price
            self.total_revenue += p.price # [추가] 매출액 누적
        return p, msg

    def reset_system(self):
        """시스템 초기화 및 잔액 반환"""
        change = self.balance
        self.balance = 0
        self.payment_locked = None
        return change
    

    # [추가] 관리자 기능: 개별 보충
    def refill_one(self, p_id: int):
        p = self.products.find_by_id(p_id)
        if not p: return False, "상품 없음"
        if p.stock >= 10: return False, "이미 가득 찼습니다."
        p.stock += 1
        return True, f"{p.name} 보충 완료 (현재: {p.stock})"

    # [추가] 관리자 기능: 수익금 회수
    def collect_revenue(self):
        amount = self.total_revenue
        self.total_revenue = 0
        return amount