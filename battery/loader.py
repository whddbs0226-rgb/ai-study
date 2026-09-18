
def load_cells(path):
    rows = []  # 결과를 담을 빈 리스트

    with open(path, "r", encoding="utf-8") as f:  # "r" = 읽기 모드

        # readline() = 한 줄만 읽음 → 첫 줄(헤더)을 먼저 꺼냄
        # .strip() = 앞뒤 공백·개행 제거 ("temp\n" → "temp")
        # .split(",") = 쉼표로 자름 → ["timestamp","cell_id",...]
        header = f.readline().strip().split(",")

        # 파일 객체를 for로 돌리면 남은 줄을 한 줄씩 순회 (헤더는 위에서 이미 소비됨)
        for line in f:
            values = line.strip().split(",")  # 데이터 한 줄을 리스트로

            # zip(a, b) = 두 리스트를 짝지음 → [("cell_id","CELL-001"), ...]
            # dict(...) = 그 짝들을 dict로 → {"cell_id":"CELL-001", ...}
            row = dict(zip(header, values))

            rows.append(row)  # 리스트에 추가. Java의 list.add()

    return rows