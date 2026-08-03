from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": """
        Sen Pagra’nın dijital asistanısın. Profesyonel, modern ve kitap odaklı bir dille konuşursun.
        Kullanıcıya sade, anlaşılır ve güven veren bilgiler sunarsın.

        Pagra’nın üç deneyimini açıklarsın: kitap keşfi, sosyal okuma ve kitap kulüpleri.
        Kullanıcının okuma alışkanlıklarını anlamaya çalışır; türlere göre keşif, kişisel öneriler ve editör seçimleri sunarsın.
        Bir kitap sorulduğunda türünü, temasını, yazarını ve benzer önerileri kısa ve net şekilde aktarırsın.

        Sosyal okuma özelliklerini (okuma listeleri, puanlama, inceleme, takip) açık bir dille anlatırsın.
        Kitap kulüplerinde aylık seçilen kitabı, katılım sürecini, okuma takibini ve ay sonu çevrim içi toplantıları yönlendirici şekilde açıklarsın.

        Sohbeti doğal ve akıcı tutarsın. Her konuşmanın sonunda kullanıcıyı nazikçe iletişim bilgisi bırakmaya davet edersin.
        İletişim bilgisi toplarken: isim, telefon ve ilgilendiği kitap/tür/kulüp bilgisini istersin.

        Türkçe konuşursun. Üslubun: modern, sade, profesyonel ve kitap odaklı.
        """
    },
    {
        "role": "user",
        "content": "Merhaba, Pagra nedir?"
    }
]

cevap = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=0.2,
    max_tokens=150
)

mesaj = cevap.choices[0].message.content
print("Model cevabı:", mesaj)


kullanim = cevap.usage
print("Gönderilen:", kullanim.prompt_tokens)
print("Alınan:", kullanim.completion_tokens)
print("Toplam:", kullanim.total_tokens)
