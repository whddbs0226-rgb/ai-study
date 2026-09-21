import asyncio, time

async def fetch_cell_status(cell_id: str) -> dict[str, str | float]:
    """외부 API 호출을 흉내 (0.5초 대기 후 더미 데이터 반환)"""
    await asyncio.sleep(0.5)
    return {"cell_id" : cell_id}


async def fetch_all(cell_ids: list[str]) -> list[dict[str, str | float]]:
    """여러 셀을 동시에 조회"""
    return await asyncio.gather(*[fetch_cell_status(i) for i in cell_ids])

cell_ids = ["1", "2", "3", "4"]

async def main():
    a = await fetch_cell_status("5")
    print(a)

    start = time.time()
    b = await fetch_all(cell_ids)
    print(b)
    print(f"{time.time() - start:.1f}")



asyncio.run(main())