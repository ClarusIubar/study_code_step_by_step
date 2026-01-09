class VendingMachine:
    def __init__(self):
        self.products = {i: f"상품-{i:02d}" for i in range(1, 37)}

    def get_product(self, code_str):
        try:
            code = int(code_str)
            if code in self.products:
                item = self.products[code]
                return item, f"{code}번 {item} 배출 완료"
            return None, f"오류: {code}번은 없는 번호입니다."
        except ValueError:
            return None, "오류: 숫자만 입력 가능합니다."