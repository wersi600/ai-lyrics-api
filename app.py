from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENAI_KEY = "여기에_본인_API_KEY"

@app.route("/lyrics", methods=["POST"])
def lyrics():

    data = request.json

    style = data.get("style","")
    vocal = data.get("vocal","")

    prompt = f"""
3분30초 정도 길이의 노래 가사를 만들어줘. 
반드시  
1절 4줄 
줄바꿈 
후렴 4줄 
줄바꿈 
2절 4줄 
줄바꿈  
후렴 4줄  

스타일: {style}
보컬: {vocal}

가사만 출력하고 JSON 형식, 설명, 제목, 따옴표, 코드블록 없이 순수 가사만 작성해라
"""

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model":"gpt-4o-mini",
            "messages":[{"role":"user","content":prompt}],
            "temperature":0.9
        }
    )

    result = r.json()

    lyrics = result["choices"][0]["message"]["content"]

    return jsonify({"lyrics":lyrics})
