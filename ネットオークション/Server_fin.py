import socket
import select
import time

def send_to(sock,msg):
    try:
        sock.send(msg.encode())
        return True
    except:
        sock.close()
        return False

def broadcast(socklist,msg):
    for sock in socklist:
        if not send_to(sock,msg):
            socklist.remove(sock)

def return_sender_port(client_sock_table,sock):
    #client_sock_tableから、送信者のボードを調べる
    #辞書型のキーと値をfor文で順に参照する
    for key, val in client_sock_table.items():
        if val == sock:
            return key
    return None

def send_product(sock_list,product):#更新または初期の接続の際に商品情報を送るメソッド 引数sock,product 戻り値なし
    product_data = {"PRODUCTS":product}
    send_data = str(product_data)
    send_to(sock_list[-1],send_data)

"-----------------------------------------------------------------------------------"    
#サーバの名前（あるいはIPアドレス）
#host='127.0.0.1' #localhost
host="10.65.171.161"
#接続先ホストのポート番号
port=15001
#接続キューの最大数
backlog=10
#ソケットから受信するデータのバッファサイズ
bufsize=4096

product = [["りんご","1","100"],["みぎた","10","10000"],["もとき","30","400"],
          ["みぎたのグローブ","500","10000"],["せんべい","100","150"],["ぶどう","50","500"],
          ["おにぎり","10","100"]]


bid_deta = []
i = 0
j = -1
#ソケットを作成する
server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("sock is created")

try:
    #作成したソケットにアドレスとポート番号を設定
    server_sock.bind((host,port))
    #クライアントからの接続待ちを開始
    print("socket bind")
    server_sock.listen(backlog)
    print("socket listen")
    sock_list = [server_sock]
    #クライアントのソケットをボートで管理するために、辞書型でソケットを保存する
    client_sock_table = {}
    while True:
        print("まってまーす")
            
            #読み込み準備完了ソケットリスト
            #書き込み準備完了ソケットリスト
            #例外ソケットリスト
            #を取得
            #
            #第１引数には読み込み待ちのソケットリストを指定
            #第2、第3引数は今回使わないので空リストで良い
        r_ready_sockets,w_ready_sockets,e_ready_sockets = select.select(sock_list,[],[])
        #recv:ソケットからデータを受信
        for sock in r_ready_sockets:
            if sock == server_sock:
                print("最初の接続")
                conn,address = sock.accept()
                #新しいソケットをソケットリストに追加する
                sock_list.append(conn)
                #サーバソケットには送らなくて良いので、リストから一旦外す
                #ボートをキーとしてソケットを保存する
                client_sock_table[address[1]] = conn
                #誰かからの接続があったことを全員に通知する
                sock_list.remove(server_sock)
                send_product(sock_list,product)
                #サーバソケットをリストに戻す
                sock_list.append(server_sock)
                print(str(address) + "is connected")
            else:
                try:                   
                    #ここで読み取るのは入札か出品か
                    b_msg=sock.recv(bufsize)
                    #バイトコードが送られてくるのででコードする
                    t=b_msg.decode('utf-8')
                    print(t)
                    if len(t) == 0:
                        print("接続きれたよ")
                        sock.close()
                        sock_list.remove(sock)
                    else:
                        sender_port = return_sender_port(client_sock_table,sock)
                        if sender_port is not None:    
                            if t == "入札":
                                b_msg=sock.recv(bufsize)
                                #バイトコードが送られてくるのででコードする
                                msg=b_msg.decode('utf-8')
                                list_goods =str(msg).rsplit("/")
                                c = len(bid_deta)
                                bid_deta.append([])
                                bid_deta[c].append(str(sender_port))
                                bid_deta[c].append(list_goods[1])
                                bid_deta[c].append(list_goods[2])
                                #print(bid_deta)
                                for k in range(len(product)):
                                    if product[k][0] == bid_deta[c][1]:
                                        product[k][1] = bid_deta[c][2]
                                        newk = k
                                        
                                        #即決の
                                if int(product[newk][1]) >= int(product[newk][2]):
                                    del product[newk]
                                print("---------受信情報------------")
                                print(bid_deta)

                                
                            elif t =="出品":
                                b_msg=sock.recv(bufsize)
                                msg=b_msg.decode('utf-8')
                                list_goods =str(msg).rsplit("/") 
                                print("---------------[商品名,現在価格,即決価格]-----------")
                                print(list_goods)
                                c = len(product)
                                            
                                product.append([])
                                product[c].append(list_goods[0])
                                product[c].append(list_goods[1])
                                product[c].append(list_goods[2])

                                
                            print("after product")
                            print(product)                                
                            sock_list.remove(server_sock)
                            product_data = {"PRODUCTS":product}
                            send_data = str(product_data)
                            broadcast(sock_list,send_data)
                            sock_list.append(server_sock)
                            
                            
                except:
                    sock.close()
                    sock_list.remove(sock)
                    sock_list.remove(server_sock)
                    broadcast(sock_list,"someone disconnected")
                    sock_list.append(server_sock)
                    #ソケットにデータを送信
except Exception as e:
    print("Exception")
    print(e)
    server_sock.close()
    