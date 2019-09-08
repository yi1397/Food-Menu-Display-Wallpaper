#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ctypes
import time
import shutil
import os

setting = {}

def check_folder():
    mp4Dir = r"C:\wallpaper_changer"
    if not os.path.isdir(mp4Dir):
        os.mkdir(mp4Dir)


# 프로그램이 설정값을 불러오는 함수
def get_setting():
    mp4Dir = r"C:\wallpaper_changer\set.txt"
    if not os.path.isfile(mp4Dir):
        f = open(r"C:\wallpaper_changer\set.txt", 'w')
        f.write('box_x1 =1350\nbox_x2 =1850\nbox_y1 =100\nbox_y2 =1050\nbox_color =khaki\nfont_size =36\n')
        f.close()
    f = open(r'C:\wallpaper_changer\set.txt', 'r')
    lines = f.readlines()
    f.close()
    for i in lines:
        line = i.split(' =')
        line[1] = line[1][:-1]
        setting[line[0]] = line[1]


# 기존 바탕화면 이미지가 저장된 경로를 찾아내는 함수
def find_wallpaper_path():
    shutil.copy('C:/Users/user/AppData/Local/Microsoft/Windows/Themes/Custom.theme', 'theme.txt')
    f = open('C:/Users/user/AppData/Local/Microsoft/Windows/Themes/Custom.theme', 'rb')
    while True:
        try:
            line = f.readline()
            line = line.decode('cp949 ')
            if line is '':
                return -1
            if 'Wallpaper'in line:
                path = line[10:-2]
                if '%USERPROFILE%' in path:
                    path = r'c:\users\user' + path[13:]
                if '%SystemDrive%' in path:
                    path = r'c:' + path[13:]
                if '%SystemRoot%' in path:
                    path = r'c:\windows' + path[12:]
                return path
        except:
            pass


def get_html(url):
    _html = ""
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            _html = resp.text
    except:
        time.sleep(10)
        return get_html(url)
    return _html


def get_diet(code, ymd):
    schMmealScCode = code  # int
    schYmd = ymd  # str
    num = int((datetime.datetime.today().weekday()+1)%7)
    URL = (
            "https://stu.dje.go.kr/sts_sci_md01_001.do?"
            "domainCode=G10&schulKndScCode=4&schulCrseScCode=4&schulCode=G100000170&schMmealScCode=%s&schYmd=%s" % (schMmealScCode, schYmd)
    )
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find_all("tr")
    element = element[2].find_all('td')
    try:
        element = element[num]  # num
        element = str(element)
        element = element.replace('amp;', '')
        element = element.replace('[', '')
        element = element.replace(']', '')
        element = element.replace('<br/>', '\n')
        element = element.replace('<td class="textC last">', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('</td>', '')
        element = element.replace('(h)', '')
        element = element.replace('.', '')
        element = re.sub(r"\d", "", element)
    except:
        element = " "
    return element


def draw_loading_img():
    img = Image.open(find_wallpaper_path())
    ctypes.windll.user32.SetProcessDPIAware()
    img = img.resize((ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)))
    draw = ImageDraw.Draw(img)
    x1 = int(setting['box_x1'])
    y1 = int(setting['box_y1'])
    x2 = int(setting['box_x2'])
    y2 = int(setting['box_y2'])
    box = Image.new("RGB", (x2 - x1, y2 - y1), "khaki")
    img.paste(box, (x1, y1, x2, y2))
    font = ImageFont.truetype('gulim.ttc', 36)
    draw.text((x1 + 100, y1 + 100), '인터넷 로딩중...', (0, 0, 0), font)
    img.save(r"C:\wallpaper_changer\loading.jpg")
    path = r"C:\wallpaper_changer\loading.jpg"
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

    
# 데이터 문자열을 이미지에 적고 바탕화면에 적용하는  
def draw_list_img():
    food = []
    food.append(get_diet(1, datetime.datetime.today().strftime("%Y.%m.%d")).split('\n'))
    food.append(get_diet(2, datetime.datetime.today().strftime("%Y.%m.%d")).split('\n'))
    food.append(get_diet(3, datetime.datetime.today().strftime("%Y.%m.%d")).split('\n'))
    img = Image.open(find_wallpaper_path())
    ctypes.windll.user32.SetProcessDPIAware()
    img = img.resize((ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)))
    draw = ImageDraw.Draw(img)
    x1 = int(setting['box_x1'])
    y1 = int(setting['box_y1'])
    x2 = int(setting['box_x2'])
    y2 = int(setting['box_y2'])
    box = Image.new("RGB", (x2 - x1, y2 - y1), "khaki")
    img.paste(box, (x1, y1, x2, y2))
    font = ImageFont.truetype('gulim.ttc', 30)
    cnt = 0
    for i in food:
        for j in i:
            cnt += 35
            draw.text((x1 + 60, y1 + 30 + cnt), j, (0, 0, 0), font)
    img.save(r"C:\wallpaper_changer\result.jpg")
    path = r"C:\wallpaper_changer\result.jpg"
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)


def main():
    check_folder()
    get_setting()
    draw_loading_img()
    draw_list_img()

main()
