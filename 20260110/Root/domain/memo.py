from pydantic import Field
from core.model import StandardModel

class Memo(StandardModel):
    id: int = Field(ge=1, le=9) # 메모 가용 영역 1~9번 엄수
    title: str = ""