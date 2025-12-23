from dataclasses import dataclass

@dataclass
class CafeMenu:
    name:str
    price:int

    def order(self):
        print(f"메뉴 : {self.name}의 가격은 {self.price}원 입니다.")
    
cola = CafeMenu("아이스아메리카노", 2000)
cola.order() # CafeMenu(name='아이스아메리카노', price=2000)
print(cola) # dataclass __str__ 자동생성 # CafeMenu(name='아이스아메리카노', price=2000)
print(cola.name) # "아이스 아메리카노"