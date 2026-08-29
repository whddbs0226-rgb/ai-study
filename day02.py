count = 3
count = "three"
count = 3.7

print(count, type(count))

voltage = 3.7
cell_id = "CELL_001"
is_charging = True
error = None

print(type(voltage), type(cell_id), type(is_charging), type(error))


cell_id = "CELL-001"
voltage = 3.7521
temp = 28.4

print("cell: " + cell_id + ", voltage: " + str(voltage))
print("cell: {}, voltage: {}".format(cell_id, voltage))
print(f"cell: {cell_id}, voltage: {voltage}")

print(f"voltage: {voltage:.2f}V")
print(f"temp: {temp:>10}")
print(f"cell {cell_id:<12} | {voltage:.3f}V")
print(f"계산: {voltage * 3:.2f}")

cells = [3.7, 3.8, 3.65, 4.1]

for c in cells:
    if c > 4.0:
        print(f"{c} 과전압")
    else:
        print(f"{c} 정상")
print("검사 완료")

# Java vs Python
# 1. 변수 선언: String s = "a";  →  s = "a"   (타입 없음)
# 2. 세미콜론: 필요  →  불필요
# 3. 블록: { }  →  들여쓰기
# 4. null  →  None
# 5. String.format()  →  f"{변수}"
# 6. 타입 검사: 컴파일 시점  →  실행 시점