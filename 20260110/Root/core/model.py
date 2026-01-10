from pydantic import BaseModel
from typing import TypeVar, Type, Union, List, Dict, Any

# Pydantic v1/v2 호환성 레이어 (TypeAdapter 부재 대응)
try:
    from pydantic import TypeAdapter
    HAS_V2 = True
except ImportError:
    from pydantic import parse_obj_as
    HAS_V2 = False

T = TypeVar("T", bound="StandardModel")

def get_structure_tag(v: Any) -> str:
    """O(1) 구조 판별자: 데이터 샘플링을 통해 차원 결정"""
    if isinstance(v, list): return "list"
    if isinstance(v, dict):
        for k, val in v.items():
            if k == "default": continue
            return "map" if isinstance(val, dict) else "single"
    return "single"

class StandardModel(BaseModel):
    class Config: # v1 호환
        validate_assignment = True
        extra = "allow"
    
    # v2 호환
    model_config = {"validate_assignment": True, "extra": "allow"}

    @classmethod
    def from_auto(cls: Type[T], data: Any) -> Union[T, List[T], Dict[str, T]]:
        """Single, List, Map을 자동 판별하고 ID를 주입하는 범용 엔진"""
        tag = get_structure_tag(data)
        
        if tag == "map":
            res = {}
            for k, v in data.items():
                if k == "default" or not k.isdigit(): continue
                v_copy = v.copy() if isinstance(v, dict) else {}
                v_copy["id"] = int(k) # JSON Key를 ID로 바인딩
                res[k] = cls._parse(v_copy)
            return res
        
        return cls._parse(data, many=(tag == "list"))

    @classmethod
    def _parse(cls, data, many=False):
        if HAS_V2:
            target = List[cls] if many else cls
            return TypeAdapter(target).validate_python(data)
        return parse_obj_as(List[cls] if many else cls, data)