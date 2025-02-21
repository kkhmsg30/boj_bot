from openai import OpenAI
from os import getenv

client = OpenAI(api_key=getenv("GPT_KEY"))

def generate_encouragement():
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "문제풀이성공을 축하해줘"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "격려메세지"
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "정말 못푸시네유!"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "20자 정도 격려메세지"
                }
            ]
            }
        ],
        response_format = {
            "type": "text"
        },
        temperature = 1.3
    )
    return response.choices[0].message.content