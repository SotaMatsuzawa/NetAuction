# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 18:07:41 2019

@author: souta
"""
"----------------------------------機能の説明---------------------------------------------"
"""
１．通信開始したらポート番号によてユーザ名を管理する
２．初期画面（検索ボタン、ソートボタン、出品ボタン）の配置
３．サーバからproductsを受け取り、そのproducts数だけ商品ボタンを配置する


それ以降は入札、出品がされたらproductsが更新されるのでそのたびに３を実行

"""


"---------------------------------モジュールのインポート----------------------------------"
import tkinter as tk
import exh_fin as exh
import bid_fin as bid
import ast
import socket, select
import threading


"----------------------------------初期値設定----------------------------------------"
buttons=[]
stocked_msg = []
username="testuser"
#host='127.0.0.1' #localhost
host="10.65.171.161"
#接続先ホストのポート番号
port=15001
#ソケットから受信するデータのバッファサイズ
bufsize=4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"--------------------------------関数の定義------------------------------------------"
def return_productButton(products):#商品の数だけボタンを作成する
    i=0
    for name in products: 
        buttons.append(tk.Button(frame,text=name[0]+" : 現在価格 "+str(name[1])+"円　　即決価格"+str(name[2])+"円",command=bid.call_bid(products,name,username,sock)))
        buttons[i].place(relx=0,rely=0.3+i*0.25,relwidth=1.0,relheight=0.25)#ボタンの配置場所をi*0.25によって縦方向にずらしている
        buttons[i].pack(fill="x")
        i+=1
    return buttons


def search(Product):#検索このメソッドは笹本君に作ってもらった
    global buttons
    buttons=destroy_button()#配置されたボタンを一度削除する
    character=Search_w.get()
    if len(character)<=0:#入力された文字数が０の場合はすべての商品を表示
        return_productButton(Product)
        return Product
    searchlist=[]#検索結果に当てはまる商品を追加するリスト
    count=0
    namelist=[x[0] for x in Product]
    for i in namelist:       
        count=count+1
        if character in i:
            searchlist.append(Product[count-1])    
    Product=[]
    Product=searchlist.copy()
    return_productButton(Product)
    return Product


def sort(Product):#ソート　このメソッドは笹本君に作ってもらった
    global buttons
    buttons=destroy_button()
    way=listbox.curselection()[0]
    if way==0:
        sorted1=sorted(Product,key=lambda x:x[0])
    elif way==1:
        sorted1=sorted(Product,key=lambda x:x[1])
    else:
        sorted1=sorted(Product,key=lambda x:x[2])        
    Product=[]
    Product=sorted1.copy()
    return_productButton(Product)
    return Product


def update(Product):
    global buttons
    buttons=destroy_button()
    return_productButton(Product)
    return Product


def destroy_button():#配置されたボタンを削除するメソッド
    global buttons
    for button in buttons:        
        button.destroy()
    buttons=[]
    return buttons

def send_to(sock,msg):
    try:
        sock.send(msg.encode())
        return True
    except:
        sock.close()
        return False


product = []
stocked_pro=[]
def listen():
    global buttons
    global product
    try:
        sock.connect((host,port))
        while True:
            r_ready_sockets, w_ready_sockets, e_ready_sockets = select.select([sock],[],[])
            try:
                recev_msg = sock.recv(bufsize)
                pro=recev_msg.decode('utf-8')                
                products_data = ast.literal_eval(pro)
                products=products_data["PRODUCTS"]
                product=[]#productの初期化
                for l in products:
                    product.append([l[0],int(l[1]),int(l[2])])
                print("---------------------------------------------------")
                print(product)
                update(product)

            except:
                break

    except Exception as e:
        print(e)
    finally:
        stocked_msg.append(product)
        sock.close()
        print("厄介")

"----------------------------------初期情報の取得-----------------------------------------------------------"

products=product.copy()#ソートや検索の際にproductをいじりたくないため、クライアント側で扱うのはproductsとした
buttons=return_productButton(products)

"----------------------------初期画面の設定-------------------------------------------------"
root = tk.Tk()
root.title("初期画面")
root.geometry("500x400")

"""
フレームに配置されるボタンの個数が増えるとボタンが見えなくなってしまうのでスクロールバーを付ける必要がある
フレームにボタンを配置し、スクロールバーを配置するとうまくスクロールバーが機能してくれないので、
キャンバスにフレームとスクロールバーを配置し、そのフレームのサイズによってスクロールするようにした
"""
canvas = tk.Canvas(root,bg="red")
canvas.pack(side=tk.LEFT, fill=tk.BOTH)


bar = tk.Scrollbar(root, orient=tk.VERTICAL)
bar.pack(side=tk.RIGHT, fill=tk.Y)
bar.config(command=canvas.yview)


canvas.config(yscrollcommand=bar.set)
canvas.config(scrollregion=(0,0,400,600)) #スクロール範囲


frame = tk.Frame(canvas,bg="light gray")
frame.pack(expand=True)
canvas.create_window((0,0), window=frame, anchor=tk.NW, width=480)
canvas.pack(fill="both",expand=True)

"""
TitleLabel=tk.Label(master=frame,text="ミギーズオークション",font=("メイリオ","12"),bg="green")
TitleLabel.place(relx=0,rely=0,relwidth=1.0,relheight=0.1)
"""
"検索をするために文字入力することができるEntryを作成し、検索ボタンにコマンドとしてsearchさせる"
entered_txt=tk.StringVar()
Search_w=tk.Entry(master=frame,width=30,textvariable=entered_txt)
Search_w.pack(anchor="nw")
character=Search_w.get()
SearchButton=tk.Button(frame,text="検索",command=lambda:search(product))
SearchButton.pack(anchor="nw")
"出品ボタンの配置,コマンドは出品"
ExhButton=tk.Button(frame,text="出品",command=exh.call_exh(products,username,sock))
ExhButton.pack(anchor="nw")

"ソートの仕方の選択ができるリストボックスの作成"
listbox = tk.Listbox(frame, height=3)
for line in ["商品名順", "現在価格順","即決価格順"]:
    listbox.insert(tk.END, line)
listbox.select_set(0)
listbox.pack(anchor="nw")

"ソートができるボタンの配置"
sortButton=tk.Button(frame,text="並べ替え",command=lambda:sort(product))
sortButton.pack(anchor="nw")


#renewButton=tk.Button(frame,text="更新",command=lambda:update(product))
#renewButton.pack(anchor="nw")

"----------------------------これ以下が実行内容--------------------------------------------------"


#サーバから送信されたメッセージを持つ処理を別のスレッドで制御する
#threading.Threadのインスタンスを生成する
#targetで指定したlistenをスレッドで処理する
thrd = threading.Thread(target=listen)
thrd.start()

root.mainloop()
