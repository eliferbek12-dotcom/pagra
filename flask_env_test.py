from dotenv import load_dotenv
import os

load_dotenv()  

api_key = os.getenv("GROQ_API_KEY")
print("API Anahtarı:", api_key)

from flask import Flask

app= Flask(__name__)

@app.route('/')

def ana_sayfa():
    return "Merhaba, Flask uygulamasına hoş geldiniz!"

if __name__ == '__main__':
    app.run(debug=True)

    