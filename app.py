from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "application-d1c45598abb5d6f3a859031fa595d950"
APPLICATION_ID = "007d316a-0897-11f0-bc52-0242ac110002"
FIXED_CHAT_ID = "a2b766a6-24d7-11f0-bb3e-0242ac110002"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "问题不能为空"}), 400

    payload = {
        "message": question,
        "re_chat": False,
        "stream": False  # ✅ 非流式请求
    }

    url = f"https://xzs.njwenshu.com/api/application/chat_message/ {FIXED_CHAT_ID}"
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result.get("data", {}).get("content", "（无返回内容）")

        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
