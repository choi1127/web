import requests
import json

url = "http://ictrobot.hknu.ac.kr:11434/api/chat"

payload = {
    "model": "llama3.1",
    "messages": [
        {"role": "user", "content": "API에 대해 알려줘."}
    ]
}

res = requests.post(url, json=payload, stream=True)

for line in res.iter_lines():
    if line:
        data = json.loads(line.decode())
        if "message" in data:
            print(data["message"]["content"], end="", flush=True)