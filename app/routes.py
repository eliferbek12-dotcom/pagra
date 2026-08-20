from flask import Blueprint, request, render_template, jsonify, Response
from flask_cors import CORS
from .services.ai_service import ai_chat
import csv
import io

main = Blueprint("main", __name__)

CORS(main)

# Müşteri adayları listesi
LEADS_DATA = []

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

@main.route("/sohbet", methods=["GET", "POST"])
def sohbet():
    if request.method == "GET":
        return jsonify({"durum": "GET isteği alındı, POST gönderin."})

    data = request.get_json(force=True)
    soru = data.get("soru", "")
    cevap = ai_chat(soru)

    return jsonify({"cevap": cevap})

@main.route("/demo-talep", methods=["POST"])
def demo_talep():
    data = request.get_json(force=True)
    
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

@main.route("/yonetim/veriler", methods=["GET"])
def yonetim_veriler():
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

@main.route("/yonetim/csv-indir", methods=["GET"])
def csv_indir():
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