coffee = []
coffee.append({
    "원산지" : ["에티오피아", "케냐", "콜롬비아", "브라질", "베트남"]
})
coffee.append({
    "물종류" : ["경수", "연수", "석수"]
})
coffee.append({
    "얼음" : ["냉장고얼음", "고드름", "석빙고얼음"]
})
coffee.append({
    "드립방식" : ["하리오", "칼리타", "케멕스", "금속필터"]
})

# coffee.append("커피콩") # 에티오피아, 케냐, 콜롬비아, 브라질, 베트남
# coffee.append("물") # 경수, 연수, 석수
# coffee.append("얼음") # 냉장고얼음, 공업용얼음, 고드름, 끓인얼음, 석빙고얼음
# coffee.append("드로퍼") # 하리오, 칼리타, 케멕스, 금속필터

# print(coffee)
print(coffee[1])
print(coffee[0]["원산지"])
print(len(coffee[0]["원산지"]))
print(coffee[0].values()) ## dict_values([['에티오피아', '케냐', '콜롬비아', '브라질', '베트남']]) 

coffee[0]["원산지"].append("루왁")
print(coffee[0])

print(coffee[0].keys()) # 나는 저 0,1,2,3을 쓰고 싶지 않아. # 그렇다고 for문을 써서 순회하는 방법도 X


## 아이스 아메리카노 레시피를 하나 만들래요. 
# 1. 객체, 배열을 추가하는 방법
# 2. 원하는 위치로 접근하는 방법
# 3. 재할당하는 방법
# 4. 필요한 만큼 꺼내쓰는 방법
# ---
# 5. 판단
# 6. 내역을 뽑을 수도 있음.