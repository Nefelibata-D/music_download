import requests
from selenium_get_music import get_music
import os

# 音乐文件名自动调整，删除异常符号
def name_check(name):
    position = name.find('?')
    if position != -1:
        print('\033[0;33m---->Warning!\033[0m  原音乐文件命名不规范，正在尝试删除不规范字符')
        name = name[0:position] + name[position + 1:-1]
    position = name.find('/')
    if position != -1:
        print('\033[0;33m---->Warning!\033[0m  原音乐文件命名不规范，正在尝试删除不规范字符')
        name = name[0:position] + name[position + 1:-1]
    position = name.find('<')
    if position != -1:
        print('\033[0;33m---->Warning!\033[0m  原音乐文件命名不规范，正在尝试删除不规范字符')
        name = name[0:position] + name[position + 1:-1]
    position = name.find('>')
    if position != -1:
        print('\033[0;33m---->Warning!\033[0m  原音乐文件命名不规范，正在尝试删除不规范字符')
        name = name[0:position] + name[position + 1:-1]
    position = name.find('|')
    if position != -1:
        print('\033[0;33m---->Warning!\033[0m  原音乐文件命名不规范，正在尝试删除不规范字符')
        name = name[0:position] + name[position + 1:-1]
    return name


class cloudmusic_playlist:
    # noinspection PyUnboundLocalVariable
    def playlist_patch(self, url):
        playlist = {}
        playlist_id = url.split("&")[0].split("=")[1]
        music_Ids = get_music(playlist_id)['music']
        os.system('cls')
        number = len(music_Ids)
        times = 0
        print('\033[0;32m---->\033[0m  已返回音乐数据')
        print('\033[0;32m---->\033[0m  正在处理音乐数据…………')
        print('\033[0;32m------>\033[0m      \033[7;32m处理数据进程如下：\033[0m     \033[0;32m<------\033[0m  ')
        print('  ')
        print('\033[0;32m---->\033[0m  共 {} 条数据待处理'.format(number))
        print('  ')
        for trackId in music_Ids:
            res = requests.get('https://api.imjad.cn/cloudmusic/?type=detail&id={}'.format(trackId))
            song_name = res.json()['songs'][0]['name']  # 获得音乐名称
            singer = res.json()['songs'][0]['ar'][0]['name']  # 获得歌手名称
            name = singer + ' - ' + song_name
            times += 1
            print('\r' + '\033[0;32m---->\033[0m  处理数据中……  已处理: {}'.format(times), end="")
            playlist[name] = str(trackId)
        return playlist



    def download(self, song_id, name, list_long, times, position):
        print('\033[0;32m---->\033[0m  正在提交线程 ， 已提交任务数：{} ，提交百分比为：{}%'.format(times, round(times / list_long * 100, 1)))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4033.0 Safari/537.36 Edg/81.0.403.1 '
        }
        # 进行歌曲爬取与下载
        res = requests.get('http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id), headers=headers)
        if res.status_code != 200:
            return '\033[7;31m---->  未接收到指定服务器反馈，请检查网络连接，或该ip已经被服务器封禁，请待会再试\033[0m'
        elif res.encoding == 'utf8':
            print('\033[7;31m---->  || 状态：下载失败  ||  歌曲名: {} ||\033[0m'.format(name))
            return name
        try:
            with open(position + '//music_download//' + name + '.mp3', 'wb') as file:
                file.write(res.content)
                print('\033[0;32m---->\033[0m  || 状态：下载成功  ||  歌曲名: {} '.format(name))
        except:
            print('\033[7;31m---->  ||状态：出现错误 || 歌名命名失败 || 尝试自动调整\033[0m')
            position = name.find('-')
            if position != -1:
                name = name[0:position] + '(强制重新命名)'
                try:
                    with open(position + '//music_download//' + name + '.mp3', 'wb') as file:
                        file.write(res.content)
                        print('\033[0;32m---->\033[0m  || 状态：下载成功  ||  歌曲名: {} '.format(name))
                        print('  ')
                except:
                    print('\033[7;31m---->  ||状态：下载失败 || 文件命名失败  || 歌曲名：{}\033[0m'.format(name))
