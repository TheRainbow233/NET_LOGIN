#该程序适配pyinstaller，命令行运行会无法正常使用文件保存以及开机启动。需自行更改
import base64
from io import UnsupportedOperation
import uuid
import requests
import os, sys
import socket
import win32api
import win32con
import tkinter
import json
from Crypto.Cipher import ARC4
from tkinter import ttk
import tkinter.messagebox as msgbox

#Base64图标
icon = "AAABAAIAEBAAAAEAIABoBAAAJgAAACAgAAABACAAKBEAAI4EAAAoAAAAEAAAACAAAAABACAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFgAAAEkAAABOAAAATgAAAE4AAABKAAAAPgAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlQAAAPkAAAD9AAAA/QAAAP0AAAD9AAAA/QAAAPwAAAD4AAAAlQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAADgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC8AAAD4AAAA/wAAAP8AAAD/AAAA/wAAAPgAAAAvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACKAAAA0QAAAMwAAACCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABnAAAA/wAAAP8AAAD/AAAA/wAAABgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAD/AAAA/wAAAP8AAABgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJIAAAD/AAAA/wAAAP8AAAD/AAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAvAAAAPsAAAD5AAAAogAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2AAAAFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAAAAIAAAAEAAAAABACAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAFQAAABgAAAAYAAAAGAAAABgAAAAYAAAAGAAAABgAAAAYAAAAGAAAABgAAAAYAAAAGAAAABgAAAAYAAAAEgAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALAAAADzAAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAADrAAAArgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPwAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAA/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAAuQAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAuQAAAAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2AAAAP4AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAANgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPAAAAYgAAANwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAANwAAABiAAAADwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANAAAAGwAAABsAAAAbAAAAGwAAAA0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFAAAAZQAAAOgAAAD/AAAA/gAAAKsAAAA1AAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAANoAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPUAAACZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACnAAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAABOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP4AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAKYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIQAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAM8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAawAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAOEAAAAOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeAAAAwgAAAP8AAAD/AAAA/wAAAOsAAACMAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAGAAAABgAAAAYAAAAEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="

config = {
    "account": "null",
    "password": "null",
    "type": "null",
    "autoStart": 0
}

