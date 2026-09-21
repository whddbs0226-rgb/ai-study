import time

def fetch(name: str) -> str:
    print(f"{name} 시작")
    time.sleep(2)
    print(f"{name} 완료")
    return f"{name} 결과"

start = time.time()
# fetch("셀1")
# fetch("셀2")
# fetch("셀3")

# print(f"총 {time.time() - start:.1f} 초")


import asyncio

async def fetch_async(name: str) -> str:
    print(f"{name} 시작")
    await asyncio.sleep(2)       # time.sleep이 아님. 주의
    print(f"{name} 완료")
    return f"{name} 결과"


async def main() -> None:
    start = time.time()
    results = await asyncio.gather(
        fetch_async("셀1"),
        fetch_async("셀2"),
        fetch_async("셀3"),
    )
    print(results)
    print(f"총 {time.time() - start:.1f}초")

# asyncio.run(main())




# async def = 코루틴 함수
async def get_voltage(cell_id: str) -> float:
    await asyncio.sleep(0.1)
    return 3.7


# 호출만 하면 실행이 안 됩니다
coro = get_voltage("C1")
print(coro)              # <coroutine object ...>  ← 결과가 아님

# await를 붙여야 실행되고 결과가 나옴
async def main():
    v = await get_voltage("C1")
    print(v)             # 3.7

asyncio.run(main())


async def main():
    # 순차 — 하나 끝나야 다음
    a = await get_voltage("C1")
    b = await get_voltage("C2")

    # 동시 — 한꺼번에
    a, b = await asyncio.gather(
        get_voltage("C1"),
        get_voltage("C2"),
    )

    # 리스트로 넘길 때 (문서 30개 처리 같은 경우)
    ids = ["C1", "C2", "C3", "C4", "C5"]
    results = await asyncio.gather(*[get_voltage(i) for i in ids])
    print(results)

asyncio.run(main())




async def slow() -> str:
    await asyncio.sleep(10)
    return "완료"


async def main():
    try:
        r = await asyncio.wait_for(slow(), timeout=2.0)
        print(r)
    except asyncio.TimeoutError:
        print("시간 초과")

asyncio.run(main())