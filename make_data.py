import random  # 난수 생성 모듈. Java의 java.util.Random

random.seed(42)  # 시드 고정 → 실행할 때마다 같은 난수가 나옴 (디버깅할 때 결과 재현용)

# with 구문: Java의 try-with-resources. 블록 끝나면 파일이 자동으로 닫힘
# "w" = 쓰기 모드, encoding="utf-8" = Windows에서 한글 깨짐 방지 (항상 붙이세요)
with open("cells.csv", "w", encoding="utf-8") as f:
    f.write("timestamp,cell_id,voltage,current,temp\n")  # 헤더. write는 줄바꿈을 자동으로 안 넣어서 \n 직접 붙임

    for hour in range(24):          # range(24) → 0,1,2,...,23 (24는 포함 안 됨)
        for cell_num in range(1, 6):  # 1,2,3,4,5 (6은 포함 안 됨)

            ts = f"2026-09-14 {hour:02d}:00:00"   # :02d → 2자리 정수, 빈 자리는 0 (9 → "09")
            cell_id = f"CELL-{cell_num:03d}"       # :03d → 3자리 (1 → "001")

            # random.uniform(a, b) = a~b 사이 실수
            # round(값, 자릿수) = 반올림. Java의 Math.round와 달리 자릿수 지정 가능
            voltage = round(random.uniform(3.2, 4.3), 3)
            current = round(random.uniform(-5.0, 5.0), 2)
            temp = round(random.uniform(20.0, 45.0), 1)

            f.write(f"{ts},{cell_id},{voltage},{current},{temp}\n")  # CSV 한 줄 = 쉼표로 이어붙이고 개행

print("cells.csv 생성 완료")



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


data = load_cells("cells.csv")
print(len(data))   # 행 수 확인
print(data[0])     # 첫 행이 어떤 모양인지 눈으로 확인 ← 중요. 값이 전부 문자열입니다



def to_float(value, default=None):
    """문자열을 float로. 실패하면 default 반환"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default 


def cell_ids(rows):
    """등장하는 셀 ID 목록을 정렬해서 반환 (중복 제거)"""
    id_list = []

    for row in rows:
        id_list.append(row['cell_id'])
    return sorted(set(id_list))


def avg_voltage_by_cell(rows):
    """셀별 평균 전압. {"CELL-001": 3.72, ...} 형태"""
    cell_data = {}
    result = {}
    for row in rows:
        
        cell_id = row['cell_id']
        voltage = to_float(row['voltage'])
        if voltage is None:
            continue

        if cell_id not in cell_data:
            cell_data[cell_id] = [0.0, 0]

        cell_data[cell_id][0] += voltage
        cell_data[cell_id][1] += 1
    
    for cell_id, (total, count) in cell_data.items():
        result[cell_id] = round(total / count, 3)
        
    return result


def max_temp_by_cell(rows):
    """셀별 최고 온도. {"CELL-001": 44.2, ...} 형태"""
    cell_data = {}
    result = {}

    for row in rows:
        
        cell_id = row['cell_id']
        temperature = to_float(row['temp'])
        if temperature is None:
            continue

        if cell_id not in cell_data:
            cell_data[cell_id] = []

        cell_data[cell_id].append(temperature)
    
    for cell_id, temperature in cell_data.items():
        high_temperature = max(temperature)
        result[cell_id] = high_temperature
        
    return result


def abnormal_rows(rows, high=4.2, low=3.0):
    """전압이 범위를 벗어난 행 리스트"""

    cell_list = []
    for row in rows:
        voltage = to_float(row['voltage'])
        if voltage is None:
            continue

        if not low <= voltage <= high:
            cell_list.append(row)
       
    return cell_list


def report(rows):
    """아래 형태로 출력
    CELL-001 | 평균 3.721V | 최고온도 44.2C | 이상 3건
    """
    result_list = []
    cell_avg_dict = avg_voltage_by_cell(rows)
    max_temp_dict = max_temp_by_cell(rows)
    abnormal = abnormal_rows(rows)

    for cell in cell_ids(rows):       
        cell_avg = cell_avg_dict[cell]
        max_temp = max_temp_dict[cell]
        abnormal_count = 0
        for abnormal_data in abnormal:
            if abnormal_data['cell_id'] == cell:
                abnormal_count += 1
        
        result = f"{cell} | 평균 {cell_avg}V | 최고온도 {max_temp} | 이상 {abnormal_count} 건"
        result_list.append(result)

    return result_list


print(f"to_float : {to_float(data[0]['voltage'])}")
print(f"cell_ids : {cell_ids(data)}")
print(f"avg_voltage_by_cell : {avg_voltage_by_cell(data)}")
print(f"max_temp_by_cell : {max_temp_by_cell(data)}")
print(f"abnormal_rows : {abnormal_rows(data)}")
print(f"report : {report(data)}")
