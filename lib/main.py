"""
    ===================================================================+
    *                                                                  *
    *    因为网易云音乐的网页端改版, 所有与网易云音乐下载有关的代码         *
    *    已全部失效, 无法使用, 望谅解                                    *
    *                                                                  *
    *    现已暂停网易云音乐下载服务，可能会重构代码。                      *
    *                                                                  *
    *    Latest Update : 2020.07.12                                    *
    *                                                                  *
    *    代码已重构，重新采用selenium模块，并调用chromewebdriver          *
    *                                                                  *
    *    Latest Update : 2020.07.24
    +==================================================================+
"""

import os
import time
from concurrent import futures
from cloudmusic_playlist_download import cloudmusic_playlist, name_check
from kugoumusic_song_download import kugoumusic_song

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
position = BASE_DIR

print('欢迎使用该音乐下载软件，目前支持网易云音乐的歌单音乐一次性下载以及酷狗音乐的单曲搜索')
print('为了提升下载速度，本程序已尝试在网易云音乐代码中开启多线程工作，默认线程为10')
print('3秒后程序开始运行……')
time.sleep(3)
os.system('cls')
if os.path.exists(position + '\\music_download'):
    print('\033[0;32m---->\033[0m  已检测到下载路径！')
else:
    print('\033[0;31m----!  未检测到下载路径！尝试创建下载路径！\033[0m')
    try:
        os.mkdir(position + '\\music_download')
        print('\033[0;32m---->\033[0m  创建成功！')
    except:
        print('\033[0;31m----!  创建失败！请尝试授予管理员权限后运行！')

workers = input('\033[0;32m---->\033[0m  请输入同时下载歌曲数（系统默认为10）：  ')
if workers:
    if int(workers) <= 10:
        max_workers = int(workers)
    else:
        a = input('\033[0;33m---->Warning!\033[0m  建议同时下载数量不要大于10,是否调整为10[Y/N]:  ')
        if a == 'N' or 'No' or 'no':
            max_workers = int(workers)
        else:
            max_workers = 10
else:
    max_workers = 10
# 初始化线程池
executor = futures.ThreadPoolExecutor(max_workers=max_workers)
# 给予对象实例
cloud = cloudmusic_playlist()

choice_method = int(input('\033[0;32m---->\033[0m  请选择下载方式： 网易云音乐【1】  酷狗音乐【2】'))


# 酷狗音乐下载部分：0
def kugou():
    print('\n')
    song_name = input('请输入你需要查找的歌曲：   ')
    kugou = kugoumusic_song(song_name)
    kugou.song_search()
    times = 0
    for i in kugou.song_information:
        if i['FileHash'] != '':
            if i['HQFileHash'] != '':
                if i['SQFileHash'] != '':
                    print('歌名：{}  歌手：{}  音质：一般音质、HQ音质、SQ音质  【{}】'.format(i['song_full_name'], i['song_singer'], times))
                else:
                    print('歌名：{}  歌手：{}  音质：一般音质、HQ音质  【{}】'.format(i['song_full_name'], i['song_singer'], times))
            else:
                print('歌名：{}  歌手：{}  音质：一般音质  【{}】'.format(i['song_full_name'], i['song_singer'], times))
        else:
            print('歌名：{}  歌手：{}  音质：未找到相关音质  【{}】'.format(i['song_full_name'], i['song_singer'], times))
        times += 1
    print('')
    print('')
    print('歌曲音质对应序号：   一般音质 【0】     HQ音质 【1】     SQ音质 【2】')

    choice_1 = int(input('请输入需要的歌曲所对应数字   '))
    song = kugou.song_information[choice_1]
    choice_2 = int(input('请输入该歌曲所需音质，请勿输错序号！  '))
    print('正在尝试下载！')
    if choice_2 == 0:
        try:
            song_name = song['song_name']
            FileHash = song['FileHash']
            kugou.File_normal_mp3(song_name, FileHash)
        except:
            print('下载失败！')
    elif choice_2 == 1:
        try:
            song_name = song['song_name']
            FileHash = song['HQFileHash']
            kugou.File_HQ_mp3(song_name, FileHash)
        except:
            print('下载失败！')
    elif choice_2 == 2:
        try:
            song_name = song['song_name']
            FileHash = song['SQFileHash']
            kugou.File_SQ_mp3(song_name, FileHash)
        except:
            print('下载失败！')


# 网易云音乐下载部分：
if choice_method == 1:
    os.system('cls')
    url = input('\033[0;32m---->\033[0m  请输入网易云音乐歌单链接：   ')
    playlist = cloud.playlist_patch(url)
    times = 0
    fs = []
    list_long = len(playlist.keys())
    time.sleep(2)
    os.system('cls')
    print('开始音乐下载！')
    print('  ')
    print('\033[0;33m---->Warning!\033[0m   部分歌曲可能为VIP试听歌曲，无法获得下载权限')
    print('\033[0;33m---->Warning!\033[0m    失败歌曲将存入列表，等待下载完会自动调用酷狗音乐接口再次尝试！')
    print('\033[0;32m------>\033[0m      \033[7;32m下载进度输出：\033[0m     \033[0;32m<------\033[0m  ')
    print('  ')
    print('  ')
    for name, song_id in playlist.items():
        times += 1
        name = name_check(name)
        fs.append(executor.submit(cloud.download, song_id, name, list_long, times, position))
    fail = []
    futures.wait(fs)
    for f in fs:
        if f.result() is not None:
            fail.append(f.result())

    if fail:
        print('\033[0;32m---->\033[0m  自动调用酷狗接口二次尝试中！')
        for name in fail:
            kugou = kugoumusic_song(name)
            kugou.song_search()
            music = kugou.song_information[0]
            if music['FileHash'] != '':
                print('\033[0;32m---->\033[0m  歌名：{}  歌手：{}  音质：一般音质'.format(music['song_full_name'], music['song_singer']))
                try:
                    song_name = music['song_name']
                    FileHash = music['FileHash']
                    kugou.File_normal_mp3(song_name, FileHash)
                except:
                    print('\033[7;31m---->  下载失败！\033[0m')

if choice_method == 2:
    while True:
        kugou()
