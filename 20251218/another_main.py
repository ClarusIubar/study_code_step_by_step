pc_cafe = {
    "food" : ["라면", "과자", "볶음밥", "햄버거", "샌드위치"],
}

# * 카페에 있는 음식 목록 보여주기
for food_index in range(len(pc_cafe["food"])):
    print(food_index, pc_cafe["food"][food_index])

# 사용자 입력받기
user_choice = input("먹고 싶은 음식을 작성하세요 : ")

if user_choice in pc_cafe["food"]:
        print(user_choice + " 음식을 준비하겠습니다.")
else:
        print("아쉽게도 그 음식은 없습니다.")
        user_yes_no = input("하지만, 내일 준비할까요?(네/아니오)")
        if user_yes_no == "네":
            pc_cafe["food"].append(user_choice)
            print(pc_cafe["food"])

        else:
            print(pc_cafe["food"])
            print("종료")

print("사용자의 선택 : ", user_choice)

# * 1. 카페 음식 정의하기
# * 2. 음식 목록 조회하기
# * 3. 사용자가 먹고싶은 음식 선택하기
# * 4. 사용자가 선택한 음식이 카페에 있는지 확인하기
# * 5. 음식이 있으면 준비하겠다고 하기