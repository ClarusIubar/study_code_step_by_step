import json
from domain.product import Product
from domain.memo import Memo
from repository.repository import VMRepository, SmartQuerySet

class VendingMachineService:
    def __init__(self, json_data: str):
        self.balance = 0
        self.total_revenue = 0
        self.payment_locked = None # None, "CASH", "CARD"
        self._repository = VMRepository()
        self._setup(json_data)

    def _setup(self, json_data: str):
        try:
            items = Product.from_auto(json.loads(json_data))
            if isinstance(items, dict):
                for p in items.values(): self._repository.save(p)
        except: pass
        for i in range(1, 10): self._repository.save(Memo(id=i, title=""))
        persisted = self._repository.load_persistence()
        if persisted:
            self.total_revenue = persisted.get("total_revenue", 0)
            entities = persisted.get("entities", {})
            for d in entities.get("Product", {}).values(): self._repository.save(Product(**d))
            for d in entities.get("Memo", {}).values(): self._repository.save(Memo(**d))

    @property
    def products(self) -> SmartQuerySet[Product]: return SmartQuerySet(self._repository.get_all(Product))
    @property
    def memos(self) -> SmartQuerySet[Memo]: return SmartQuerySet(self._repository.get_all(Memo))

    def purchase(self, p_id: int):
        p = self._repository.find_by_id(Product, p_id)
        if not p: return None, "번호 오류"
        if p.stock <= 0: return None, "품절된 상품"
        if self.balance < p.price: return None, "잔액 부족"
        
        success, msg = p.process_sell(1)
        if success:
            self.balance -= p.price
            self.total_revenue += p.price
            self._repository.persist(self.total_revenue)
        return p, msg

    def refill_one(self, p_id: int):
        p = self._repository.find_by_id(Product, p_id)
        if p and p.stock < 10:
            p.stock += 1; self._repository.persist(self.total_revenue)
            return True, f"{p.name} 보충 완료"
        return False, "보충 불가"

    def collect_revenue(self):
        amount = self.total_revenue; self.total_revenue = 0; self._repository.persist(self.total_revenue)
        return amount

    def insert_cash(self, amount: int):
        # [수정] 카드 결제 중 현금 투입 원천 차단
        if self.payment_locked == "CARD": 
            return False, "카드 결제 중에는 현금을 투입할 수 없습니다."
        self.balance += amount
        self.payment_locked = "CASH"
        return True, f"{amount}원 투입 완료"

    def tag_card(self):
        # [수정] 현금 투입 중 카드 태그 원천 차단
        if self.payment_locked == "CASH": 
            return False, "현금이 투입된 상태입니다."
        self.payment_locked = "CARD"
        self.balance = 20000
        return True, "카드 인증 성공"

    def reset_system(self):
        change = self.balance
        self.balance = 0
        self.payment_locked = None
        return change

    def save_state(self): self._repository.persist(self.total_revenue)