print("hellO")

name = "battery"
count = 3

print(f"{name} cell count: {count}")

cells = [3.7, 3.8, 3.65]
for c in cells:
    print(c)

print(f"len: {len(cells)}")
print(f"avg: {sum(cells) / len(cells)}")