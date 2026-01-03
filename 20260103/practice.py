from pydantic import Field, ValidationError
import enum_data
import data
from validate import StandardModel

class Staff(StandardModel):
    name: str = Field(min_length=1, max_length=5)
    hourly_wage: int = Field(ge=0, le=15000)
    work_hours: int = Field(default=0, ge=0, le=40)
    position: enum_data.Position
    shift: enum_data.Shift

    # 기능 C: 일하기 (시간 누적)
    def add_work_hours(self, hours: int):
        try:
            self.work_hours += hours
            print(f"{self.name} {hours}시간 근무 추가.")
        
        except ValidationError:
            print(f"{self.name}: 유효하지 않은 근무 시간 입력입니다.")
        
        return self

    # 기능 D: 급여 계산
    def calculate_salary(self) -> int:
        return self.hourly_wage * self.work_hours

class Product(StandardModel):
    name: str = Field(min_length=1, max_length=5)
    price: int = Field(ge=0, le=5000)
    stock: int = Field(ge=0, le=100)
    category: enum_data.Category

    # 기능 A: 정보 출력 (동사_목적어 형태)
    def get_summary(self) -> str:
        return f"[{self.category.value}] {self.name} | 가격: {self.price}원 | 재고: {self.stock}개"

    # 기능 B: 판매 처리
    def process_sell(self, quantity: int):
        try:
            self.stock -= quantity
            print(f"{self.name} {quantity}개 판매 완료. (남은 재고: {self.stock})")
            return self
        except ValidationError:
            print(f"{self.name}: 재고가 부족합니다. (현재 재고: {self.stock})")
        
        return self

