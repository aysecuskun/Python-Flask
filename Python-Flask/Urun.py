import requests as r
from bs4 import BeautifulSoup
import json

def urun(id,urun_listesi):
    link=""
    for i in urun_listesi:
        if(int(i["id"])==int(id)):
            link=urun_listesi[int(id)]["link"]
            break
    urun_detay=dict()
    istek = r.get(link)
    soup = BeautifulSoup(istek.content, "html.parser")

    veri0=soup.find_all("div",{"class":"s1hjsdw0-0 jcDUbg"})
    kategori=veri0[0].find_all("a")[1].text
    urun_detay["kategori"]=kategori

    k_listesi = json.load(open("Arama_detaylari.json", "r"))
    k_detay = [i["detay"] for i in k_listesi][0]

    bayrak1 = 0
    if (kategori.strip() != ""):
        for i in k_detay["kategori"]:
            if (i[0] == kategori):
                i[1] = i[1] + 1
                bayrak1 = 1
    json.dump(k_listesi, open("Arama_detaylari.json", "w"))

    veri = soup.find_all("div",{"class":"s1wxq1uo-0 hCNLGd"})[0].find_all("li")
    urun_resimleri=list()
    for i in veri:
        try:
            urun_resimleri.append("http:"+i.img["data-src"])
        except:
            urun_resimleri.append("http:"+i.img["src"])
    urun_detay["resimler"]=urun_resimleri               # resimler

    veri2 = soup.find_all("h1",{"class":"s1wytv2f-2"})[0]
    urun_detay["isim"]=veri2.text                # isim
    urun_bilgileri=list()

    if(soup.find_all("div",{"class":"s1wytv2f-3"})[0].__len__()!=0):
        for i in soup.find_all("div",{"class":"s1wytv2f-3"})[0]:
            urun_bilgileri.append(i.text)
    urun_detay["urun_bilgileri"]=urun_bilgileri         # bilgiler
    magazalar=list()
    veri3=soup.find_all("tr",{"class":["s17f9cy4-3 bkOZxz","s17f9cy4-3 jGZLRi"]})
    for i in veri3[1:]:
        link=link_bul(i.find_all("td")[0].a["href"])
        try:
            magazalar.append({
                #"link":i.find_all("td")[0].a["href"],           # link,
                "link":link,
                "logo":i.find_all("td")[0].a.img["src"],
                "isim":i.find_all("td")[1].a.h2.text,
                "kargo":[i.find_all("td")[2].a.find_all("div")[0].text,i.find_all("td")[2].a.find_all("div")[1].text],
                "fiyat":i.find_all("td")[3].a.find_all("div")[0].text
            })
        except:
            magazalar.append({
                "link":i.find_all("td")[0].a["href"],           # link,
                "logo":i.find_all("td")[0].a.img["src"],
                "isim": i.find_all("td")[1].a.h2.text,
                "fiyat":i.find_all("td")[3].a.find_all("div")[0].text
            })
    urun_detay["magazalar"]=magazalar

    urun_ozellikleri=list()
    try:
        veri4=soup.find_all("div",{"class":"s10v53f3-0"})[0]
        for i in veri4.find_all("li",{"class":"s10v53f3-4"}):
            urun_ozellikleri.append([i.find_all("span")[0].text,i.find_all("span")[1].text])
        urun_detay["urun_ozellikleri"]=urun_ozellikleri     # özellikler
    except:
        urun_detay["urun_ozellikleri"]=urun_ozellikleri     # özellikler

    for i in urun_detay:
        print(i+" : " + str(urun_detay[i]))
    return urun_detay


def link_bul(link):
    istek = r.get(link)
    soup = BeautifulSoup(istek.content, "html.parser")
    urunLink=soup.body.find_all("a")[0]["href"]
    return urunLink

