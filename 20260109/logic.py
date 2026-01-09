import json

class VendingMachine:
    def __init__(self, json_data):
        self.products = {}
        try:
            # 데이터가 비어있을 경우에 대한 방어
            data = json.loads(json_data) if json_data.strip() else {}
        except:
            data = {}

        # 1~36번 슬롯 생성
        for i in range(1, 37):
            key = str(i)
            if key in data:
                self.products[i] = data[key]
            else:
                # 데이터 없을 시 기본 이미지(아이콘) 적용
                self.products[i] = {
                    "name": f"상품-{i:02d}",
                    "image": "https://img.icons8.com/color/144/beverage.png"
                }

    def get_product(self, code_str):
        try:
            code = int(code_str)
            if code in self.products:
                item = self.products[code]
                return item, f"{code}번 {item['name']} 선택"
            return None, f"번호 오류: {code}번 없음"
        except:
            return None, "숫자만 입력 가능합니다."