from typing import TypeVar, Type, Dict, Any, Generic, Iterable, List
import json
from pyscript import window
from core.model import StandardModel

T = TypeVar("T", bound=StandardModel)

class SmartQuerySet(Generic[T]):
    """[Query] 욱재마트 규격 스마트 프로젝션 엔진"""
    def __init__(self, items: Iterable[T] = None):
        self._items = list(items) if items else []

    def filter(self, func) -> 'SmartQuerySet[T]':
        return SmartQuerySet([item for item in self._items if func(item)])

    def get_all(self) -> List[T]:
        return sorted(self._items, key=lambda x: x.id)

    def __getattr__(self, key: str) -> 'SmartQuerySet':
        if not self._items: return SmartQuerySet()
        try:
            return SmartQuerySet([getattr(item, key) for item in self._items])
        except AttributeError:
            raise AttributeError(f"속성 '{key}'를 찾을 수 없습니다.")

    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __getitem__(self, idx): return self._items[idx]

class VMRepository:
    """[Command/Storage] 타입 기반 CQRS 저장소"""
    STORAGE_KEY = "UKJAE_VM_FINAL_V58"

    def __init__(self):
        self._storage: Dict[Type[StandardModel], Dict[int, Any]] = {}

    def _to_dict(self, obj: Any) -> Dict[str, Any]:
        if hasattr(obj, "model_dump"): return obj.model_dump()
        return obj.dict() if hasattr(obj, "dict") else {}

    def save(self, item: StandardModel):
        t = type(item)
        if t not in self._storage: self._storage[t] = {}
        self._storage[t][item.id] = item

    def find_by_id(self, cls: Type[T], item_id: int) -> T:
        return self._storage.get(cls, {}).get(item_id)

    def get_all(self, cls: Type[T]) -> List[T]:
        return list(self._storage.get(cls, {}).values())

    def persist(self, total_revenue: int):
        data = {
            "total_revenue": total_revenue,
            "entities": {
                cls.__name__: {obj.id: self._to_dict(obj) for obj in objs.values()}
                for cls, objs in self._storage.items()
            }
        }
        window.localStorage.setItem(self.STORAGE_KEY, json.dumps(data))

    def load_persistence(self) -> Dict[str, Any]:
        raw = window.localStorage.getItem(self.STORAGE_KEY)
        return json.loads(raw) if raw else None