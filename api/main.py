from fastapi import HTTPException
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello"}

@app.get("/cells/{cell_id}")
async def list_cells(limit: int = 10, order: str = "asc"):
    # 경로에 없는 인자 = 쿼리 파라미터
    # /cells?limit=5&order=desc
    return {"limit": limit, "order": order}



from pydantic import BaseModel, Field

class CellCreate(BaseModel):                     # 요청 본문 스키마
    cell_id: str
    voltage: float = Field(ge=0.0, le=5.0)
    temp: float

class CellResponse(BaseModel):                   # 응답 스키마
    cell_id: str
    voltage: float
    status: str

@app.post("/cells", response_model=CellResponse)    # response_model 사용하여 검증
async def create_cell(cell: CellCreate):         # 인자 타입이 pydantic 모델 = 요청 본문
    status = "정상" if 3.0 <= cell.voltage <= 4.2 else "이상"
    return CellResponse(
        cell_id=cell.cell_id,
        voltage=cell.voltage,
        status=status,
    )

from battery.loader import load_cells
from battery.analyzer import report, avg_voltage_by_cell, max_temp_by_cell

@app.get("/report")
async def get_report():
    """load_cells + report를 호출해서 결과 반환"""
    data = load_cells("cells.csv")
    return {"report": report(data)}


@app.get("/cells/{cell_id}/stats")
async def cell_stats(cell_id: str):
    """해당 셀의 평균 전압, 최고 온도 반환. 없는 셀이면 404"""
    
    data = load_cells("cells.csv")
    avg_map = avg_voltage_by_cell(data)
    max_temp_map = max_temp_by_cell(data)


    if cell_id not in avg_map or cell_id not in max_temp_map:
        raise HTTPException(status_code=404, detail="Cell not found")

    return {
        "avg_map": avg_map[cell_id], 
        "max_temp": max_temp_map[cell_id]
    }