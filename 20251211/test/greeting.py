# 이름을 불러오면 인사를 하는 기본 코드를 작성한다.
# 로그인을 하지 않으면 사용자님 안녕하세요로 작동하게 한다.
# input(이름) + 인사하기 -> output(~님, 안녕하세요.)

def greeting(name = "사용자"):
    print(f"""{name}님 안녕하세요! 환영합니다!""")

greeting()
greeting("유효현")