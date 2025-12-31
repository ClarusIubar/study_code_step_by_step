# 윤년
# 윤년 규칙은 4로 나누어 떨어지는 해는 윤년이지만, 
# 100으로 나누어 떨어지면 윤년이 아니고, 
# 단, 400으로 나누어 떨어지면 다시 윤년이 되는 규칙입니다. 

year = int(input("년을 입력하세요: "))

# 우선순위와 논리적 포함 관계를 고려한 조건식
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    year_label = "윤년"
else:
    year_label = "평년"

print(f"{year}년은 {year_label}입니다.")