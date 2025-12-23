member = [ 
    {"name": "공욱재", "age":26},
    {"name": "김동찬", "age":39},
    {"name": "고경명", "age":55},
]

print(member[0]["name"])
print(member[2]["age"])

# 만약 고경명이라는 이름이 있다면, 신재혁으로 바꿔주세요.
for i in range(len(member)):
    assemble = member[i]
    if assemble["name"] == "고경명":
        assemble["name"] = "신재혁"
    print(assemble["name"], assemble["age"])
    # print(member[i]["name"], member[i]["age"])


# 욱재님 말고는 나머지 사람은 나이가 +2 많아진다.
for i in range(len(member)):
    assemble = member[i]
    if assemble["name"] != "공욱재":
        assemble["age"] += 2
    print(assemble["name"], assemble["age"])

# 만약에 다른 배열을 입력받아서, 이름 전체를 다 바꾸고 싶다면?
# Q. 이름 전체만 쏙 바꾸고 싶다면?

# 내장함수를 안쓰고, 마지막에 유효현을 넣어본다.
# 딕셔너리를 삽입하는 방법, 분해해서 넣는 방법도 있을 것이고
# 내장함수를 안쓰는 방식이면, 쪼개서 넣어야겠네.

add_member = {"name":"유효현", "age":35}
# enumerate 검지검지
# 각각의 요소를 넣자.
member.append(add_member)
print(member)
# append도 검지검지.
# 엄청 쉬운데 어렵게 생각하고 있는지도 몰라.

# add_member.keys # key, value도 내장함수네.
# add_member.values

member = member + [add_member] # 원시적이지만 가장 간단한 방법
print(member)

