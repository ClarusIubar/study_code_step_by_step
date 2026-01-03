from practice import Product, Staff

class WookjaeMart:
    def __init__(self, products: list[Product], staffs: list[Staff]):
        # 1. 성능용: 검색은 Dict (O(1))
        self._product_map = {p.name: p for p in products}
        self._staff_map = {s.name: s for s in staffs}
        
        # 2. 연산용: 집합 관리는 Resultset
        self.products = Resultset(products)
        self.staffs = Resultset(staffs)

    # --- [조회 영역: 수정이 발생할 수 있는 지점] ---
    def find_product(self, name: str) -> Product:
        return self._product_map.get(name)

    def find_staff(self, name: str) -> Staff:
        return self._staff_map.get(name)
    
    # --- [추출 영역: 속성이 추가되어도 수정이 필요 없는 지점] ---
    def get_products_under_stock(self, threshold: int) -> Resultset:
        items = [p for p in self.products if p.stock < threshold]
        return Resultset(items)

class Resultset(list):
    def __getattr__(self, key):
        """
        [정의] 인스턴스 집합에서 특정 속성(Attribute)을 일괄 추출하는 '동적 프로젝션' 엔진.
        
        :param self: Resultset 인스턴스 (Product나 Staff 객체들이 담긴 리스트 상태).
        :param key: 인스턴스에서 추출하고자 하는 속성 키, 사용자가 점(.) 뒤에 입력한 문자열. 
        파이썬 객체 구조상 '속성 이름'이자 '딕셔너리 키'와 동일함.
        
        [작동 원리]
        1. 사용자가 `result.price`를 호출하면, 파이썬은 Resultset에 'price'가 없음을 확인.
        2. 즉시 이 메서드를 실행하며 `key` 인자에 "price" 문자열을 전달.
        3. 내부 리스트를 순회하며 각 객체의 .price 값을 낚아채어 새로운 Resultset으로 반환.
        
        [실무적 이점]
        - 디버깅 시: getattr() 단계에서 객체에 해당 키가 없는 경우를 명확히 트래킹 가능.
        """
        """속성 추출 (Projection)"""
        if not self: return Resultset()
        try:
            return Resultset([getattr(item, key) for item in self])
        except AttributeError:
             raise AttributeError(f"내부 객체들에 '{key}' 속성이 없습니다.")

    def __str__(self):
        """
        [사용자용] print(low_stock.name)을 했을 때 
        ['...'] 괄호를 제거하고 값만 깔끔하게 전달합니다.
        """
        if not self:
            return ""
        return ", ".join(map(str, self))

    def __repr__(self):
        """
        [디버깅용] 변수 자체를 찍거나 디버거에서 볼 때 
        리스트임을 명시하고 내부 데이터 타입을 보여줍니다.
        """
        content = super().__repr__()
        return f"Resultset({content}) <Count: {len(self)}>"
    
    def filter(self, func):
        """[추가] 조건에 맞는 요소만 걸러내어 다시 Resultset으로 반환 (Chaining)"""
        return Resultset([item for item in self if func(item)])