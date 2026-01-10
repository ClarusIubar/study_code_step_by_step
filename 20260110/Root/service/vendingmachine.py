import json
from pyscript import window
from domain.product import Product
from domain.memo import Memo
from repository.repository import InventoryRepository

class VendingMachineService:
    STORAGE_KEY = "UKJAE_VM_DATA"

    def __init__(self, json_data: str):
        self.balance = 0
        self.total_revenue = 0
        self.payment_locked = None # CASH, CARD, None
        self.products = InventoryRepository[Product]()
        self.memos = InventoryRepository[Memo]()
        self._init_memos() # 메모 초기화 (기존 로직 엄수)
        self._load(json_data)
        self._load_from_storage() # 로컬 스토리지 데이터 복구

    def _save_to_storage(self):
        """매출 및 재고 상태를 로컬 스토리지에 저장 (욱재마트 규격)"""
        data = {
            "total_revenue": self.total_revenue,
            "stocks": {p.id: p.stock for p in self.products.get_all()}
        }
        window.localStorage.setItem(self.STORAGE_KEY, json.dumps(data))

    def _load_from_storage(self):
        """로컬 스토리지에서 데이터 복구"""
        raw = window.localStorage.getItem(self.STORAGE_KEY)
        if not raw: return
        try:
            data = json.loads(raw)
            self.total_revenue = data.get("total_revenue", 0)
            stocks = data.get("stocks", {})
            for pid, stock in stocks.items():
                p = self.products.find_by_id(int(pid))
                if p: p.stock = stock
        except: pass

    def _load(self, json_data: str):
        try:
            items = Product.from_auto(json.loads(json_data))
            if isinstance(items, dict):
                for p in items.values(): self.products.save(p)
        except Exception as e:
            print(f"Data Load Error: {e}")

    def _init_memos(self):
        """메모 초기화 원본 유지"""
        for i in range(1, 10): self.memos.save(Memo(id=i, title=""))

    def insert_cash(self, amount: int):
        if self.payment_locked == "CARD":
            return False, "카드 결제 중에는 현금을 투입할 수 없습니다."
        self.balance += amount
        self.payment_locked = "CASH"
        return True, f"{amount}원 투입됨"

    def tag_card(self):
        if self.payment_locked == "CASH":
            return False, "현금이 투입된 상태에서는 카드를 사용할 수 없습니다."
        self.payment_locked = "CARD"
        self.balance = 20000 
        return True, "카드 인증 성공 (잔액 20,000원 설정)"

    def purchase(self, p_id: int):
        p = self.products.find_by_id(p_id)
        if not p: return None, "번호 오류"
        if p.stock <= 0: return None, "품절된 상품입니다."
        if self.balance < p.price: return None, "잔액 부족"
        
        success, msg = p.process_sell(1)
        if success: 
            self.balance -= p.price
            self.total_revenue += p.price
            self._save_to_storage() # 상태 저장
        return p, msg

    def refill_one(self, p_id: int):
        """관리자: 재고 보충 (최대 10개)"""
        p = self.products.find_by_id(p_id)
        if not p: return False, "상품 없음"
        if p.stock >= 10: return False, "재고가 가득 찼습니다."
        p.stock += 1
        self._save_to_storage() # 상태 저장
        return True, f"{p.name} 보충 완료"

    def collect_revenue(self):
        """관리자: 수익금 회수"""
        amount = self.total_revenue
        self.total_revenue = 0
        self._save_to_storage() # 상태 저장
        return amount

    def reset_system(self):
        change = self.balance
        self.balance = 0
        self.payment_locked = None
        return change