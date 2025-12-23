def add_normal(a, b):
    return a + b

add_lambda = lambda a, b: a + b # parameter, return

print(f"일반 함수 결과: {add_normal(5,3)}")
print(f"람다 함수 결과: {add_lambda(5,3)}")

is_positive = lambda x: 'Positive' if x>0 else 'None-Positive'
print(is_positive(10))
print(is_positive(-5))

is_True = lambda x: True if x>0 else False
print(is_True("유효현" == "유효현"))
print(type(is_True("유효현" == "유효현")))