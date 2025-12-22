from dataclasses import dataclass

@dataclass
class Member:
    name: str
    age: int

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError(f"유효하지 않은 이름입니다. 당신의 입력 : {self.name}")
        if not 0 < self.age < 150:
            raise ValueError(f"유효하지 않은 숫자 혹은 숫자범위입니다. 당신의 입력 : {self.age}")
        self.name = self.name.strip()

test1 = Member(" 공욱재   ", 25)
# test2 = Member("공욱재", -5)
test3 = Member(["공욱재"], 25)

print(test1) # Member(name='공욱재', age=25)
# print(test2) # ValueError: 유효하지 않은 숫자 혹은 숫자범위입니다. 당신의 입력 : -5
print(test3) # TypeError: 유효하지 않은 이름입니다. 당신의 입력 : ['공욱재']