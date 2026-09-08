cells = [3.7, 3.8, 3.65, 4.1]

print(cells[0], cells[-1])
print(cells[1:3])
print(len(cells))

cells.append(3.9)
cells.insert(0, 3.5)    # insert(index, elment)
cells.remove(4.1)
print(cells)

print(sorted(cells))
print(max(cells), min(cells), sum(cells))

#####################
cell = {"id": "CELL-001", "voltage": 3.7, "temp": 28.4}
    
print(cell["id"])
print(cell.get("soc"))  # soc가 없으면 None 출력
print(cell.get("soc", 0))   # soc가 없으면 0 출력

cell["soc"] = 87
del cell["temp"]

for key, value in cell.items():
    print(f"{key}: {value}")

print("voltage" in cell)

########################
point = (3.7, 28.4)
v, t = point
print(v, t) # 변수 동시 선언 가능

ids = ["A", "B", "A", "C", "B"]
print(set(ids), len(set(ids)))  # set([]) : 배열의 중복된 문자열을 제거

###########################
cells = [3.7, 3.8, 3.65, 4.1, 3.55]

result = [c * 1000 for c in cells]
high = [c for c in cells if c > 3.7]
labels = [f"{c}V" for c in cells if c > 3.7]

print(result)
print(high)
print(labels)

cell_map = {f"CELL-{i:03d}": v for i, v in enumerate(cells)}
print(cell_map)