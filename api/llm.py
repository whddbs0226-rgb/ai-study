# api/llm.py
import os
import httpx
from dotenv import load_dotenv
from api.errors import AppError

load_dotenv()
KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
HEADERS = {"x-goog-api-key": KEY, "Content-Type": "application/json"}
    
async def ask_llm(question: str, system: str | None = None) -> tuple[str, int]:
    """질문을 보내고 (답변, 사용토큰수) 반환"""

    try:
        payload: set[dict[str, dict[str, list[dict[str, str]]]] | list[dict[str, list[dict[str, str]] | str]] | str | None] = {
            "contents": [{"role": "user", "parts": [{"text": question}]}]} 
        if system:
            payload["system_instruction"] = {"parts": [{"text": system}]}
            
        async with httpx.AsyncClient() as client:
            r = await client.post(URL, headers=HEADERS, json=payload, timeout=30.0)
            r.raise_for_status()          # 4xx/5xx면 예외 발생
        
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"], data["usageMetadata"]["totalTokenCount"]

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

    
    # 1. payload 조립 (system이 있으면 system_instruction 추가)
    # 2. httpx.AsyncClient로 POST
    # 3. 상태 코드 확인 → 에러면 AppError
    # 4. 응답에서 text와 totalTokenCount 꺼내서 반환
    ...

if __name__ == "__main__":
    import asyncio
    print(asyncio.run(ask_llm("배터리 셀 전압이 4.3V면 정상인가요?")))