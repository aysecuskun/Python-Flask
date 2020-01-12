from flask import Flask,jsonify,request,Response,render_template
from flask_socketio import SocketIO
from socket import *
import os,json
import Urun,Urunler,Urundetay

app = Flask(__name__)
socketio = SocketIO( app )
app.secret_key = os.urandom(24)

host = gethostbyname(gethostname())
port=1234

urun_listesi=list()
@app.route('/')             # Anasayfa
def f_home():
    return  render_template("/aramasayfasi.html")

@socketio.on('k_verileri')      # kullanıcı arama verilerini alır (sayfadan ara butonuna basıldığında çalışır)
def s_k_verileri(veri,kayit=True):
    if (kayit==True):
        arama = ""
        for i in veri["arama"]: arama = arama + chr(i)
        veri["arama"]=arama
    global urun_listesi
    for i in veri:
        veri[i] = veri[i].strip()
    urun_listesi = Urunler.k_verileri(veri,False) # urun listesi gelir
    socketio.emit('geri', urun_listesi)         # urun listesi "geri" ye gonderilir
    return "1"

@socketio.on('veriler')         # urun verileri alma
def s_veriler(veri):
    global urun_listesi
    print(veri)
    id = veri["urun_path"][veri["urun_path"].rfind("/")+1:]
    urun_detay=Urun.urun(id,urun_listesi)   # urun detayları geri döner
    socketio.emit('urunsayfasi', urun_detay)    # urun detayları "urunsayfasi" na gönderilir
    return "1"

@app.route('/urun/<id>')        # urun sayfası yuklenince çalışır
def f_urunSayfasi(id):
    return render_template("/ürün.html")

if __name__ == '__main__':
    app.run(debug=True,host=host,port=port)
