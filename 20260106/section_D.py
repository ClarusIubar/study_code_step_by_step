# D-01
# name = input("이름을 입력하세요 : ")
# age = int(input("나이를 입력하세요 : "))

# members = []
# person = {"name" : name, "age": age}
# members.append(person)

# print(members)

# D-02
members = [
    {"name":"공욱재", "age":26},
    {"name":"공미남", "age":27},
    {"name":"공추남", "age":28},
]

for member in members:
    print(member["name"])
