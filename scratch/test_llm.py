import asyncio
from dotenv import load_dotenv
load_dotenv()
from chatbot.llm.client import LLMClient

async def main():
    client = LLMClient()
    print("Testing model:", client.model)
    print("API Key prefix:", client.api_key[:10] if client.api_key else "None")
    
    print("\n--- Direct Groq Test ---")
    try:
        async for token in client._stream_groq("What is your model name? Answer in one sentence.", client.api_key):
            print(token, end="", flush=True)
        print("\n[Groq Success!]")
    except Exception as e:
        print(f"\n[Groq Error]: {e}")

    print("\n--- generate_stream Test ---")
    async for token in client.generate_stream("What is Akhil's role?", "Akhil is a Data Scientist and AI Engineer."):
        print(token, end="", flush=True)
    print("\n[Stream Test Done]")

if __name__ == "__main__":
    asyncio.run(main())
