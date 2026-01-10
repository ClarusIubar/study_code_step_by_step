from pydantic import Field
from core.model import StandardModel

class Product(StandardModel):
    id: int = Field(ge=1, le=36)
    name: str = Field(min_length=1, max_length=20)
    price: int = Field(ge=0, le=10000)
    stock: int = Field(ge=0, le=100)

    def process_sell(self, quantity: int = 1):
        if self.stock >= quantity:
            self.stock -= quantity
            return True, f"[{self.name}] 배출 완료"
        return False, f"[{self.name}] 재고 부족"