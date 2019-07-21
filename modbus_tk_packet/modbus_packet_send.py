##interface 1:sign in
##include ip & port
##  @smart manufactory 2019
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import tkinter as tk
import os
from tkinter.filedialog import askopenfilename as askopfile

class GetCode:    
    def __init__(self, windows=None):
        self.window = window
        self.data={}  # 存放返回值
        self.var_port = tk.StringVar()
        self.var_port.set('1000')
        #self.var_port.set('5020')
        
        e = tk.Entry(self.window,textvariable=self.var_port,font=('Arial',12)).place(x=60,y=20)
        self.var_report = tk.StringVar()
        self.var_report.set('port: ')
        l1 = tk.Label(self.window,textvariable=self.var_report,font=('Arial',12)).place(x=20,y=20)

        self.var_ip = tk.StringVar()
        self.var_ip.set('192.168.1.1')
        #self.var_ip.set('127.0.0.1')
        e = tk.Entry(self.window,textvariable=self.var_ip,font=('Arial',12)).place(x=60,y=60)
        self.var_reip = tk.StringVar()
        self.var_reip.set('IP: ')
        l2 = tk.Label(self.window,textvariable=self.var_reip,font=('Arial',12)).place(x=20,y=60)
        b = tk.Button(self.window,text='enter',width=13,height=2,command=self.enter).place(x=100,y=100)
    def enter(self):
        self.data["port"] = self.var_port.get()
        self.data["ip"] = self.var_ip.get()
        print(self.data["port"],self.data["ip"])
        client = ModbusClient(self.data["ip"], self.data["port"])

        


if __name__ == '__main__':
    window = tk.Tk()
    window.title('my modbus')
    window.geometry('300x150')
    window.resizable(width=False,height=False)
    GetCode(window)
    
    window.mainloop()
