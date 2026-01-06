# B-01
# members = []
# person = {
#     "name" : "공욱재",
#     "age" : 26,
# }

# members.append(person)
# print(members)

# B-02
# members = [
#     {"name":"공욱재", "age":26},
#     {"name":"공미남", "age":27},
#     {"name":"공추남", "age":28},
# ]
# print(members) 
# [{'name': '공욱재', 'age': 26}, {'name': '공미남', 'age': 27}, {'name': '공추남', 'age': 28}]

# B-03
# members = [
#     {"name":"공욱재", "age":26},
#     {"name":"공미남", "age":27},
# ]
# first = members[0]
# print(first)

# B-04
# members = [
#     {"name":"공욱재", "age":26},
#     {"name":"공미남", "age":27},
# ]
# name = members[0]["name"]
# print(name) # 공욱재

# B-05
# members = [
#     {"name":"공욱재", "age":26},
#     {"name":"공미남", "age":27},
#     {"name":"공추남", "age":28}
# ]
# for member in members:
#     print(member)

# B-06
# members = [
#     {"name": "공욱재", "age": 26},
#     {"name": "공미남", "age": 27},
#     {"name": "공추남", "age": 28}
# ]

# for member in members:
#     print(member["name"]) # 공욱재 \n 공미남 \n 공추남

# B-07
# members = [
#     {"name":"공욱재", "age":26},
#     {"name":"공미남", "age":27}
# ]
# for member in members:
#     member["age"] += 1
# print(members)