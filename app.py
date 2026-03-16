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
    theme = data.get("theme", "")
    vocal = data.get("vocal", "")

    prompt = f"""
{style} 스타일의 3분30초 정도 길이의 노래 가사를 만들어라.

주제: {theme}
보컬: {vocal}

출력 형식

제목:
(노래 제목)

가사:
1절 4줄
후렴 4줄
2절 4줄
후렴 4줄

설명 없이 출력해라.
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

    text = result["choices"][0]["message"]["content"]

    parts = text.split("가사:")

    title = parts[0].replace("제목:", "").strip()
    lyrics = parts[1].strip()

    # Suno용 구조 변환
    lyrics = lyrics.replace("1절", "[Verse 1]")
    lyrics = lyrics.replace("2절", "[Verse 2]")
    lyrics = lyrics.replace("후렴", "[Chorus]")

    return jsonify({
        "title": title,
        "lyrics": lyrics
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
