
import fitz
import re
import os
import ttkbootstrap as tk
from ttkbootstrap.constants import *

if os.path.exists('cache'):
    print('pass')
    pass
else:
    os.mkdir('cache')
    print('no')


cache_path = 'cache'

from tkinter.filedialog import (askopenfilename,
                                    askopenfilenames,
                                    askdirectory,
                                    asksaveasfilename)
from configparser import ConfigParser

import unicodedata
# 初始化配置文件
if os.path.exists('config.ini'):
    pass
else:
    with open('config.ini', 'w+', encoding='utf-8') as file:
        configure = f"""[comparing]
originalkey1 = \((.*?)\) \[(.*?)\((.*?)\)\]
targetkey1 =
originalkey2 = \((.*?)\) \[(.*?)\\]
targetkey2 =

[folder]
path = ./cache/
"""
        file.write(configure)
        file.close()

key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
pathKey = ConfigParser()
pathKey.read('config.ini', encoding='utf-8')
filepath = pathKey.get('folder', 'path')

def save_pdf_img(path, save_path):
    '''
    path: pdf的路径
    save_path : 图片存储的路径
    '''
    # 使用正则表达式来查找图片
    checkXO = r"/Type(?= */XObject)"
    checkIM = r"/Subtype(?= */Image)"
    # 打开pdf
    doc = fitz.open(path)
    # 图片计数
    imgcount = 0
    # 获取对象数量长度
    lenXREF = doc.xref_length()

    # 打印PDF的信息
    print("文件名:{}, 页数: {}, 对象: {}".format(path, len(doc), lenXREF - 1))

    # 遍历每一个图片对象
    for i in range(1, lenXREF):
        # 定义对象字符串
        text = doc.xref_object(i)
        # print(i,text)
        isXObject = re.search(checkXO, text)
        # 使用正则表达式查看是否是图片
        isImage = re.search(checkIM, text)

        # 如果不是对象也不是图片，则continue
        if not isXObject or not isImage:
            continue
        imgcount += 1
        # 根据索引生成图像
        pix = fitz.Pixmap(doc, i)
        # 根据pdf的路径生成图片的名称
        new_name = 'pic' + "_img{}.png".format(imgcount)
        new_name = new_name.replace(':', '')
        # 如果pix.n<5,可以直接存为PNG
        if pix.n < 5:
            pix._writeIMG(os.path.join(save_path, new_name), 1)
        # 否则先转换CMYK
        else:
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0._writeIMG(os.path.join(save_path, new_name), 1)
            pix0 = None
        # 释放资源
        pix = None
        print("提取了{}张图片".format(imgcount))




def multiconvert(path):
    for dir, dir_abs, files in os.walk(path):
        for file in files:
            try:
                if '.pdf' in file:
                    dirname = str(file).replace('.pdf', '')
                    picdir = dir + dirname + '/'
                    if os.path.exists(picdir):
                        pass
                    else:
                        os.mkdir(picdir)
                    filedir = dir + file
                    print(filedir)
                    print(picdir)
                    save_pdf_img(filedir, picdir)
            except:
                continue

class Window:
    button_list = []
    object_list = []

    def __init__(self):
        '''创建窗口和frame'''
        self.window = tk.Window()
        self.window.title('PDF2IMG')
        self.window.geometry('640x360')
        self.frame = tk.Frame(self.window)
        self.frame.place(x=300, y=160, anchor='center')
        self.frame_b = tk.Frame(self.frame)
        self.frame_b.pack(anchor='center', side='top')
        self.frame_l = tk.Frame(self.frame)
        self.frame_l.pack(anchor='center', side='bottom')
        self.text = tk.StringVar()

    def extract_pic(self):
        currentconfig = ConfigParser()
        currentconfig.read('config.ini', encoding='utf-8')
        filepathnow = currentconfig.get('folder', 'path')
        multiconvert(filepathnow + '/')

    def change_Path(self):
        # 选择文件并更新显示当前配置
        directory = askdirectory()
        if directory == '':
            pass
        else:
            pathKey.set('folder', 'path', directory)
            self.text.set(directory)
        with open('config.ini', 'w', encoding='utf-8') as f:
            pathKey.write(f)


    def show_info(self):
        try:
            self.frame_b.destroy()
        except:
            print('按钮非显示状态')

        labelinfo = tk.Label(self.frame_l, text='✳本操作会遍历目录下全部PDF文件')
        labelinfo.grid(row=1, column=2, padx=20, pady=5)

        btn6 = tk.Button(self.frame_l, text='点击开始转换', width=15, bootstyle=PRIMARY,
                         command=self.extract_pic)
        btn6.grid(row=2, column=2, padx=20, pady=20)
        btn6 = tk.Button(self.frame_l, text='修改路径', width=15, bootstyle=(PRIMARY, OUTLINE),
                         command=self.change_Path)
        btn6.grid(row=3, column=2, padx=20, pady=20)
        self.text.set('当前路径：%s' % filepath)
        labelinfosnos = tk.Label(self.frame_l, textvariable=self.text)
        labelinfosnos.grid(row=4, column=2, padx=20, pady=20)

    def new_button(self):
        '''创建展示按钮'''"开始检测和显示结果可在此处新添加tk.button"
        self.startbtn = tk.Button(self.frame_b, text='欢迎使用', width=10, bootstyle=PRIMARY,
                  command=self.show_info).pack()

    def run(self):
        '''主程序调用'''
        self.window.mainloop()

if __name__ == '__main__':
    w = Window()
    w.new_button()
    w.run()