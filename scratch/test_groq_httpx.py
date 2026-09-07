import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

async def test():
    try:
        import httpx
        key = os.environ.get("GROQ_API_KEY")
        model = os.environ.get("LLM_MODEL", "llama-3.1-8b-instant")
        print(f"Testing httpx to Groq with model: {model}, key prefix: {key[:8] if key else 'None'}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": "What is 2+2? Answer in one word."}],
                    "max_tokens": 10
                }
            )
            print("Status Code:", resp.status_code)
            print("Response:", resp.json())
    except Exception as e:
        print("Error with httpx:", type(e), e)

if __name__ == "__main__":
    asyncio.run(test())
