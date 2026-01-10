from pydantic import BaseModel
from typing import TypeVar, Type, Union, List, Dict, Any

try:
    from pydantic import TypeAdapter
    HAS_V2 = True
except ImportError:
    from pydantic import parse_obj_as
    HAS_V2 = False

T = TypeVar("T", bound="StandardModel")

def get_structure_tag(v: Any) -> str:
    if isinstance(v, list): return "list"
    if isinstance(v, dict):
        for k, val in v.items():
            if k == "default": continue
            return "map" if isinstance(val, dict) else "single"
    return "single"

class StandardModel(BaseModel):
    class Config:
        validate_assignment = True
        extra = "allow"
    
    model_config = {"validate_assignment": True, "extra": "allow"}

    @classmethod
    def from_auto(cls: Type[T], data: Any) -> Union[T, List[T], Dict[str, T]]:
        """[수정] 맵 구조 로딩 시 파이썬 루프 오버헤드를 제거한 네이티브 파싱"""
        tag = get_structure_tag(data)
        if tag == "map":
            if HAS_V2:
                return TypeAdapter(Dict[str, cls]).validate_python(data)
            return parse_obj_as(Dict[str, cls], data)
        return cls._parse(data, many=(tag == "list"))

    @classmethod
    def _parse(cls, data, many=False):
        if HAS_V2:
            target = List[cls] if many else cls
            return TypeAdapter(target).validate_python(data)
        return parse_obj_as(List[cls] if many else cls, data)