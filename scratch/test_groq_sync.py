import os, json, urllib.request, urllib.error
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get("GROQ_API_KEY")
print("Key exists:", bool(key))
model = os.environ.get("LLM_MODEL", "llama-3.1-8b-instant")
print("Model:", model)

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}
payload = {
    "model": model,
    "messages": [{"role": "user", "content": "Say hello in 3 words"}],
    "max_tokens": 50
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
try:
    print("Sending request to Groq...")
    with urllib.request.urlopen(req, timeout=10) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        print("Response received successfully!")
        print("Content:", res_data["choices"][0]["message"]["content"])
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.reason, e.read().decode("utf-8"))
except Exception as e:
    print("Exception:", type(e), e)
