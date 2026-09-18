from battery.loader import load_cells
from battery.analyzer import report

def main() -> None:
    data = load_cells("cells.csv")
    for line in report(data):
        print(line)


# 파이썬은 import만 해도 파일 전체가 실행되기 때문에 __str__ 은 이 파일이 직접 실행될 때만 실행
# ex) import main -> 실행안됨 | python main.py -> 실행됨
if __name__ == "__main__":
    main()