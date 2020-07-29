from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import getpass
from bs4 import BeautifulSoup
import os


def get_music(playlist_id):
    playlist_Ids = []
    music_Ids = []
    playlist_information = {}
    playlist_url = 'https://music.163.com/#/my/m/music/playlist?id=' + playlist_id

    # 设置chrome浏览器无界面模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    print('\033[0;32m---->\033[0m  正在转到登录界面…………')
    browser.get('https://music.163.com/#login')
    time.sleep(1)
    browser.switch_to.frame(browser.find_element_by_id('g_iframe'))
    other = browser.find_element_by_class_name('other')
    other.click()
    law = browser.find_element_by_id('j-official-terms')
    law.click()
    telephone_login = browser.find_element_by_class_name('u-btn2-2')
    telephone_login.click()
    browser.switch_to.default_content()

    def login():
        print('\033[0;32m---->\033[0m  请输入网易云音乐账号与密码')
        number = input('       手机号：  ')
        pw = getpass.getpass('       密码（自动隐藏）：  ')
        telephone_number = browser.find_element_by_id('p')
        password = browser.find_element_by_id('pw')
        telephone_number.clear()
        password.clear()
        telephone_number.send_keys(number)
        password.send_keys(pw)
        sure = browser.find_element_by_class_name('j-primary')
        sure.click()

    os.system('cls')
    login()
    time.sleep(0.5)
    while True:
        try:
            browser.find_element_by_class_name('u-err')
            print('\033[7;31m---->  密码错误，请重试: \033[0m')
            login()
            time.sleep(1)
        except:
            break
    time.sleep(2)
    os.system('cls')
    print('\033[0;32m---->\033[0m  尝试查找音乐列表，请耐心等待……')
    my_music = browser.find_element_by_link_text('我的音乐')
    my_music.click()
    browser.switch_to.frame(browser.find_element_by_id('g_iframe'))
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    playlist = soup.select('div.n-minelst-1')[0].select('li.j-iflag')
    playlist_name = soup.select('div.j-flag div.cnt h2.f-thide')[0].text
    print('\033[0;32m---->\033[0m  正在尝试获取歌曲链接')
    for i in playlist:
        data_matcher = i['data-matcher']
        link = data_matcher.split('-')[1]
        playlist_Ids.append(link)
    check = playlist_id in playlist_Ids
    if check:
        browser.get(playlist_url)
        time.sleep(2)
        browser.switch_to.frame(browser.find_element_by_id('g_iframe'))
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        musicIds = soup.select('table.m-table tbody span.txt a')
        for i in musicIds:
            music_id = i['href']
            music_id = music_id.split('=')[1]
            music_Ids.append(music_id)
        browser.close()
    else:
        print('\033[0;31m---->  未在"创建的歌单中"找到，请在手机端将所需歌曲收藏的你自己所创建的歌单后再做尝试 \033[0m')
        time.sleep(2)
        print('\033[0;32m---->  程序正在退出中……')
        browser.close()
    playlist_information['name'] = playlist_name
    playlist_information['music'] = music_Ids
    return playlist_information
