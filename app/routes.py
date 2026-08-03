from flask import Blueprint, request, render_template, jsonify
from .services.ai_service import ai_chat

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "Merhaba! PAGRA Akıllı Kitap Asistanına Hoş Geldiniz."

@main.route("/hakkinda")
def hakkinda():
    return "Bu bir PAGRA Python servisidir."

@main.route("/ai", methods=["GET", "POST"])
def ai():
    if request.method == "POST":
        # JSON'u zorla parse et → string gelmesini engeller
        data = request.get_json(force=True)

        # JSON içindeki message alanını al
        message = data.get("message", "")

        # Groq API çağrısı
        return ai_chat(message)

    # GET isteği gelirse bilgilendirme döner
    return "Bu endpoint POST ile çalışır. Lütfen JSON gönderin."

@main.route("/html")
def html_sayfa():
    kullanici = "Elif"
    return render_template("index.html", isim=kullanici)

@main.route("/durum")
def durum():
    veri = {
        "durum": "aktif",
        "versiyon": "1.0",
        "mesaj": "API çalışıyor"
    }
    return veri

@main.route("/kullanici/<int:id>")
def kullanici(id):
    return {
        "id": id,
        "ad": "Elif",
        "rol": "admin"
    }


@main.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json(force=True)
    soru = data.get("soru", "")

    # Şimdilik test cevabı
    cevap = f"Backend mesajı aldım: {soru}"

    return jsonify({"cevap": cevap})

    




