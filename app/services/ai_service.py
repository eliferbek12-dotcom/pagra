from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_chat(message: str):
    try:
        cevap = client.chat.completions.create(
            model="groq/compound",
            messages=[{"role": "user", "content": message}]
        )
        return cevap.choices[0].message.content

    except Exception as e:
        return f"Hata: {e}"