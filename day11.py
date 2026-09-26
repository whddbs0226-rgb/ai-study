import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
HEADERS = {"x-goog-api-key": KEY, "Content-Type": "application/json"}

# 요청 본문. 이게 LLM API의 전부입니다
payload = {
    "contents": [
        {"role": "user", "parts": [{"text": "배터리 셀 전압이 4.3V면 정상인가요? 한 문장으로."}]}
    ]
}

res = httpx.post(URL, headers=HEADERS, json=payload, timeout=30.0)
print(res.status_code)

if res.status_code != 200:
    print(res.text)
    raise SystemExit          # 여기서 멈춤. KeyError 안 남

data = res.json()
#print(json.dumps(data, ensure_ascii=False, indent=2))
# print("\n답변:", data["candidates"][0]["content"]["parts"][0]["text"])
# print("토큰:", data["usageMetadata"]["totalTokenCount"])


# 대화 이력과 system 지시
payload = {
    "system_instruction": { # 역할과 규칙
        "parts": [{"text": "당신은 배터리 설비 진단 전문가입니다. 간결하게 답하세요."}]
    },
    "contents": [
        {"role": "user",  "parts": [{"text": "3번 셀 전압이 4.35V입니다"}]},
        {"role": "model", "parts": [{"text": "과전압입니다. 즉시 충전을 중단하세요."}]},
        {"role": "user",  "parts": [{"text": "온도는요?"}]},
    ],
    "generationConfig": {
        "temperature": 0.2,      # 0에 가까울수록 일관, 2에 가까울수록 다양
        "maxOutputTokens": 200,  # 응답 길이 제한 = 비용 방어
    },
}

res = httpx.post(URL, headers=HEADERS, json=payload, timeout=30.0)

print(res.status_code)

if res.status_code != 200:
    print(res.text)
    raise SystemExit          # 여기서 멈춤. KeyError 안 남

data = res.json()
#print(json.dumps(data, ensure_ascii=False, indent=2))
# print("\n답변2:", data["candidates"][0]["content"]["parts"][0]["text"])
# print("토큰2:", data["usageMetadata"]["totalTokenCount"])


# 비동기 병렬 호출
import asyncio
import time


async def ask(client: httpx.AsyncClient, question: str) -> str:
    payload = {"contents": [{"role": "user", "parts": [{"text": question}]}]}
    r = await client.post(URL, headers=HEADERS, json=payload, timeout=30.0)
    r.raise_for_status()          # 4xx/5xx면 예외 발생
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]


async def main() -> None:
    questions = [
        "리튬이온 셀의 정상 전압 범위는?",
        "셀 온도가 60도면 어떤 문제인가?",
        "SOC는 무엇의 약자인가?",
    ]

    async with httpx.AsyncClient() as client:
        start = time.time()
        for q in questions:
            await ask(client, q)
        print(f"순차: {time.time() - start:.1f}초")

        start = time.time()
        results = await asyncio.gather(*[ask(client, q) for q in questions])
        print(f"병렬: {time.time() - start:.1f}초")

        for r in results:
            print("-", r[:60])

# asyncio.run(main())



from api.errors import AppError     # 어제 만든 것


async def ask_safe(client: httpx.AsyncClient, question: str) -> str:
    try:
        payload = {"contents": [{"role": "user", "parts": [{"text": question}]}]}
        r = await client.post(URL, headers=HEADERS, json=payload, timeout=30.0)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

    except httpx.TimeoutException:
        raise AppError("LLM_TIMEOUT", "응답 시간 초과", 504)

    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if code == 429:
            raise AppError("LLM_RATE_LIMIT", "요청 한도 초과", 429)
        if code in (401, 403):
            raise AppError("LLM_AUTH", "API 키가 유효하지 않습니다", 500)
        raise AppError("LLM_ERROR", f"LLM 호출 실패: {code}", 502)

    except (KeyError, IndexError):
        raise AppError("LLM_NO_RESPONSE", "응답을 생성하지 못했습니다", 502)