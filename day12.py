# day12.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# 클라이언트 생성 — 키를 한 번만 넘기면 됨
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# res = client.models.generate_content(
#     model=MODEL,
#     contents="배터리 셀 전압이 4.3V면 정상인가요? 한 문장으로.",
# )

# print(res.text)                              # 답변 바로 꺼내짐
# if res.usage_metadata:
#     print(res.usage_metadata.total_token_count)  # 토큰도 속성으로


# 스트리밍 버전 (답변이 한번에 생성되지 않고 조금씩 생성됨)
stream = client.models.generate_content_stream(
    model=MODEL,
    contents="리튬이온 배터리의 충전 원리를 세 문단으로 설명해줘",
)

# for chunk in stream:
#     print(chunk.text, end="", flush=True)   # 텍스트 조각을 모음 (end: 줄바꿈 안함)
# print()


# 비동기 버전 (답변을 한번에 응답함)
import asyncio

async def stream_answer(question: str) -> None:
    stream = await client.aio.models.generate_content_stream(
        model=MODEL,
        contents=question,
    )
    async for chunk in stream:
        print(chunk.text, end="", flush=True)
    print()

asyncio.run(stream_answer("SOC와 SOH의 차이를 설명해줘"))