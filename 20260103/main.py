import data
from practice import Product, Staff
from WookjaeMart import WookjaeMart

# 1. 마트 시스템 오픈 (WookjaeMart 객체 생성)
product_list = Product.from_list(data.product_data)
staff_list = Staff.from_list(data.staff_data)
mart = WookjaeMart(product_list, staff_list)

# 2. [직원 관리] '김수빈' 직원을 찾아서,
#    - 8시간 일하게 하고 (여러분이 만든 메서드 호출)
#    - 급여가 얼마인지 출력하세요.
salary = mart.find_staff("김수빈").add_work_hours(4).add_work_hours(4).calculate_salary()
print(salary) # 78880
salary = mart.find_staff("김수빈").add_work_hours(40).calculate_salary() 
# 주 40시간 제한 / 유효하지 않은 근무 시간 입력입니다.
print(salary) # 78880

# 3. [재고 관리] '삼각김밥'을 찾아서,
#    - 현재 정보를 출력하고 (여러분이 만든 메서드 호출)
#    - 5개를 판매 처리하세요.
#    - 다시 현재 정보를 출력하여 재고가 줄었는지 확인하세요.
gimbab = mart.find_product("삼각김밥").process_sale(5)   # 삼각김밥 5개 판매 완료. (남은 재고: 10)
gimbab = mart.find_product("삼각김밥").process_sale(100) # 삼각김밥: 재고가 부족합니다. (현재 재고: 10)
gimbab = mart.find_product("삼각김밥").process_sale(5)   # 삼각김밥 5개 판매 완료. (남은 재고: 5)

# 4. [보너스] 전체 재고 파악
#    - mart가 가진 모든 상품을 반복문으로 돌면서,
#    - 재고가 20개 미만인 상품의 이름만 출력해보세요.
#    (힌트: p.stock 처럼 속성에 접근하거나, 정보 출력 메서드 활용)

low_stock_items = mart.get_products_under_stock(20)
print(low_stock_items.name, sep=',') # 삼각김밥, 초코파이

# 래퍼 클래스, 스마트 컨테이너 동작 확인
# print(repr(low_stock_items))    # Resultset([Product(name='삼각김밥', price=1200, stock=5, category=<Category.RETORT: '간편식'>), Product(name='초코파이', price=4500, stock=18, category=<Category.SNACK: '과자'>)]) <Count: 2>
# print(low_stock_items[0].name)  # 삼각김밥
# print(low_stock_items[0].price) # 1200