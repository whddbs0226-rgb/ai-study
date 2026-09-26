from pathlib import Path

# 문자열 대신 Path 객체를 씁니다
p = Path("cells.csv")

#print(p.exists())        # 파일이 있나?  ← 지난주 "파일이 없다" 헤맸을 때 이거면 바로 알았음
#print(p.name)            # cells.csv
#print(p.stem)            # cells (확장자 제외)
#print(p.suffix)          # .csv
#print(p.absolute())      # 전체 경로

# 경로 결합은 / 연산자
data_dir = Path("data")
csv_path = data_dir / "cells.csv"      # data/cells.csv
#print(csv_path)

# 폴더 만들기
out_dir = Path("output")
out_dir.mkdir(exist_ok=True)     # 이미 있어도 에러 안 남

# 파일 읽고 쓰기 — open() 없이 한 줄
Path("test.txt").write_text("hello", encoding="utf-8")
#print(Path("test.txt").read_text(encoding="utf-8"))

# 폴더 안 파일 목록
#for f in Path(".").glob("*.py"):
#    print(f.name)


import json

cell = {"cell_id": "CELL-001", "voltage": 3.7, "tags": ["정상", "충전중"]}

# dict → JSON 문자열
s = json.dumps(cell)
print(s)

# dict → JSON 문자열 변환 시 한글이 \uXXXX로 깨져 나오면 이 옵션
s = json.dumps(cell, ensure_ascii=False, indent=2)
print(s)

# JSON 문자열 → dict
back = json.loads(s)
print(back["voltage"], type(back))



from pathlib import Path

# 쓰기
Path("cell.json").write_text(
    json.dumps(cell, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# 읽기
data = json.loads(Path("cell.json").read_text(encoding="utf-8"))
print(data)


from battery.models import CellRow

# json.loads → 검증 없음. dict가 그대로 나옴
raw = json.loads('{"cell_id":"C1","voltage":"3.7"}')
print(type(raw["voltage"]))        # str  ← 문자열 그대로

# pydantic → 검증 + 변환
raw2 = json.loads('{"timestamp":"2026-12-12","cell_id":"C1","voltage":"3.7", "current":"1", "temp":"12"}')
pyRaw = CellRow.model_validate(raw2)
print(type(pyRaw.voltage)) # float <- 변환됨



#환경변수와 env
import os
from dotenv import load_dotenv

load_dotenv()      # .env 파일을 읽어서 환경변수로 등록

api_key = os.getenv("GOOGLE_API_KEY")
app_env = os.getenv("APP_ENV", "production")     # 없으면 기본값
max_retries = int(os.getenv("MAX_RETRIES", "3")) # 환경변수는 항상 문자열! 변환 필요

print(api_key)
print(app_env, max_retries)

from pydantic_settings import BaseSettings

