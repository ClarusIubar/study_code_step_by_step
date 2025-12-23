# 일반자판기
# input : money
# process : product
# output : can_for_drink, money

import caculate_money
import product_table

def normal_vending_machine(money, product):
    # calculate_money
    choiced_product, price_product = product_table.approved_product(product) 
    # 추후의 재고의 개수를 리턴 받을 수도 있으므로 ( , ) 
    # 재고가 없다고 반환할 수도 있음. (none type -> 처리방법 다르게)

    # 얘도 분리할 수 있을 것 같고, 리터럴 안 쓸 수 있을 것 같아. 
    if money >= price_product:
        remain = caculate_money.calculate_remain(money, price_product)
        print(f"거스름돈 {remain}원과 {choiced_product}를 받으세요.")
    else:
        raise ValueError("돈을 더 넣으쇼!") # 0보다 작은 값은 허용하지 않음 -> value error
    
## 뭐가 있는지 보여주기
## 선택했을 때, input을 사용자로부터 받게 하기
## 예외처리
## output결과에 따라 error raise 또는 인자별로 결과가 달라지게 함수구성