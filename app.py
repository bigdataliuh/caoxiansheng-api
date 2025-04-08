
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

def get_chat_id():
    url = f"https://xzs.njwenshu.com/api/application/{APPLICATION_ID}/chat/open"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("data")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    chat_id = data.get("chat_id") or get_chat_id()

    payload = {
        "message": question,
        "re_chat": False,
        "stream": False
    }
    url = f"https://xzs.njwenshu.com/api/application/chat_message/{chat_id}"
    res = requests.post(url, headers=HEADERS, json=payload)
    try:
        answer = res.json().get("data", {}).get("content")
    except:
        answer = "❌ 解析失败"

    return jsonify({
        "answer": answer,
        "chat_id": chat_id
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway 会注入 PORT 环境变量
    app.run(host="0.0.0.0", port=port)

