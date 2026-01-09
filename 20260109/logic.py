import json

class VendingMachine:
    def __init__(self, json_data):
        self.balance = 0
        self.status = "IDLE"  # IDLE, READY, PROCESS, DISPENSE
        self.payment_locked = None  # CASH, CARD
        
        try:
            data = json.loads(json_data) if json_data.strip() else {}
        except:
            data = {}

        self.products = {}
        # 1~36번 슬롯 초기화 (default 데이터 활용)
        default_item = data.get("default", {"name": "상품", "price": 1000, "stock": 5, "image": ""})
        for i in range(1, 37):
            self.products[i] = data.get(str(i), default_item.copy())

    def insert_cash(self, amount):
        """현금 투입: 카드 결제 중에는 차단"""
        if self.payment_locked == "CARD":
            return False, "카드 결제 진행 중에는 현금을 투입할 수 없습니다."
        
        if self.balance + amount > 50000:
            return False, "현금 투입 한도(5만원)를 초과했습니다."
            
        self.balance += amount
        self.payment_locked = "CASH"
        self.status = "READY"
        return True, f"{amount}원 투입됨 (현재 잔액: {self.balance}원)"

    def tag_card(self):
        """카드 태그: 현금 투입 중에는 차단 및 승인 대기 상태 전환"""
        if self.payment_locked == "CASH":
            return False, "현금이 투입된 상태에서는 카드를 사용할 수 없습니다."
        
        self.status = "PROCESS" # 승인 프로세스 진입
        self.payment_locked = "CARD"
        return True, "카드 승인 요청 중..."

    def purchase(self, code):
        """상품 구매: 재고, 잔액, 상태를 모두 검증"""
        try:
            idx = int(code)
            p = self.products.get(idx)
            
            if not p:
                return None, "존재하지 않는 상품 번호입니다."
            if p['stock'] <= 0:
                return None, f"[{p['name']}] 상품은 현재 품절입니다."
            if self.balance < p['price']:
                return None, f"잔액이 부족합니다. (부족분: {p['price'] - self.balance}원)"
            
            # 구매 확정 및 차감
            self.balance -= p['price']
            p['stock'] -= 1
            self.status = "DISPENSE"
            
            return p, f"[{p['name']}] 배출 완료. 남은 잔액: {self.balance}원"
        except ValueError:
            return None, "숫자 번호를 정확히 입력해주세요."

    def reset_system(self):
        """시스템 초기화: 잔액 반환 및 모든 잠금 해제"""
        change = self.balance
        self.balance = 0
        self.payment_locked = None
        self.status = "IDLE"
        return change