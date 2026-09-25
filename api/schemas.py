from pydantic import BaseModel, Field

class CellCreate(BaseModel):
    cell_id: str = Field(min_length=1, max_length=20)
    voltage: float = Field(ge=0.0, le=5.0)
    temp: float = Field(ge=-40.0, le=100.0)

class CellResponse(BaseModel):
    cell_id: str
    voltage: float
    temp: float
    status: str