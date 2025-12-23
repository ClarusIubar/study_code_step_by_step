# 키오스크로 범위를 제한하고 시작한다.
# 우선 사용자의 입력(행위 : 선택)은 단순하게 literal로 받는다. 대신 2개 이상을 고려하여 리스트 형태로 구성한다.
# 리스트 형태의 입력을 파싱해서 각각의 가능여부(음료가 실제로 있는지, 재고가 있는지)를 파악한다.
    # 만약에 여러개 중에 하나라도 존재하지 않는다면(불가 항목), 없는 것은 빼라고 할 지.
    # 존재하지 않는 항목에 대해서는 따로 리스트에 append한다. 나중에 데이터 분석시에 빈도수를 고려하여 사용자의 요구 빈도에 따라 메뉴를 추가할 지 말 지 결정한다.
# 결과 : 선택한 제품의 리스트를 보여주고 끝낸다.


# * 데이터 정의
Yoos_menu = {
    "Coffee": [
        {"name": "앗!메리카노(ICED)", "price": 2000},
        {"name": "앗!메리카노(HOT)", "price": 1500},
        {"name": "원조커피(ICED)", "price": 2500},
        {"name": "바닐라라떼(ICED)", "price": 3700},
        {"name": "카페라떼(ICED)", "price": 3000}
    ],
    "Beverage": [
        {"name": "딸기라떼", "price": 3800},
        {"name": "청포도에이드", "price": 4000},
        {"name": "미숙이가루", "price": 2500},
        {"name": "단호박식혜", "price": 2500}
    ],
    "Paik'sccino": [
        {"name": "초코빽스치노(소프트)", "price": 4000},
        {"name": "딸기바나나빽스치노(베이직)", "price": 3800},
        {"name": "녹차빽스치노(소프트)", "price": 4300}
    ],
    "Dessert": [
        {"name": "노말한소프트", "price": 2000},
        {"name": "사라다빵", "price": 3500},
        {"name": "소시지빵", "price": 3500},
        {"name": "크리미슈", "price": 2000}
    ]
}

# 우선은 상단의 탭은 str리터럴을 누르면(input) 하위의 제품은 0(숫자인덱스)와 제품과 가격이 맵핑하게 선택 후, 수량입력 , 
# "주문"을 할 경우에 영수증이 나오게 하고 싶어. 우선은 데이터 타입으로 접근을 구분하는 if문으로 나눌 생각이야.

# * 사용자가 맨 처음 마주할 화면
basket_product = []

print("="*40)
print("      [ 짭다방 키오스크 시스템 ]")
print("  ('주문' 입력 시 최종 결제 및 영수증 발행)")
print("="*40)

for category in Yoos_menu:
    print(category)

# user_input_category = input("카테고리를 선택해 주세요.")
user_input_category = "Coffee"

if user_input_category in Yoos_menu:
    for item in Yoos_menu[user_input_category]:
        print(item["name"],"\t", item["price"])

# user_input_product = input("메뉴를 선택해 주세요.")
user_input_product = "앗!메리카노(HOT)"

