from typing import Annotated
from pydantic.dataclasses import dataclass
from pydantic import Field, AfterValidator

# 1. 재사용 가능한 데이터 규격 (마치, 옵시디언에서 메타데이터의 타입을 제한하고 싶을 때처럼,
#     프론트메터로 지정하면, 데이터에 대한 검증을 쉽게 변경할 수 있다.)
NameType = Annotated[str, AfterValidator(str.strip), Field(min_length=1)]
AgeType = Annotated[int, Field(ge=0, le=150)]

# 2. 데이터 금형을 정의
@dataclass
class Member():
    name:NameType
    age:AgeType

# 3. 데이터 금형을 활용
try:
    print(Member("    공욱재  ", 25)) # Member(name='공욱재', age=25)
except Exception as e:
    print(f"올바른 데이터 형식이 아닙니다. {e}")
