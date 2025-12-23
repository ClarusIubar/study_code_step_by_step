import add as add_module
import element_table as element_module

# input (number)
# number limiter for element
# choose element
# output -> element

# 사람이 숫자 두 개를 입력한다.
# 119이상이 들어오면 막는다.
# 118이하까지 원소 숫자를 더한다.
# 원소 숫자에 맞는 원소를 가져온다.
# 원소를 출력한다.

number1 = 30
number2 = 50

if (number1 + number2) > 118:
    print("당신은 주기율표에 없는 새로운 원소를 생성하려고 하시는군요. 새로운 원소를 정의해야겠어요!")
else:
    result = add_module.add(number1,number2)
    element = element_module.out_element(result)
    print(f"{element}가 연성되었습니다.")

# ---
