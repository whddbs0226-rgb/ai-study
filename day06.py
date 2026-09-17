#타입 힌트
# 변수에 타입 표기: 변수명: 타입 = 값
cell_id: str = "CELL-001"
voltage: float = 3.7
count: int = 5
is_charging: bool = True

# 함수: 인자는 (이름: 타입), 반환값은 -> 타입
def check_voltage(voltage: float) -> str:
    if voltage > 4.2:
        return "과전압"
    return "정상"


# 반환값이 없으면 -> None
def log_cell(cell_id: str) -> None:
    print(f"[LOG] {cell_id}")


print(check_voltage(4.3))
log_cell("CELL-001")


#컬렉션과 특수 타입
# 리스트: list[원소타입]
voltages: list[float] = [3.7, 3.8, 3.65]
cell_names: list[str] = ["CELL-001", "CELL-002"]

# dict: dict[키타입, 값타입]
avg_map: dict[str, float] = {"CELL-001": 3.72}

# 중첩도 됩니다. 어제 load_cells가 반환한 게 이 모양
rows: list[dict[str, str]] = [{"cell_id": "CELL-001", "voltage": "3.7"}]

# 튜플: 길이와 각 자리 타입을 다 적음
point: tuple[float, float] = (3.7, 28.4)

# set
ids: set[str] = {"CELL-001", "CELL-002"}