
from pydantic import ValidationError
from battery.models import CellRow

def load_cells(path: str) -> list[CellRow]:
    rows = []  # 결과를 담을 빈 리스트

    with open(path, "r", encoding="utf-8") as f:  # "r" = 읽기 모드

        # readline() = 한 줄만 읽음 → 첫 줄(헤더)을 먼저 꺼냄
        # .strip() =  ("temp\n" → "temp")
        header = f.readline().strip().split(",")

        for line in f:
            values = line.strip().split(",")

            # zip(a, b) = 두 리스트를 짝지음 → [("cell_id","CELL-001"), ...]
            # dict(...) = 그 짝들을 dict로 → {"cell_id":"CELL-001", ...}
            row = dict(zip(header, values))

            try:
                cell_row = CellRow(**row)
            except ValidationError:
                continue

            rows.append(cell_row)  # 리스트에 추가. Java의 list.add()

    return rows