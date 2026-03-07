import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def chat_response(message, history, chat_history):

    messages = []

    # System instruction
    messages.append({
        "role": "system",
        "content": (
            "You are a supportive mental health assistant. "
            "Keep replies SHORT (1–2 sentences). "
            "Be empathetic and conversational."
            "Suggest what to do based on user history and chat. "
        )
    })

    # Journal context
    if history:
        messages.append({
            "role": "system",
            "content": f"User journal context: {history}"
        })

    # Previous chat messages
    for msg in chat_history[-6:]:  # last 6 messages only
        messages.append(msg)

    # Current user message
    messages.append({
        "role": "user",
        "content": message
    })

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": messages,
            "max_tokens": 80   # limits reply size
        }
    )

    data = response.json()

    if "choices" in data:
        return data["choices"][0]["message"]["content"]

    print(data)

    return "I'm here to listen. Tell me more."