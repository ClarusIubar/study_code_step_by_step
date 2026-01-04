from typing import TypeVar, Type, Dict, Any, Generic, Iterable
from practice import Product, Staff
from validate import StandardModel

T = TypeVar("T", bound=StandardModel)

class SmartQuerySet(Generic[T]): # fluent interface
    """[Query] 개발 편의성을 위한 스마트 프로젝션 엔진"""
    def __init__(self, items: Iterable[T] = None):
        self._items = list(items) if items else []

    def __getattr__(self, key: str) -> 'SmartQuerySet':
        if not self._items: return SmartQuerySet()
        try:
            return SmartQuerySet([getattr(item, key) for item in self._items])
        except AttributeError:
            raise AttributeError(f"속성 '{key}'를 찾을 수 없습니다.")

    def filter(self, func) -> 'SmartQuerySet[T]':
        return SmartQuerySet([item for item in self._items if func(item)])

    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __getitem__(self, idx): return self._items[idx]
    def __str__(self): return ", ".join(map(str, self._items))
    def __repr__(self): return f"SmartQuerySet({self._items}) <Count: {len(self._items)}>"


class MartRepository: # CQRS
    """[Command/Storage] CQRS를 지키기 위한 타입 기반 저장소"""
    def __init__(self):
        self._storage: Dict[Type[StandardModel], Dict[str, Any]] = {}

    def save_many(self, items: Iterable[StandardModel]):
        for item in items:
            t = type(item)
            if t not in self._storage: self._storage[t] = {}
            self._storage[t][item.name] = item

    def get_all(self, cls: Type[T]) -> list[T]:
        return list(self._storage.get(cls, {}).values())

    def find_by_name(self, cls: Type[T], name: str) -> T:
        return self._storage.get(cls, {}).get(name)

    def delete(self, cls: Type[T], name: str) -> bool:
        if cls in self._storage:
            return self._storage[cls].pop(name, None) is not None
        return False


class WookjaeMart: # MartServiceFacade
    """[Business Logic] 비즈니스 로직을 수행하는 통합 인터페이스"""
    def __init__(self, products: list[Product], staffs: list[Staff]):
        self._repository = MartRepository()
        self._repository.save_many(products)
        self._repository.save_many(staffs)

    @property
    def products(self) -> SmartQuerySet[Product]:
        return SmartQuerySet(self._repository.get_all(Product))

    @property
    def staffs(self) -> SmartQuerySet[Staff]:
        return SmartQuerySet(self._repository.get_all(Staff))

    def find_product(self, name: str) -> Product:
        return self._repository.find_by_name(Product, name)

    def find_staff(self, name: str) -> Staff:
        return self._repository.find_by_name(Staff, name)

    def get_low_stock_products(self, threshold: int) -> SmartQuerySet[Product]:
        """비즈니스 정책: 재고 부족 상품 필터링"""
        return self.products.filter(lambda p: p.stock < threshold)