ogrenciler = {}
def ogrenci_ekle():

 numara = input("Öğrenci Numarası: ")
 isim = input("Öğrenci İsmi: ")
 notu = input("Öğrenci Notu: ")

 ogrenciler[numara] = {
        "isim": isim,
        "not": notu
    }

 print("Öğrenci başarıyla eklendi.")
 

