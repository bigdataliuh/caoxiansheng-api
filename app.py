from flask import Flask, request, Response
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "https://lambent-froyo-cb1103.netlify.app"}})

API_KEY = "application-d1c45598abb5d6f3a859031fa595d950"
FIXED_CHAT_ID = "a2b766a6-24d7-11f0-bb3e-0242ac110002"
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    payload = {
        "message": question,
        "re_chat": False,
        "stream": True
    }

    url = f"https://xzs.njwenshu.com/api/application/chat_message/{FIXED_CHAT_ID}"
    upstream = requests.post(url, headers=HEADERS, json=payload, stream=True)

    def generate():
        for line in upstream.iter_lines():
            if line:
                try:
                    obj = json.loads(line.decode("utf-8"))
                    token = obj.get("reasoning_content", "")
                    if token:
                        yield f"data: {token}\n\n"
                except Exception as e:
                    print("解析错误：", e)

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
