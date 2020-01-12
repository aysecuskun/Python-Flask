import requests as r
from bs4 import BeautifulSoup
import time,json
import Urun

def k_verileri(veri,kayit=False):   # kullanici verileri gelir
    kullanici_verileri = veri

    if(kayit):
        k_listesi = json.load(open("Arama_detaylari.json", "r"))
        k_detay = [ i["detay"] for i in k_listesi ][0]

        bayrak1=0
        if (kullanici_verileri["arama"].strip()!=""):
            for i in k_detay["arama"]:
                if (i[0]==kullanici_verileri["arama"]):
                    i[1]=i[1]+1
                    bayrak1=1
            if (bayrak1==0): k_detay["arama"].append([kullanici_verileri["arama"],1])

        bayrak1=0
        for i in k_detay["siralama"]:
            if (i[0]==kullanici_verileri["siralama"]):
                i[1]=i[1]+1
                bayrak1=1
        if (bayrak1==0): k_detay["siralama"].append([kullanici_verileri["siralama"],1])

        json.dump(k_listesi,open("Arama_detaylari.json", "w"))
    print(kullanici_verileri)
    t = urunler(kullanici_verileri)
    return t            # urun listesi geri doner

def urunler(kullanici_verileri):
    basla=time.time()
    ara = kullanici_verileri["arama"]
    if (ara==""): ara="calıkusu"
    ara_ek = '-'.join(ara.split(" "))
    siralama = {"akilli_siralama":"","azalan_fiyat":"&sort=price%2Casc"}
    sirala = siralama[kullanici_verileri["siralama"]]


    url= "https://www.cimri.com/"+"arama?q="+ara_ek+sirala
    print(url)

    istek = r.get(url)
    soup = BeautifulSoup(istek.content, "html.parser")
    veri=soup.find_all("div",{"class":"s1cegxbo-1 cACjAF"})[0]
    veri2 = veri.find_all("div",{"id":"cimri-product"})

    urun_listesi=[]
    sayi=0
    for i in veri2:
        m=list()
        try:
            for j in i.find_all("a",{"class":"s14oa9nh-0 gwkxYt"}):
                m.append([Urun.link_bul(j["href"]).j.contents[0].text,j.contents[1]])

            if(i.find_all("img")[0]["data-src"]):
                urun_listesi.append({'id':int(sayi),
                                'resim':"http:"+i.find_all("img")[0]["data-src"],
                                'link':"https://www.cimri.com"+i.find_all("a")[0]["href"],
                                'isim':i.find_all("h3")[0].text,
                                'magazalar':m
                                })
        except:
            urun_listesi.append({'id':int(sayi),
                            'resim': i.find_all("img")[0]["src"],
                            'link': "https://www.cimri.com" + i.find_all("a")[0]["href"],
                            'isim':i.find_all("h3")[0].text,
                            'magazalar':m
                            })
        sayi=sayi+1
    print(time.time()-basla)
    return urun_listesi

