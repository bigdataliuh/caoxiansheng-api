from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ 启用跨域支持
import requests
import os

app = Flask(__name__)
CORS(app)

# 从环境变量中获取 API Key 和 应用 ID
API_KEY = os.getenv("API_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

# 获取 chat_id，用于上下文记忆
def get_chat_id():
    url = f"https://xzs.njwenshu.com/api/application/{APPLICATION_ID}/chat/open"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("data")

# 问答接口
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
    # Railway 默认监听 5000 端口
    app.run(host="0.0.0.0", port=5000)
