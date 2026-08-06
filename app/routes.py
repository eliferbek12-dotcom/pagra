from flask import Blueprint, request, render_template, jsonify
from flask_cors import CORS
from .services.ai_service import ai_chat

# Blueprint oluştur
main = Blueprint("main", __name__)

# CORS'u blueprint'e uygula (Wix POST için şart)
CORS(main)

@main.route("/")
def home():
    return "Merhaba! PAGRA Akıllı Kitap Asistanına Hoş Geldiniz."

@main.route("/hakkinda")
def hakkinda():
    return "Bu bir PAGRA Python servisidir."

@main.route("/ai", methods=["GET", "POST"])
def ai():
    if request.method == "POST":
        data = request.get_json(force=True)
        message = data.get("message", "")
        return ai_chat(message)

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

# ⭐ Sohbet endpoint'i (Wix buraya POST atıyor)
@main.route("/sohbet", methods=["GET", "POST"])
def sohbet():
    if request.method == "GET":
        return jsonify({
            "durum": "GET isteği alındı, POST gönderin."
        })

    data = request.get_json(force=True)
    soru = data.get("soru", "")

    cevap = ai_chat(soru)

    return jsonify({
        "cevap": cevap
    })