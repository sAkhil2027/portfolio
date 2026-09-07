import asyncio, os, httpx
from dotenv import load_dotenv
load_dotenv()

async def list_models():
    key = os.environ.get("GROQ_API_KEY")
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {key}"}
        )
        data = resp.json()
        models = [m["id"] for m in data.get("data", [])]
        print("Available Groq models:")
        for m in sorted(models):
            print(" -", m)

if __name__ == "__main__":
    asyncio.run(list_models())
