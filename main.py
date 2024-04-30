import customtkinter as ctk
from customtkinter import INSERT
from customtkinter import CTkLabel as Label
from customtkinter import CTkComboBox as Combobox
import os
from PIL import Image
import json
import threading

import date_frame
from caculate import cacu

ctk.set_widget_scaling(1.0)


def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


def is_lyear(year):
    if year % 4 == 0 and year % 100 != 0:
        return True
    elif year % 400 == 0:
        return True
    else:
        return False


class ScrollableRadiobuttonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, text_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item, text_list[i])

    def add_item(self, item, text):
        radiobutton = ctk.CTkRadioButton(self, text=text, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()


def main():
    top = ctk.CTk()  # top level window
    top.geometry('1200x630')  # window size
    top.title('Plum Blossom Numerology')  # window
    top.resizable(height=True, width=True)
    top.columnconfigure(1, weight=1)
    # Plum Blossom Numerology
    label = ctk.CTkLabel(top, text='Plum Blossom Numerology', font=('', 15), width=300)
    label.grid(row=0, column=1, sticky='w')

    # Time Container
    fram_time = ctk.CTkFrame(top, width=400)
    fram_time.grid(row=1, column=0, padx=30)

    def change_day(chioces):
        y = int(cbox_year.get())
        m = int(cbox_mon.get())
        monl1 = [1, 3, 5, 7, 8, 10, 12]
        monl2 = [4, 6, 9, 11]
        if m in monl1:
            d_li = [str(i) for i in range(1, 32)]
        elif m in monl2:
            d_li = [str(i) for i in range(1, 31)]
        else:
            if is_lyear(y):
                d_li = [str(i) for i in range(1, 30)]
            else:
                d_li = [str(i) for i in range(1, 29)]
        cbox_day.configure(values=d_li)

    yyyy = [str(i) for i in range(2000, 2050)]
    cbox_year = ctk.CTkComboBox(fram_time, width=80, values=yyyy, command=change_day)
    cbox_year.grid(row=1, column=0)
    label_year = ctk.CTkLabel(fram_time, text='Year', font=('', 13), width=20, height=1)
    label_year.grid(row=1, column=1)

    mm = [str(i) for i in range(1, 13)]
    cbox_mon = ctk.CTkComboBox(fram_time, width=50, values=mm, command=change_day)
    cbox_mon.grid(row=1, column=2)

    label_mon = Label(fram_time, text='Month', font=('', 13), width=20, height=1)
    label_mon.grid(row=1, column=3)

    dd = [str(i) for i in range(1, 32)]
    cbox_day = Combobox(fram_time, width=70, values=dd)
    cbox_day.grid(row=1, column=4)

    label_day = Label(fram_time, text='Day', font=('', 13), width=20, height=1, )
    label_day.grid(row=1, column=5)

    hh = [str(i) for i in range(0, 24)]
    cbox_hour = Combobox(fram_time, width=70, values=hh)
    cbox_hour.grid(row=1, column=6)

    label_hour = Label(fram_time, text='Hour', font=('', 13), width=3, height=1)
    label_hour.grid(row=1, column=7)

    '''start'''
    cont = ''
    p1_path = './source/'
    p2_path = r"./source/"
    photo1 = ctk.CTkImage(dark_image=Image.open(os.path.join(p1_path, "乾.png")), size=(70, 55))
    photo2 = ctk.CTkImage(dark_image=Image.open(os.path.join(p2_path, "乾.png")), size=(70, 55))

    # event
    def call_run():
        global cont, photo1, photo2
        ye, mo, da, ho = int(cbox_year.get()), int(cbox_mon.get()), int(cbox_day.get()), int(cbox_hour.get())
        if mo in [4, 6, 9, 11] and da > 30:
            da = 30
        if mo == 2 and is_lyear(ye) and da > 29:
            da = 29
        if mo == 2 and (not is_lyear(ye)) and da > 28:
            da = 28
        rr = cacu(ye, mo, da, ho)
        cont = rr[0]
        i1 = rr[1]
        i2 = rr[2]
        cont = cont + '\n' + str(ye) + ' year(年)' + str(mo) + ' month(月)' + str(da) + ' day(日)' + str(ho) + ' hour(时)'
        p1_path = r"./source/"
        p2_path = r"./source/"
        photo1 = ctk.CTkImage(dark_image=Image.open(os.path.join(p1_path, f"{i1}.png")), size=(70, 55))
        photo2 = ctk.CTkImage(dark_image=Image.open(os.path.join(p2_path, f"{i2}.png")), size=(70, 55))
        content_label.configure(text=cont)
        img_label1.configure(image=photo1)
        img_label2.configure(image=photo2)

        value = rr[3]
        js_go = open("./source/go_en.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, value + '\n' + js_go[value])

    # 万物类象-按钮事件
    def call_world():
        newWindow = ctk.CTkToplevel(top)
        newWindow.geometry('600x600')  # 设置窗口大小
        newWindow.title('万物类象 (All Things)')  # 设置窗口标题
        newWindow.resizable(height=False, width=False)
        newWindow.attributes('-topmost', 'true')
        # 万物类象-点击
        def wanwu_click():
            t = str(wanwu_lis.get_checked_item())
            js_world = open("./source/world_en.json", encoding='utf-8')
            js_world = json.load(js_world)
            txt_world.delete('1.0', 'end')
            txt_world.insert(INSERT, t + '\n\n' + js_world[t])

        # 万物类象-列表框
        l_w = ['乾卦', '坤卦', '坎卦', '艮卦', '震卦', '离卦', '兑卦', '巽卦']
        l_w_english = ['乾卦 - Qian Gua', '坤卦 - Kun Gua', '坎卦 - Kan Gua', '艮卦 - Gen Gua', '震卦 - Zhen Gua', '离卦 - Li Gua', '兑卦 - Dui Gua', '巽卦 - Xun Gua']
        wanwu_lis = ScrollableRadiobuttonFrame(master=newWindow, width=200, height=250,
                                               command=wanwu_click,
                                               item_list=[f"{i}" for i in l_w],
                                               text_list=[f"{i}" for i in l_w_english],
                                               label_text="")
        wanwu_lis.grid(row=0, column=0, padx=0, pady=10, sticky='en')
        # 万物类象查询结果显示框
        txt_world = ctk.CTkTextbox(newWindow, width=380, height=450, undo=True, autoseparators=False, wrap='word')
        txt_world.insert(INSERT, 'Search Results will be shown here!')
        txt_world.grid(row=0, column=1, padx=0, pady=10, sticky='en')


    # 主功能按钮容器：起卦，立即起卦，字典，万年历，万物类象
    def main_button():
        fram_btn = ctk.CTkFrame(top)
        fram_btn.grid(row=3, column=0, sticky='n')
        # Start Divination - Button
        btn_run = ctk.CTkButton(fram_btn, text='起卦 (Start Divination)', font=('华文行楷', 20), width=60, height=40, command=call_run)
        btn_run.grid(row=0, column=0, padx=5, pady=5)
        # All Things - Button
        btn_world = ctk.CTkButton(fram_btn, text='万物类象 (All Things)', font=('华文行楷', 20), width=60, height=40, command=call_world)
        btn_world.grid(row=1, column=0, padx=5, pady=5)

    # 底部
    # 下方文字
    label_word = ctk.CTkLabel(top, text='Literature in the Age of Artificial Intelligence Project', font=("", 17))
    label_word.grid(row=4, column=0, padx=30, pady=5, columnspan=3, sticky='w')
    main_button()
    '''END'''

    # 显示区：卦象，卦图，详细内容
    # 卦象显示
    fram_show = ctk.CTkFrame(top)
    fram_show.grid(row=2, column=2, padx=20)
    content_label = Label(fram_show, text='The hexagram (卦象) is displayed here', font=('黑体', 13), wraplength=190, anchor='n', width=10, height=8,
                          justify='left')
    content_label.grid(row=0, column=0, rowspan=2, padx=20)
    # 卦图显示
    img_label1 = Label(fram_show, width=60, height=50, image=photo1, text='')
    img_label1.grid(row=0, column=1, padx=10, pady=7)
    img_label2 = Label(fram_show, width=60, height=50, image=photo2, text='')
    img_label2.grid(row=1, column=1, padx=10, pady=7)
    # 详细内容

    txt = ctk.CTkTextbox(top, width=340, height=365, undo=True, autoseparators=False, wrap='word')
    txt.insert(INSERT, 'Search Results will be shown here!')
    txt.grid(row=3, column=2, padx=0, pady=10, rowspan=2, sticky='n')
    '''END'''

    # 详细-按钮事件
    def call_detail():
        t = f"{top.scrollable_radiobutton_frame.get_checked_item()}"
        if t == '':
            t = '乾为天'
        js_detail = open("./source/detail_en.json", encoding='utf-8')
        js_detail = json.load(js_detail)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, t + '\n' + js_detail[t])

    # 详细-按钮
    btn_detail = ctk.CTkButton(fram_show, text='详  细(Details)', font=('华文行楷', 20), width=20, height=30, command=call_detail)
    btn_detail.grid(row=1, column=2, padx=10, sticky='s')
    # 查询框
    l2 = ['乾为天', '坤为地', '水雷屯', '山水蒙', '水天需', '天水讼', '地水师', '水地比', '风天小畜', '天泽履', '地天泰', '天地否', '天火同人', '火天大有', '地山谦',
          '雷地豫', '泽雷随', '山风蛊', '地泽临', '风地观', '火雷噬嗑', '山火贲', '山地剥', '地雷复', '天雷无妄', '山天大畜', '山雷颐', '泽风大过', '坎为水', '离为火',
          '泽山咸', '雷风恒', '天山遯', '雷天大壮', '火地晋', '地火明夷', '风火家人', '火泽睽', '水山蹇', '雷水解', '山泽损', '风雷益', '泽天夬', '天风姤', '泽地萃',
          '地风升', '泽水困', '水风井', '泽火革', '火风鼎', '震为雷', '艮为山', '风山渐', '雷泽归妹', '雷火丰', '火山旅', '巽为风', '兑为泽', '风水涣', '水泽节',
          '风泽中孚', '雷山小过', '水火既济', '火水未济']
    l2_english = [
    '乾为天 - Qian as Heaven',
    '坤为地 - Kun as Earth',
    '水雷屯 - Water and Thunder Accumulating',
    '山水蒙 - Mountain and Water Covering',
    '水天需 - Water and Heaven Needing',
    '天水讼 - Heaven and Water Contending',
    '地水师 - Earth and Water Army',
    '水地比 - Water and Earth Comparing',
    '风天小畜 - Wind and Heaven Accumulating Small',
    '天泽履 - Heaven and Marsh Treading',
    '地天泰 - Earth and Heaven Peace',
    '天地否 - Heaven and Earth Denial',
    '天火同人 - Heaven and Fire Fellowship',
    '火天大有 - Fire and Heaven Great Possession',
    '地山谦 - Earth and Mountain Modesty',
    '雷地豫 - Thunder and Earth Preceding',
    '泽雷随 - Marsh and Thunder Following',
    '山风蛊 - Mountain and Wind Repairing',
    '地泽临 - Earth and Marsh Overseeing',
    '风地观 - Wind and Earth Observing',
    '火雷噬嗑 - Fire and Thunder Biting Through',
    '山火贲 - Mountain and Fire Adorning',
    '山地剥 - Mountain and Earth Peeling',
    '地雷复 - Earth and Thunder Returning',
    '天雷无妄 - Heaven and Thunder Without Falsehood',
    '山天大畜 - Mountain and Heaven Storing Great',
    '山雷颐 - Mountain and Thunder Nourishment',
    '泽风大过 - Marsh and Wind Great Exceeding',
    '坎为水 - Kan as Water',
    '离为火 - Li as Fire',
    '泽山咸 - Marsh and Mountain Salty',
    '雷风恒 - Thunder and Wind Persevering',
    '天山遯 - Heaven and Mountain Withdrawing',
    '雷天大壮 - Thunder and Heaven Great Strength',
    '火地晋 - Fire and Earth Progressing',
    '地火明夷 - Earth and Fire Darkening of the Light',
    '风火家人 - Wind and Fire Family',
    '火泽睽 - Fire and Marsh Opposing',
    '水山蹇 - Water and Mountain Hindered',
    '雷水解 - Thunder and Water Dispersing',
    '山泽损 - Mountain and Marsh Diminishing',
    '风雷益 - Wind and Thunder Increasing',
    '泽天夬 - Marsh and Heaven Deciding',
    '天风姤 - Heaven and Wind Encountering',
    '泽地萃 - Marsh and Earth Gathering',
    '地风升 - Earth and Wind Ascending',
    '泽水困 - Marsh and Water Exhausted',
    '水风井 - Water and Wind Well',
    '泽火革 - Marsh and Fire Revolution',
    '火风鼎 - Fire and Wind Cauldron',
    '震为雷 - Zhen as Thunder',
    '艮为山 - Gen as Mountain',
    '风山渐 - Wind and Mountain Gradually',
    '雷泽归妹 - Thunder and Marsh Marrying Maiden',
    '雷火丰 - Thunder and Fire Abundance',
    '火山旅 - Fire and Mountain Traveler',
    '巽为风 - Xun as Wind',
    '兑为泽 - Dui as Marsh',
    '风水涣 - Wind and Water Dissipating',
    '水泽节 - Water and Marsh Restricting',
    '风泽中孚 - Wind and Marsh Inner Trust',
    '雷山小过 - Thunder and Mountain Small Exceeding',
    '水火既济 - Water and Fire Already Completed',
    '火水未济 - Fire and Water Not Yet Completed'
    ]


    def radiobutton_frame_event():
        t = f"{top.scrollable_radiobutton_frame.get_checked_item()}"
        print(t)
        js_go = open("./source/go_en.json", encoding='utf-8')
        js_go = json.load(js_go)
        txt.delete('1.0', 'end')
        txt.insert(INSERT, t + '\n' + js_go[t])

    top.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=top, width=300, height=350,
                                                                  command=radiobutton_frame_event,
                                                                  item_list=[f"{i}" for i in l2],
                                                                  text_list=[f"{i}" for i in l2_english],
                                                                  label_text="")
    top.scrollable_radiobutton_frame.grid(row=3, column=1, padx=0, pady=10, sticky='en')
    '''END'''
    top.mainloop()


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    main()
