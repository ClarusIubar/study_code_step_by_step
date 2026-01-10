from typing import TypeVar, Dict, List, Generic
from core.model import StandardModel

T = TypeVar("T", bound=StandardModel)

class InventoryRepository(Generic[T]):
    def __init__(self):
        self._storage: Dict[int, T] = {}

    def save(self, item: T):
        self._storage[item.id] = item

    def find_by_id(self, item_id: int) -> T:
        return self._storage.get(item_id)

    def get_all(self) -> List[T]:
        return sorted(self._storage.values(), key=lambda x: x.id)