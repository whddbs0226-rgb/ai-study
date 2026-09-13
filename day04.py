# 함수와 기본 인자
def check_voltage(voltage):
    if voltage > 4.0:
        return "과전압"
    elif voltage < 3.0:
        return "저전압"
    return "정상"

print(check_voltage(4.2))

# 기본 값이 있는 인자
def format_cell(cell_id, unit="V", decimals=2):
    return f"{cell_id} ({unit}, {decimals}자리)"

print (format_cell("CELL_001"))
print (format_cell("CELL_001", "mv"))
print (format_cell("CELL_001", decimals=3))

# 여러값 반환
def analyze(cells):
    return min(cells), max(cells), sum(cells) / len(cells)

lo, hi, avg = analyze([3.7, 3.8, 3.65, 4.1])
print(f"min={lo} max={hi} avg={avg:.3f}")

# 튜플의 반환
def total(*values):
    print(type(values), values) # 튜플 타입
    return sum(values)

print(total(1, 2, 3))
print(total(1, 2, 3, 4, 5))


def make_cell(**fields):
    print(type(fields), fields) # dict 타입 (json과 유사)
    return fields

c = make_cell(id="CELL-001", voltage=3.7, temp=28.4)
print(c)

# 예외처리
def parse_voltage(raw):
    try:
        v = float(raw)
        return v
    except ValueError:  #value가 없을 떄
        print(f"변환 실패: {raw}")
        return None
    finally:
        print("검사 종료")

print(parse_voltage("3.7"))
print(parse_voltage("abc"))


# 예외처리
cells = {"CELL-001": 3.7}

def get_voltage(cell_id):
    try:
        return cells[cell_id]
    except KeyError:    # 키가 없을 떄
        return None

print(get_voltage("CELL-999"))

# 직접 예외 처리
def set_voltage(v):
    if v < 0:
        raise ValueError(f"전압은 음수일 수 없습니다: {v}")
    return v

try:
    set_voltage(-1)
except ValueError as e:
    print(f"에러: {e}")



def find_abnormal(cells, high=4.0, low= 3.0):
    

    return [
        cell for cell in cells
        if not (low <= float(cell["voltage"]) <= high)
    ];

cell_data = [{"id" : "1", "voltage" : "3.7" }, {"id" : "2", "voltage" : "4.2" }, {"id" : "3", "voltage" : "2.5" }]

print (find_abnormal(cell_data))

    