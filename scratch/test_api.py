import urllib.request
import json

url = "http://127.0.0.1:5000/api/chat"
payload = {
    "message": "Tell me about Akhil RAG project",
    "conversation_id": "session_123"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        print("API Response Success!")
        print(json.dumps(res_data, indent=2))
except Exception as e:
    print(f"Error: {e}")
