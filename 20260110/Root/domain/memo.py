from pydantic import Field
from core.model import StandardModel

class Memo(StandardModel):
    id: int = Field(ge=1, le=9)
    title: str = ""