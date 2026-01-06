# # A-01
# person = {}
# print(person)

# A-02
# person = {
#     "name" : "공욱재",
#     "age" : 26,
# }
# print(person)

# A-03
# person = {
#     "name" : "공욱재",
#     "age" : 26,
# }
# name = person["name"]
# print(name)

# A-04
# person = {
#     "name" : "공욱재",
#     "age" : 26,
# }
# person["age"] = 30
# print(person)

# A-05
# person = {
#     "name" : "공욱재",
#     "nickname" : "공미남",
# }
# person["nickname"] = "공추남"
# print(person)

# # A-06
# person = {
#     "name" : "공욱재",
#     "nickname" : "공미남",
# }
# result = "name" in person
# print(result)

# A-07
# person = {
#     "name" : "공욱재",
#     "age" : 26,
#     "nickname" : "공미남",
# }
# del person["nickname"]
# print(person)

# A-08
# person = {
#     "name" : "공욱재",
#     "age" : 26,
# }

# keys = list(person.keys())
# print(keys) # ['name', 'age']

# for data in person:
#     print(data) # name \n age

# for key in person:
#     print(person[key]) # 공욱재 \n 26

# for i, key in enumerate(person):
#     print(i, key) # 0 name \n 1 age