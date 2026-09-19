from pydantic import ValidationError
from pydantic import BaseModel, Field

class Cell(BaseModel):
    cell_id: str
    voltage: float = Field(ge=0.0, le=5.0)      # ge = 이상, le = 이하
    temp: float = Field(ge=-40.0, le=100.0)
    soc: int | None = None                       # 기본값 있으면 선택 필드
    tags: list[str] = []                         # 리스트도 됨


c = Cell(cell_id="C1", voltage=3.7, temp=28.4)
print(c.soc, c.tags)

try:
    Cell(cell_id="C2", voltage=99.0, temp=28.4)   # 범위 초과
except ValidationError as e:
    print(e)


class Module(BaseModel):
    module_id: str
    cells: list[Cell]

m = Module(module_id="MOD-01", cells=[
    {"cell_id": "C1", "voltage": "3.7", "temp" : "28.4"},   # volatge "str" 로 넘겨도 자동 치환됨 (pydantic)
    {"cell_id": "C2", "voltage": "3.9", "temp" : "30.1"},
])

print(m.cells[0].voltage, type(m.cells[0]))

print(m.model_dump())        # → dict
print(m.model_dump_json())   # → JSON 문자열

# 역방향
data = {"module_id": "MOD-02", "cells": [{"cell_id": "C9", "voltage": 4.0, "temp": 25.0}]}
m2 = Module(**data)          # ** 는 목요일에 배운 그 언패킹
print(m2)

json_str = '{"module_id": "MOD-03", "cells": []}'
m3 = Module.model_validate_json(json_str)
print(m3)