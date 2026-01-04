from pydantic import BaseModel, TypeAdapter
from typing import TypeVar, Type, Union

# 자기 자신을 반환하기 위한 타입 힌트
T = TypeVar("T", bound="StandardModel")

class StandardModel(BaseModel):
    model_config = {"validate_assignment": True}

    @classmethod
    def from_list(cls: Type[T], data: Union[list, dict]) -> Union[list[T], T]:
        """파이썬 객체(list/dict)를 검증하여 인스턴스로 변환"""
        # 데이터가 리스트면 리스트로, 단일 객체면 단일 인스턴스로 자동 대응
        target_type = list[cls] if isinstance(data, list) else cls
        return TypeAdapter(target_type).validate_python(data)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> Union[list[T], T]:
        """JSON 문자열을 검증하여 인스턴스로 변환"""
        # 문자열이 '['로 시작하면 리스트로 판단
        is_list = json_str.strip().startswith("[")
        target_type = list[cls] if is_list else cls
        return TypeAdapter(target_type).validate_json(json_str)