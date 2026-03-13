from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_KEY = "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"

@app.route("/")
def home():
    return "AI Lyrics API running"

@app.route("/lyrics", methods=["POST"])
def lyrics():

    data = request.json

    style = data.get("style", "")
    vocal = data.get("vocal", "")
    theme = data.get("theme", "")

    prompt = f"""
3분 정도 길이의 노래 가사를 만들어줘.

구조:
1절 4줄
후렴 4줄
2절 4줄
후렴 4줄

스타일: {style}
보컬: {vocal}
주제: {theme}

가사만 출력해라.
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9
        }
    )

    result = response.json()

    lyrics = result["choices"][0]["message"]["content"]

    return jsonify({"lyrics": lyrics})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
