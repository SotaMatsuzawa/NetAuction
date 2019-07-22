import tkinter as tk
import sys
import time

def call_bid(products,info,username,sock):
    def bid():
        
        "------------入力値（全ての商品・選択した商品・ユーザー名）------------"        
        deta = info
        thing = info[0]
        user=username
        print(deta)
        
        "----------------------戻り値の定義(全ての商品・入札情報)-----------------"
        bid_deta = []
        #入札せれた履歴を残す


        global etr
        def newButton(deta,i,j):
            probutton=tk.Label(root,text=deta,bg="green")
            probutton.place(relx=0.20*(j+1),rely=0.10+i*0.1,relwidth=0.20,relheight=0.1)
        
        def send_to(sock,msg):
            try:
                sock.send(msg.encode())
                print("send:"+msg)
                return True
            except:
                sock.close()
            return False
                    
        def sumarry(a):
        #即決するかを決める関数
        #現在価格が即決価格以上ならTrue、そうでなければFalseを返す
            if int(a[1]) >= a[2]:
                return True
            else:
                return False
        def destroy():
                root.destroy()
        def newWin(deta,bid_deta,count,user,thing,n):
            n=etr.get()
            root2 = tk.Toplevel(root)
            root2.geometry("300x200")
            try:
                n_int=int(n)
                if n_int!=0 and n_int>=deta[1]:
                    if int(n)<deta[2]:
                        label1=tk.Label(root2,text=thing+"を"+n+"円で入札")
                        label1.pack()
                    else:
                        products.remove(info)
                        label2=tk.Label(root2,text=thing+"を"+n+"円で購入")
                        label2.pack()
                    button1=tk.Button(root2,text="確定",command = lambda:res_mer(deta,bid_deta,0,user,thing,n))
                    button1.pack()
                    button2=tk.Button(root2,text="キャンセル",command=lambda:root2.destroy())
                    button2.pack()
                elif n_int==0:
                    label3=tk.Label(root2,text="0円での入札は不可")
                    label3.pack()
                elif n_int<deta[1]:
                    label4=tk.Label(root2,text="現在価格未満の値段での入札は不可")
                    label4.pack()
                else:
                    label5=tk.Label(root2,text="なーにやってんの")
                    label5.pack()
            except ValueError:
                label6=tk.Label(root2,text="不正な入力です,✕を押してもう一度入力してください")
                label6.pack()
                

                
            root2.mainloop()
                
                       
        def res_mer(deta,bid_deta,count,user,thing,n):
            n=etr.get()
            root2 = tk.Toplevel(root)
    
            if len(n)<=0:
                return
            
            n=int(n)
                               
            wanted_good = deta
            wanted_good[1] = n
            #現在価格の更新
            deta[1] = str(wanted_good[1])
            #商品のデータの上書き
            bid_deta.append([])
            bid_deta[0].append(user)
            bid_deta[0].append(thing)
            bid_deta[0].append(n)
            flag2 = sumarry(wanted_good)
            
            if flag2:
                print(user + "さんが" +str(deta[0]) + "を" + str(deta[1]) + "円で購入しました")
            else:
                print(user+"さんが"+info[0]+"を"+str(info[1])+"円で入札しました")
            send_to(sock,"入札")
            time.sleep(1)
            msg=str(user+"/"+str(deta[0])+"/"+str(deta[1]))
            send_to(sock,msg)
            destroy()
            root2.mainloop()
     
        if deta == []:
            #在庫がなくなった場合はプログラムを終了させる
            print("在庫がないため終了します")
            sys.exit()
 
        root = tk.Tk()
        root.title("商品名："+deta[0])
        root.geometry("800x600")
        
        pr1=tk.Label(root,text="現在価格:" + str(deta[1]) + "円",bg="green")
        pr1.place(relx=0.10,rely=0.10,relwidth=0.85,relheight=0.2)
        pr2=tk.Label(root,text="即決価格:" + str(deta[2]) + "円",bg="green")
        pr2.place(relx=0.10,rely=0.30,relwidth=0.85,relheight=0.2)
        pr3=tk.Label(root,text="入札価格を入力してください")
        pr3.place(relx=0.05,rely=0.65,relwidth=0.65,relheight=0.1)
        entered_txt = tk.StringVar()       
        etr = tk.Entry(root,width=50,textvariable = entered_txt)
        n=etr.get()
        #etr.bind("<Return>",lambda:newWin(deta,bid_deta,0,user,thing,n))
        etr.place(relx=0.05,rely=0.75,relwidth=0.65,relheight=0.1)
        bt = tk.Button(root,text='入札', width=50,command=lambda:newWin(deta,bid_deta,0,user,thing,n),bg="orange")
        bt.place(relx=0.75,rely=0.75,relwidth=0.20,relheight=0.1)
            
        """
        for i in range(len(bid_deta)):
            #最後に入札した人たちのデータを出力
                print(bid_deta[i])     
         """   

    return bid