if __name__ == "__main__":

    def rc4_encrypt(data):# RC4加密
        key = bytes(str(uuid.uuid3(uuid.NAMESPACE_URL, "TH3RA1NB0W")).replace("-", ""), encoding='utf-8')
        enc = ARC4.new(key)
        res = enc.encrypt(data.encode('utf-8'))
        res=base64.b64encode(res)
        res = str(res,'utf-8')
        return res

    def rc4_decrypt(data):# RC4解密
        data = base64.b64decode(data)
        key = bytes(str(uuid.uuid3(uuid.NAMESPACE_URL, "TH3RA1NB0W")).replace("-", ""), encoding='utf-8')
        enc = ARC4.new(key)
        res = enc.decrypt(data)
        res = str(res,'utf-8', 'ignore')
        return res

    #登录Get请求
    def loginNET(account: str, password: str, type: str) -> str:
        my_ip = socket.gethostbyname(socket.gethostname())
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "192.168.40.2:801",
            "Referer": "http://192.168.40.2/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52"
        }
        url = f"http://192.168.40.2:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=,0,{account}@{type}&user_password={password}&wlan_user_ip={my_ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.2&terminal_type=1&lang=zh-cn&v=4836&lang=zh"
        try:
            req = requests.get(url=url, headers=header).text
            retu = json.loads(req[7:-2])["msg"]
        except BaseException as ex:
            retu = req
        return retu
    
    #pyinstaller打包后无法使用os.path.dirname(os.path.realpath(__file__))获取目录
    def config_load():
        try:
            f = open(f"{os.path.dirname(os.path.realpath(sys.executable))}\setting")
            rc4 = rc4_decrypt(f.read())
            j = json.loads(rc4)
            config["account"] = j["account"]
            config["password"] = j["password"]
            config["type"] = j["type"]
            config["autoStart"] = j["autoStart"]
            #读取配置文件后自动登录
            if(config["account"] != "" and config["password"] != "" and config["type"] != "" and config["autoStart"] == 1):
                msgbox.showinfo("登录结果", loginNET(config["account"], config["password"], config["type"]))
                sys.exit()
        except FileNotFoundError:
            config_save()
        except UnsupportedOperation:
            config_save()
        except KeyError:
            config_save()
        except json.JSONDecodeError:
            msgbox.showerror("提示", "配置读取失败,可能是文件损坏或者使用了其他计算机的配置\n请删除配置文件再尝试启动！")
            sys.exit(0)
        except PermissionError:
            msgbox.showerror("提示", "配置文件无法访问！")
            sys.exit(0)
        #WRITE ICON_FILE
        tmp = open("temp.i", "wb+")
        tmp.write(base64.b64decode(icon))
        tmp.close()

    def config_save():
        f = open(f"{os.path.dirname(os.path.realpath(sys.executable))}\setting","w")
        j = json.dumps(config, sort_keys=False, indent=4, separators=(', ', ': '))
        #加密配置文件，防止账号泄露(如果算法被拿到了依旧可以解密
        rc4 = rc4_encrypt(j)
        f.write(rc4)
        f.close()

    def setIncon(tk: tkinter.Tk):
        tk.iconbitmap("temp.i")
        os.remove("temp.i")

    config_load()

    tk = tkinter.Tk()

    #设置窗口属性
    tk.title("校园网登录器(窗口版) by Th3Ra1nb0w")
    setIncon(tk)
    tk.geometry('388x180')
    tk.resizable(0,0)

    #设置窗口控件
    canvas = tkinter.Canvas(tk, width=200, height=200)
    canvas.place(x=5, y=3)
    canvas.create_text(20, 14, text="账号: ", font=('微软雅黑', 10))
    canvas.create_text(20, 50, text="密码: ", font=('微软雅黑', 10))

    box1 = tkinter.Entry(tk, width=20)
    box1.place(x=50, y=7)
    box2 = tkinter.Entry(tk, width=20)
    box2.place(x=50, y=43)

    listBox = ttk.Combobox(tk, state="readonly")
    listBox.grid(row=1, sticky="NW")
    listBox['value'] = ("中国移动", "中国电信", "中国联通")
    listBox.current(0)
    listBox.place(x=210, y=7)

    varB = tkinter.IntVar()
    varB.set(int(config["autoStart"]))

    #自启动注册表读写
    def register_system():
        config["autoStart"] = varB.get()
        path = os.path.dirname(os.path.realpath(sys.executable)) # 要添加的exe完整路径如：
        # 文件名(不含路径)
        fileAllName = os.path.basename(sys.argv[0])
        fileName = os.path.splitext(fileAllName)[0]
        # 注册表项名
        KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        infoText = ""
        if(varB.get() == 1): 
            infoText = "添加自启" 
        else:  
            infoText = "移除自启"
        # 异常处理
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            if(varB.get() == 1):
                win32api.RegSetValueEx(key, fileName, 0, win32con.REG_SZ, path + "\\" + fileAllName)
                win32api.RegCloseKey(key)
            else:
                win32api.RegDeleteValue(key, fileName)
        except:
            msgbox.showerror("提示", f'{infoText}失败')
            return
        msgbox.showinfo("提示", f'{infoText}成功！')
        config_save()
    
    cb = tkinter.Checkbutton(tk, text="开机启动", variable=varB, command=register_system)
    cb.place(x=45, y=70)

    #按钮事件
    def login():
        if (box1.get() != "" and box2.get() != ""):
            var = ""
            config["account"] = box1.get()
            config["password"] = box2.get()
            match listBox.get():
                case "中国移动":
                    var = "cmcc"
                case "中国电信":
                    var = "telecom"
                case "中国联通":
                    var = "unicom"
            config["type"] = var
            msgbox.showinfo("登录结果", loginNET(box1.get(), box2.get(), var))
            config_save()
        else:
            msgbox.showwarning("提示", "账号或密码不能为空!")
    
    button = tkinter.Button(text="登录", height=2, width=15, command=login)
    button.place(x=138, y=110)
    tk.mainloop()
    #os.system("pause")
