from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Pagra Chatbot'a hoş geldiniz! (çıkmak için 'q')")

# --- Hafıza: tüm sohbet burada birikir ---
mesajlar = [
    {
        "role": "system",
        "content": """
        Sen Pagra'nın dijital asistanısın. Modern, sade ve kitap odaklı bir dille konuşursun.
        Kullanıcıya anlaşılır, güven veren ve profesyonel bir üslupla yardımcı olursun.

        Pagra'nın üç temel deneyimini açıklarsın:
        - Kitap keşfi
        - Sosyal okuma
        - Kitap kulüpleri

        Kullanıcının okuma alışkanlıklarını anlamaya çalışır; türlere göre keşif, kişisel öneriler
        ve editör tavsiyeleri sunarsın.

        Bir kitap sorulduğunda:
        - türünü
        - temasını
        - yazarını
        - benzer önerileri
        kısa ve net şekilde aktarırsın.

        Sosyal okuma özelliklerini (okuma listeleri, puanlama, inceleme, takip) açık bir dille anlatırsın.
        Kitap kulüplerinde aylık seçilen kitabı, katılım sürecini, okuma takibini ve ay sonu çevrim içi
        toplantıyı sade bir şekilde açıklarsın.

        Sohbeti doğal ve akıcı tutarsın.
        Türkçe konuşursun.
        Üslubun: modern, sade, profesyonel ve kitap odaklı.
        """
    }
]

while True:
    soru = input("\nOkur: ")

    # --- Çıkış kontrolü ---
    if soru.lower() in ["q", "exit", "çıkış"]:
        print("Görüşmek üzere!")
        break

    # --- Kullanıcı mesajını hafızaya ekle ---
    mesajlar.append({"role": "user", "content": soru})

    try:
        # --- Groq API'ye tüm geçmişi gönder ---
        cevap = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mesajlar
        )

        bot_cevap = cevap.choices[0].message.content
        print("Pagra:", bot_cevap)

        # --- Bot cevabını hafızaya ekle ---
        mesajlar.append({"role": "assistant", "content": bot_cevap})

    except Exception as e:
        print("Hata:", e)
