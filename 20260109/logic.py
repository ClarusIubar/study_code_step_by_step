import json

class VendingMachine:
    def __init__(self, json_data):
        self.balance = 0
        self.payment_locked = None 
        
        try:
            data = json.loads(json_data) if json_data.strip() else {}
        except:
            data = {}

        self.products = {}
        # 1~36번 슬롯 초기화
        for i in range(1, 37):
            self.products[i] = data.get(str(i), data.get("default", {"name": "상품", "price": 1000, "stock": 5, "image": ""})).copy()

    def insert_cash(self, amount):
        if self.payment_locked == "CARD": return False, "카드 사용 중에는 현금을 넣을 수 없습니다."
        self.balance += amount
        self.payment_locked = "CASH"
        return True, f"{amount}원 투입 완료"

    def tag_card(self):
        if self.payment_locked == "CASH": return False, "현금이 투입된 상태입니다."
        # 카드 태그 시 프로세스는 UI에서 처리하므로 여기선 상태만 잠금
        self.payment_locked = "CARD"
        return True, "카드 승인 프로세스 시작"

    def purchase(self, code):
        """다중 구매 핵심: 구매 후 잔액이 남으면 계속 구매 가능 상태 유지"""
        try:
            idx = int(code)
            p = self.products.get(idx)
            if not p: return None, "존재하지 않는 번호입니다."
            if p['stock'] <= 0: return None, "품절된 상품입니다."
            if self.balance < p['price']: return None, "잔액이 부족합니다."
            
            # 차감 로직
            self.balance -= p['price']
            p['stock'] -= 1
            return p, f"{p['name']} 배출 중... (잔액: {self.balance}원)"
        except:
            return None, "숫자 번호를 입력하세요."

    def reset_system(self):
        """명시적 종료 및 반환"""
        change = self.balance
        self.balance = 0
        self.payment_locked = None
        return change