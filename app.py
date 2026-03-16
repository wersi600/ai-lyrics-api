from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

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
3분30초 정도 길이의 노래 가사를 만들어줘.
반드시 다음 형식으로 작성해라.

1절 4줄
후렴 4줄
2절 4줄
후렴 4줄

각 구간은 줄바꿈으로 구분한다.
가사만 출력하고 JSON 형식, 설명, 제목, 따옴표, 코드블록 없이 순수 가사만 작성해라.
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

    title = lyrics.split("\n")[0]

    return jsonify({
        "title": title,
        "lyrics": lyrics
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
