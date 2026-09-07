import urllib.request
import json

url = "http://127.0.0.1:5000/api/chat/stream"
payload = {
    "message": "What skills does Akhil have?",
    "conversation_id": "stream_demo_1"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

print("--- Testing SSE Stream Response ---")
try:
    with urllib.request.urlopen(req) as resp:
        for line in resp:
            line_str = line.decode("utf-8").strip()
            if line_str:
                print(line_str)
except Exception as e:
    print(f"Error: {e}")
