from battery.models import CellRow
from utils import to_float

def cell_ids(rows: list[CellRow]) -> list[str]:
    """등장하는 셀 ID 목록을 정렬해서 반환 (중복 제거)"""
    id_list = []

    for row in rows:
        id_list.append(row.cell_id)
    return sorted(set(id_list))


def avg_voltage_by_cell(rows: list[CellRow]) -> dict[str, float]:
    """셀별 평균 전압. {"CELL-001": 3.72, ...} 형태"""
    cell_data = {}
    result = {}
    for row in rows:
        
        cell_id = row.cell_id
        voltage = to_float(row.voltage)

        if cell_id not in cell_data:
            cell_data[cell_id] = [0.0, 0]

        cell_data[cell_id][0] += voltage
        cell_data[cell_id][1] += 1
    
    for cell_id, (total, count) in cell_data.items():
        result[cell_id] = round(total / count, 3)
        
    return result


def max_temp_by_cell(rows: list[CellRow]) -> dict[str, float]:
    """셀별 최고 온도. {"CELL-001": 44.2, ...} 형태"""
    cell_data = {}
    result = {}

    for row in rows:
        
        cell_id = row.cell_id
        temperature = to_float(row.temp)

        if cell_id not in cell_data:
            cell_data[cell_id] = []

        cell_data[cell_id].append(temperature)
    
    for cell_id, temperature in cell_data.items():
        high_temperature = max(temperature)
        result[cell_id] = high_temperature
        
    return result


def abnormal_rows(rows: list[CellRow], high: float = 4.2, low : float = 3.0) -> list[CellRow]:
    """전압이 범위를 벗어난 행 리스트"""

    cell_list = []
    for row in rows:
        voltage = to_float(row.voltage)

        if not low <= voltage <= high:
            cell_list.append(row)
       
    return cell_list


def report(rows: list[CellRow]) -> list[str]:
    """문자열 리스트 반환
    ["CELL-001 | 평균 3.721V | 최고온도 44.2C | 이상 3건", ...]
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
            if abnormal_data.cell_id == cell:
                abnormal_count += 1
        
        result = f"{cell} | 평균 {cell_avg:.3f}V | 최고온도 {max_temp} | 이상 {abnormal_count} 건"
        result_list.append(result)

    return result_list
