import asyncio, os, httpx
from dotenv import load_dotenv
load_dotenv()

async def test_model(model_name):
    key = os.environ.get("GROQ_API_KEY")
    print(f"Testing {model_name}...")
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": "What is 2+2? Answer in one word."}],
                "max_tokens": 10
            }
        )
        print("Status:", resp.status_code)
        if resp.status_code == 200:
            print("Response:", resp.json()["choices"][0]["message"]["content"])
        else:
            print("Error:", resp.text)

if __name__ == "__main__":
    asyncio.run(test_model("qwen/qwen3.8-27b"))
