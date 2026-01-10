import json
from domain.product import Product
from domain.memo import Memo
from repository.repository import VMRepository, SmartQuerySet

class VendingMachineService:
    def __init__(self, json_data: str):
        self.balance = 0
        self.total_revenue = 0
        self.payment_locked = None
        self._repository = VMRepository()
        self._setup(json_data)

    def _setup(self, json_data: str):
        # 1. 초기 데이터 로드 (맵 구조 수용)
        try:
            items = Product.from_auto(json.loads(json_data))
            if isinstance(items, dict):
                for p in items.values(): self._repository.save(p)
        except: pass
        
        for i in range(1, 10): self._repository.save(Memo(id=i, title=""))

        # 2. 영속성 데이터 복구
        persisted = self._repository.load_persistence()
        if persisted:
            self.total_revenue = persisted.get("total_revenue", 0)
            entities = persisted.get("entities", {})
            for p_data in entities.get("Product", {}).values():
                self._repository.save(Product(**p_data))
            for m_data in entities.get("Memo", {}).values():
                self._repository.save(Memo(**m_data))

    @property
    def products(self) -> SmartQuerySet[Product]:
        return SmartQuerySet(self._repository.get_all(Product))

    @property
    def memos(self) -> SmartQuerySet[Memo]:
        return SmartQuerySet(self._repository.get_all(Memo))

    def purchase(self, p_id: int):
        p = self._repository.find_by_id(Product, p_id)
        if not p: return None, "번호 오류"
        if p.stock <= 0: return None, "품절 상품"
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
            p.stock += 1
            self._repository.persist(self.total_revenue)
            return True, f"{p.name} 보충 완료"
        return False, "보충 불가"

    def collect_revenue(self):
        amount = self.total_revenue
        self.total_revenue = 0
        self._repository.persist(self.total_revenue)
        return amount

    def save_state(self):
        self._repository.persist(self.total_revenue)

    def insert_cash(self, amount: int):
        if self.payment_locked == "CARD": return False, "차단"
        self.balance += amount; self.payment_locked = "CASH"
        return True, f"{amount}원 투입됨"

    def tag_card(self):
        if self.payment_locked == "CASH": return False, "차단"
        self.payment_locked = "CARD"; self.balance = 20000
        return True, "카드 인증 성공"

    def reset_system(self):
        change = self.balance; self.balance = 0; self.payment_locked = None
        return change