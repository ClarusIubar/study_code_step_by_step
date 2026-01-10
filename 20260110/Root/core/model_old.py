from pydantic import BaseModel, TypeAdapter, Discriminator
from typing import TypeVar, Type, Union, List, Dict, Any, Annotated

T = TypeVar("T", bound="StandardModel")

def structure_discriminator(v: Any) -> str:
    """O(1) 구조 판별자: 샘플링을 통해 데이터 차원을 즉시 결정"""
    if type(v) is list: return "list"
    if type(v) is dict:
        for k, val in v.items():
            if k == "default": continue
            # 내부 값이 딕셔너리면 Map(Nested)으로 판단
            return "map" if type(val) is dict else "single"
    return "single"

class StandardModel(BaseModel):
    model_config = {"validate_assignment": True, "extra": "allow"}

    @classmethod
    def from_auto(cls: Type[T], data: Any) -> Union[T, List[T], Dict[str, T]]:
        """Single, List, Map을 자동 판별하고 Nested Dict의 Key를 ID 필드로 주입"""
        tag = structure_discriminator(data)
        
        if tag == "map":
            processed = {}
            for k, v in data.items():
                if k == "default" or not k.isdigit(): continue
                # JSON Key를 id 필드로 바인딩 (Impedance Mismatch 해결)
                v_copy = v.copy() if isinstance(v, dict) else {}
                v_copy["id"] = int(k)
                processed[k] = TypeAdapter(cls).validate_python(v_copy)
            return processed
        
        adapter = TypeAdapter(Annotated[
            Union[Annotated[cls, "single"], Annotated[List[cls], "list"]],
            Discriminator(lambda v: "list" if type(v) is list else "single")
        ])
        return adapter.validate_python(data)
    


### ---

from pydantic import BaseModel
from typing import TypeVar, Type, Union, List, Dict, Any

# Pydantic v1/v2 호환 브릿지
try:
    from pydantic import TypeAdapter
    def parse_item(cls, data, many=False):
        return TypeAdapter(List[cls] if many else cls).validate_python(data)
except ImportError:
    from pydantic import parse_obj_as
    def parse_item(cls, data, many=False):
        return parse_obj_as(List[cls] if many else cls, data)

T = TypeVar("T", bound="StandardModel")

class StandardModel(BaseModel):
    class Config: # v1 호환
        validate_assignment = True
        extra = "allow"
    
    model_config = {"validate_assignment": True, "extra": "allow"} # v2 호환

    @classmethod
    def from_auto(cls: Type[T], data: Any) -> Union[T, List[T], Dict[str, T]]:
        """데이터 구조를 판별하여 고속 파싱 및 ID 바인딩"""
        if isinstance(data, list): return parse_item(cls, data, many=True)
        if isinstance(data, dict):
            # Nested Dict(Map) 구조 판별
            first_val = next(iter(data.values())) if data else None
            if isinstance(first_val, dict):
                res = {}
                for k, v in data.items():
                    if k == "default" or not k.isdigit(): continue
                    v_copy = v.copy(); v_copy["id"] = int(k) # Key-ID 매핑
                    res[k] = parse_item(cls, v_copy)
                return res
            return parse_item(cls, data)
        return parse_item(cls, data)