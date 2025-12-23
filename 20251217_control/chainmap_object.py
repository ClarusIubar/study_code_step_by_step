from collections import ChainMap

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

coffee_view = ChainMap(*coffee) ## 이런거에 익숙해지면 안되는데. 내가 이단이 되고 있어.
coffee_view["원산지"].append("블루마운틴")

print(coffee_view.maps)

## add(key, value) -> key.append(value)
## show(key) -> value:list
## make(recipe) -> recipe(value) -> process -> output
## remove(key, value) -> None
## reassign : remove(key, value) + add(key,value)

## class only key handling in show
## key, value handling
## dict data handling

## chainmap이 의미가 없어졌어. 판다스를 가지고 추상화된 기능을 가진 클래스를 만들어야 하나?
## 오랜만에 판다스를 맛보니까 바닐라로 짜기가 싫어졌어. ㅋㅋㅋ