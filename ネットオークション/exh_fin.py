# -*- coding: utf-8 -*-

import tkinter as tk
import re
import time

def call_exh(products,username,sock):
    def exh():
                
        def send_to(sock,msg):
            try:
                sock.send(msg.encode())
                print("send:"+msg)
                return True
            except:
                sock.close()
            return False
        
        def destroy():
            root1.destroy()
        def add(value1,value2,value3):
            send_to(sock,"出品")
            time.sleep(1)
            #products.append([value1,value2,value3])
            """
            print(username+"さんが")
            print(products[-1])#リストの末尾を表示
            print("を出品")
            """
            msg=str(value1+"/"+str(value2)+"/"+str(value3))
            send_to(sock,msg)
            root1.destroy()
        def newWin():
            re_hiragana=re.compile(r'^[あ-ん]+$')
            value1=entrybox1.get()
            try:
                value2=int(entrybox2.get())
                value3=int(entrybox3.get())
            except ValueError:
                root2 = tk.Toplevel(root1)
                root2.geometry("400x500")
                label4=tk.Label(root2,text="不正な入力です,✕を押してもう一度入力してください")
                label4.place(x=20,y=20)
                root2.mainloop()
            
            
            
            if type(value1)==str and type(value2)==int and type(value3)==int:
                if value2==0 or value3==0:
                    root2 = tk.Toplevel(root1)
                    root2.geometry("400x500")
                    label4=tk.Label(root2,text="0円は不可です")
                    label4.place(x=20,y=20)
                    root2.mainloop()
                elif value2>=value3:
                    root2 = tk.Toplevel(root1)
                    root2.geometry("400x500")
                    label4=tk.Label(root2,text="即決価格を初期価格より大きくしてください")
                    label4.place(x=20,y=20)
                    root2.mainloop()
                elif re_hiragana.fullmatch(value1)==False:
                    root2 = tk.Toplevel(root1)
                    root2.geometry("400x500")
                    label4=tk.Label(root2,text="申し訳ございません、商品名はひらがなで入力をお願いします")
                    label4.place(x=20,y=20)
                    root2.mainloop()
                else:
                    root2 = tk.Toplevel(root1)
                    label=tk.Label(root2,text="["+value1+"]を初期価格："+str(value2)+"円   即決価格："+str(value3)+"円で出品します")
                    label.pack()
                    button1=tk.Button(root2,text="確定",command=lambda:add(value1,value2,value3))
                    button1.pack()
                    button2=tk.Button(root2,text="キャンセル",command=destroy)
                    button2.pack()
                    root2.mainloop()
    
        root1=tk.Tk()
        root1.geometry("400x500")
        root1.title("出品画面")
            
        
        
        label1=tk.Label(root1,text="商品名")
        label1.place(x=20,y=20)
        entrybox1=tk.Entry(master=root1)
        entrybox1.place(x=200,y=20)
        
        
        label2=tk.Label(root1,text="初期価格")
        label2.place(x=20,y=40)
        entrybox2=tk.Entry(master=root1)
        entrybox2.place(x=200,y=40)
        
        label3=tk.Label(root1,text="即決価格")
        label3.place(x=20,y=60)
        entrybox3=tk.Entry(master=root1)
        entrybox3.place(x=200,y=60)
        
        button=tk.Button(root1,text='出品する',command=newWin)
        button.place(x=20,y=100)
        
        
        root1.mainloop()
    return exh
    
    