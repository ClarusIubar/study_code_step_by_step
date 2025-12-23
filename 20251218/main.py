pc_cafe = {
    "food" : ["라면", "과자", "볶음밥", "햄버거", "샌드위치"],
}

# * 카페에 있는 음식 목록 '조회'
for food_index in range(len(pc_cafe["food"])):
    print(food_index, pc_cafe["food"][food_index])

# 만약에 input에 입력된 값이 피시까페 푸드에 있는 배열에 없는 항목이라면: 
# 죄송하지만 준비중입니다. 나중에는 추가할게요. <- 메세지
# 배열에 있는 항목이라면, 5분내로 준비해서 드리겠습니다. 

user_choice = input("먹고 싶은 음식을 작성하세요 : ")

if user_choice in pc_cafe["food"]:
    print("5분내로 준비해서 드리겠습니다.")
else:
    print("죄송하지만 준비중입니다. 나중에는 추가할게요.")

# 왜 난 또 돌아갔을까? 왜 다른 방법은 없을까하고, 다른 걸 시험해볼까?
# 코드 생각난 첫 안은 폐기해 버리고 다른 것은 없나 생각하는 것이 발동하기 시작했다.


