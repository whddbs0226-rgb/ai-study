from api.errors import register_error_handlers
from api.deps import SettingsDep
from api.errors import AppError
from api.schemas import CellCreate, CellResponse
from fastapi import HTTPException, FastAPI, status

app = FastAPI()
register_error_handlers(app)

@app.get("/")
async def root():
    return {"message": "hello"}

@app.get("/cells")
async def list_cells(limit: int = 10, order: str = "asc"):
    # 경로에 없는 인자 = 쿼리 파라미터
    # /cells?limit=5&order=desc
    return {"limit": limit, "order": order}


# 메모리 저장소 (DB는 Week 6에서)
_store: dict[str, CellResponse] = {}

@app.post("/cells", response_model=CellResponse, status_code=status.HTTP_201_CREATED)
async def create_cell(payload: CellCreate) -> CellResponse:
    if payload.cell_id in _store:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이미 존재하는 셀입니다: {payload.cell_id}",
        )

    cell = CellResponse(
        cell_id=payload.cell_id,
        voltage=payload.voltage,
        temp=payload.temp,
        status="정상" if 3.0 <= payload.voltage <= 4.2 else "이상",
    )
    _store[cell.cell_id] = cell
    return cell

from battery.loader import load_cells
from battery.analyzer import report, avg_voltage_by_cell, max_temp_by_cell

@app.get("/cells/{cell_id}/stats")
async def cell_stats(cell_id: str):
    """해당 셀의 평균 전압, 최고 온도 반환. 없는 셀이면 404"""
    
    data = load_cells("cells.csv")
    avg_map = avg_voltage_by_cell(data)
    max_temp_map = max_temp_by_cell(data)

    


    if cell_id not in avg_map or cell_id not in max_temp_map:
        # raise HTTPException(status_code=404, detail="Cell not found")
        raise AppError("CELL_NOT_FOUND", f"셀을 찾을 수 없습니다: {cell_id}", 404)

    return {
        "avg_map": avg_map[cell_id], 
        "max_temp": max_temp_map[cell_id]
    }

# 사용
@app.get("/cells/{cell_id}")
async def get_cell(cell_id: str) -> CellResponse:
    cell = _store.get(cell_id)
    if cell is None:
        raise AppError("CELL_NOT_FOUND", f"셀을 찾을 수 없습니다: {cell_id}", 404)
    return cell

@app.get("/report")
async def get_report(settings: SettingsDep):
    data = load_cells(settings.csv_path)
    return {"report": report(data)}