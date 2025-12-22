class Member:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # __str__은 객체를 print() 함수로 출력할 때 어떻게 보여줄지 정의하는 함수 
    # 사람이 읽기 편한 형태로 리턴하도록 설정합니다.
    def __str__(self):
        return f"Member(이름: {self.name}, 나이: {self.age})"

test = Member("공욱재", 24)
print(test) # Member(이름: 공욱재, 나이: 24)
