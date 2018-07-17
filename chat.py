from tkinter import *
from tkinter import ttk
import threading
import socket
from datetime import datetime
import os
import binascii

num1=0
num2=0

tk=Tk()
tk.title('对话框')
tk.resizable(0,0)
tk.geometry('600x380')
#本地地址
frame=Frame(highlightbackground='#ccc',highlightthickness=1)
title=Label(text='本地地址')
title.place(x=90,y=4)
frame.place(x=5,y=10,width=220,height=170)

type=Label(tk,text='协议类型:')
type.place(x=10,y=30)
val=StringVar(value='UDP')
input1=ttk.Combobox(values=('UDP','TCP'),textvariable=val)
input1.place(width=124,height=20,x=80,y=30)

host=Label(tk,text='本地IP地址:')
host.place(x=10,y=60)
hostname=socket.gethostname()
hostVal=StringVar(value=socket.gethostbyname(hostname))
input2=Entry(textvariable=hostVal,state=DISABLED)
input2.place(x=80,y=60)

port=Label(tk,text='本地端口号:')
port.place(x=10,y=90)
portVal=IntVar(value='3333')
input3=Entry(textvariable=portVal)
input3.place(x=80,y=90)

def save():
    global num2
    while True:
        try:
            data = sk.recvfrom(1024)
            content, address = data
            vals = content.decode(encoding='gbk')
            if longNum.get() == 1:  #十六进制转换
                vals=binascii.b2a_hex(content) #十六进制显示
            listbox.insert(0, vals)
            if timeVal.get() == 1: #添加接收时间
                strs="【" + str(datetime.now()) + "】"
                listbox.insert(0,strs)
            num2 += 1
            vala.set(num2)
        except:
            pass
obj=threading.Thread(target=save)
def connect():
    global sk  #global可以让局部变量变为全局变量
    if link['text'] == '连接':
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.bind(("", int(input3.get())))
        link['text']="断开"
        input1['state']=DISABLED
        input3['state'] = DISABLED
        if not obj.is_alive(): #判断obj是否在运行
            obj.start()
    else:
        sk.shutdown(2)
        sk.close()
        #os.system('taskkill /pid %s -f'%(str(os.getpid())))  杀死端口号
        link['text'] = "连接"
        input1['state'] = NORMAL
        input3['state'] = NORMAL
link=Button(text='连接',command=connect)
link.place(x=20,y=135,width=80,height=30)

def delete():
    global num2
    current=listbox.curselection()
    try:
        listbox.delete(current)
        num2 -= 1
        vala.set(num2)
    except:
        pass
dels=Button(text='删除',command=delete)
dels.place(x=130,y=120,width=60,height=25)

def clears():
    vala.set(0)
    listbox.delete(0,END)
clear=Button(text='清空',command=clears)
clear.place(x=130,y=150,width=60,height=25)

frame1=Frame(bd=1,highlightbackground='#ccc',highlightthickness=1)
frame1.place(x=5,y=200,width=220,height=170)
title1=Label(text='发送地址')
title1.place(x=90,y=195)

type1=Label(tk,text='协议类型:')
type1.place(x=10,y=220)
val1=StringVar(value='UDP')
input11=ttk.Combobox(values=('UDP','TCP'),textvariable=val1)
input11.place(width=124,height=20,x=80,y=220)

host1=Label(tk,text='目标IP地址:')
host1.place(x=10,y=250)
host1Val=StringVar(value=socket.gethostbyname(hostname))
input22=Entry(textvariable=host1Val)
input22.place(x=80,y=250)

port1=Label(tk,text='目标端口号:')
port1.place(x=10,y=280)
port1Val=IntVar(value=8080)
input33=Entry(textvariable=port1Val)
input33.place(x=80,y=280)

timeVal=IntVar(value=0)
times=Checkbutton(tk,text='显示接收时间',variable=timeVal,onvalue=1,offvalue=0)
times.place(x=10,y=310)

longNum=IntVar(value=0)
showLong=Checkbutton(tk,text='十六进制显示',variable=longNum,onvalue=1,offvalue=0)
showLong.place(x=10,y=340)

get=Label(text='接收：').place(x=130,y=310)
vala=StringVar(value=0)
getNum=Label(textvariable=vala).place(x=170,y=310)

put=Label(text='发送：').place(x=130,y=340)
valb=StringVar(value=0)
putNum=Label(textvariable=valb).place(x=170,y=340)

listbox=Listbox(tk,highlightthickness=0)
listbox.place(x=230,y=5,width=360,height=310)

inputVal=StringVar(value='')
input=Entry(tk,textvariable=inputVal)
input.place(x=230,y=330,width=300,height=40)

sk1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def inputs():
    global num1
    while True:
        if not state.isSet():
            state.wait()  #当event锁为0时，等待，下边代码不执行，当event锁为1时，等待不住，执行下边代码
        sk1.sendto(inputVal.get().encode('gbk'), (host1Val.get(), int(port1Val.get())))
        num1 += 1
        valb.set(num1)
        state.clear()
obj2=threading.Thread(target=inputs)
state=threading.Event()  #线程条件锁，默认为0
def run():
    state.set()  #将event锁设为1
    if not obj2.is_alive():
        obj2.start()
submit=Button(text='发送',command=run)
submit.place(x=540,y=330,width=50,height=40)

if __name__ == '__main__':
    tk.mainloop()


