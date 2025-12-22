class Member:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # __str__은 객체를 print() 함수로 출력할 때 어떻게 보여줄지 정의하는 함수 
    # 사람이 읽기 편한 형태로 리턴하도록 설정합니다.
    def __str__(self):
        return f"Member(name: {self.name}, age:{self.age})"
    
    # 리스트에 담기거나, 객체의 '본모습'을 표현할 때
    def __repr__(self):
        return f"Member(name='{self.name}', age={self.age})"

test = Member("공욱재", 24)
print(test) # Member(name: 공욱재, age: 24)

members = [test] # test 인스턴스를 단순히 리스트로 감싸서 테스트
print(members) # [Member(name='공욱재', age=24)]
