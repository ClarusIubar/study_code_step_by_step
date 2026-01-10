from pydantic import Field
from core.model import StandardModel

class Product(StandardModel):
    # products.json의 실제 필드만 정의 (category 삭제)
    id: int = Field(ge=1, le=36)
    name: str = Field(min_length=1, max_length=20)
    price: int = Field(ge=0, le=10000)
    stock: int = Field(ge=0, le=100)
    image: str = ""

    def process_sell(self, quantity: int = 1):
        """판매 처리: 재고 부족 시 에러 발생"""
        try:
            self.stock -= quantity
            return True, f"[{self.name}] 배출 완료"
        except:
            return False, f"[{self.name}] 재고 부족"