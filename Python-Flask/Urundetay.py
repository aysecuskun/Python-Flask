import json
def detayAl(kullanici):
    veri = json.load(open("Arama_detaylari.json","r"))
    detay=""
    for kullanicilar in veri:
        if( kullanicilar["isim"] == kullanici ):
            detay=kullanicilar
            break
    return detay

def genelKullanici(detay):
    detaylar = json.load(open("Arama_detaylari.json","r"))
    def hesapla(liste, detay2):
        temp_list = list()
        for i in liste: temp_list += i["detay"][detay2]
        for i in temp_list:
            for j in temp_list[temp_list.index(i) + 1:]:
                if (i[0] == j[0]):
                    i[1] = i[1] + j[1]
                    temp_list.pop(temp_list.index(j))
        return temp_list
    return hesapla(detaylar,detay)

def genelGrafik():
    detay={"arama":genelKullanici("arama"),
    "siralama":genelKullanici("siralama"),"kategori":genelKullanici("kategori")}
    return detay


def k_veri(isim):
    print(type(isim),isim)
    def k_pop(aranan):
        detay = [i["detay"] for i in json.load(open("k_detaylari.json", "r")) if (i["isim"]==isim)][0]
        max=0
        max_arama=""
        for i in detay[aranan]:
            if (max<i[1]):
                max=i[1]
                max_arama=i[0]
        return max_arama
    if(k_pop("arama")!=""):
        veri={'arama': k_pop("arama"), 'siralama': k_pop("siralama")}
    else:
        veri={'arama': "",  'siralama': "azalan_siralama"}
    return veri