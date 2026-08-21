from flask import Blueprint, request, render_template, jsonify, Response
from flask_cors import CORS
from .services.ai_service import ai_chat
import csv
import io

main = Blueprint("main", __name__)

# CORS iznini Blueprint seviyesinde aktif ediyoruz
CORS(main, resources={r"/*": {"origins": "*"}})

# Müşteri taleplerini saklayan liste
LEADS_DATA = [
    {
        "id": 1,
        "adSoyad": "Örnek Müşteri",
        "telefon": "05550000000",
        "not": "Test kaydıdır"
    }
]

@main.route("/")
def home():
    return "Merhaba! PAGRA Akıllı Kitap Asistanına Hoş Geldiniz."

@main.route("/durum")
def durum():
    return {
        "durum": "aktif",
        "versiyon": "1.0",
        "mesaj": "API çalışıyor"
    }

# Hem /chat hem /sohbet yolunu ve OPTIONS isteklerini destekleyen rota
@main.route("/chat", methods=["POST", "OPTIONS"])
@main.route("/sohbet", methods=["GET", "POST", "OPTIONS"])
def sohbet():
    # Tarayıcının CORS kontrolü için gönderdiği OPTIONS isteği
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if request.method == "GET":
        return jsonify({"durum": "GET isteği alındı, POST gönderin."})

    try:
        data = request.get_json(force=True, silent=True) or {}
        # Wix'ten "mesaj" veya "soru" gelse de yakalar
        soru = data.get("mesaj") or data.get("soru") or ""

        if not soru:
            return jsonify({"cevap": "Lütfen bir mesaj girin."}), 400

        cevap = ai_chat(soru)
        return jsonify({"cevap": cevap, "message": cevap})
    except Exception as e:
        print(f"Chat Hatasi: {e}")
        return jsonify({"cevap": "Bir hata oluştu, lütfen tekrar deneyin."}), 500

@main.route("/demo-talep", methods=["POST", "OPTIONS"])
def demo_talep():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json(force=True, silent=True) or {}
    
    ad_soyad = data.get("adSoyad", "")
    telefon = data.get("telefon", "")
    not_metni = data.get("not", "")

    yeni_kayit = {
        "id": len(LEADS_DATA) + 1,
        "adSoyad": ad_soyad,
        "telefon": telefon,
        "not": not_metni
    }
    LEADS_DATA.append(yeni_kayit)

    print(f"Yeni Demo Talebi -> Ad Soyad: {ad_soyad}, Tel: {telefon}, Not: {not_metni}")

    return jsonify({
        "durum": "basarili",
        "mesaj": "Demo talebiniz başarıyla alındı."
    })

@main.route("/yonetim/veriler", methods=["GET", "OPTIONS"])
def yonetim_veriler():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    arama = request.args.get("arama", "").lower()
    
    if arama:
        filtrelenen = [
            l for l in LEADS_DATA 
            if arama in l.get("adSoyad", "").lower() or arama in l.get("telefon", "").lower()
        ]
    else:
        filtrelenen = LEADS_DATA

    toplam = len(LEADS_DATA)
    return jsonify({
        "istatistikler": {
            "toplamLead": toplam,
            "aylikKayit": toplam,
            "gunlukKayit": len(filtrelenen),
            "donusumOrani": "%60"
        },
        "leads": filtrelenen
    })

@main.route("/yonetim/csv-indir", methods=["GET", "OPTIONS"])
def csv_indir():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    cikti = io.StringIO()
    yazici = csv.writer(cikti)
    yazici.writerow(["ID", "Ad Soyad", "Telefon", "Not"])

    for lead in LEADS_DATA:
        yazici.writerow([lead.get("id"), lead.get("adSoyad"), lead.get("telefon"), lead.get("not")])

    return Response(
        cikti.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=leads_rapor.csv"}
    )