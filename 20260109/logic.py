import json

class VendingMachine:
    def __init__(self, json_data):
        try:
            # 데이터가 없거나 비어있으면 기본 구조 할당
            if not json_data or json_data.strip() == "":
                raise ValueError("Empty data")
            self.products_data = json.loads(json_data)
        except Exception:
            self.products_data = {"default": {"name": "준비중", "image": "https://img.icons8.com/color/144/beverage.png"}}

        self.products = {}
        for i in range(1, 37):
            key = str(i)
            if key in self.products_data:
                self.products[i] = self.products_data[key]
            else:
                self.products[i] = self.products_data.get("default", {"name": f"상품-{i:02d}", "image": ""}).copy()
                if "name" not in self.products[i] or self.products[i]["name"] == "준비중":
                    self.products[i]["name"] = f"상품-{i:02d}"

    def get_product(self, code_str):
        try:
            code = int(code_str)
            if code in self.products:
                item = self.products[code]
                return item, f"{code}번 {item['name']} 선택"
            return None, f"오류: {code}번 없음"
        except:
            return None, "오류: 숫자 입력 필요"