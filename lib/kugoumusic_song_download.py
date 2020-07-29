import requests
from urllib import parse
import os


class kugoumusic_song:
    def __init__(self, name):
        self.song_name = name
        self.song_name_quote = parse.quote(self.song_name)
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4033.0 Safari/537.36 Edg/81.0.403.1',
            'referer': 'https://www.kugou.com/'
        }
        self.session.headers.update(self.headers)
        self.song_information = []
        self.fail_name = {}
        self.position = os.getcwd()
        self.cookies = 'kg_mid=b9549451fc08c8f895c4c7aa33bf1d78; kg_dfid=3Ljox00DuqF50gQvpw0MPFuK; ' \
                       'KuGooRandom=66931580632586722; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1580798937,1580965509,' \
                       '1581226017,1581226439; PHPSESSID=enroi798oj5mae76lmuggpl557; ' \
                       'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1581297099 '

    '''
    def get_cookies(self):
        #由于未学习到，暂且不进行编写，下面的cookies由自己手动传入
        url = 'https://songsearch.kugou.com/song_search_v2?keyword=%E5%91%8A%E7%99%BD%E3%81%AE%E5%A4%9C&page=1&pagesize=10'
        browser = webdriver.Chrome()
        browser.get(url)
        cookies = (browser.get_cookies()
        browser.close()
        print(self.cookies)
    '''

    def song_search(self):
        """
        为了方便后期的相似度匹配，在这里我页面爬取个数值取得是10，在最后记得要将设置交回用户!
        """
        song_search_url = 'https://songsearch.kugou.com/song_search_v2?keyword={}&page=1&pagesize={}&platform=WebFilter'.format(self.song_name_quote, 30)
        res = self.session.get(song_search_url)
        json = res.json()
        information = json['data']['lists']
        for i in information:
            song = {
                'song_name': i['SongName'].split('(')[0],
                'song_full_name': i['SongName'],
                'song_suffix': i['Suffix'],
                'song_singer': i['SingerName'],
                'FileHash': i['FileHash'],
                'ExtName': i['ExtName'],
                'HQExtName': i['HQExtName'],
                'HQFileHash': i['HQFileHash'],
                'ResFileHash': i['ResFileHash'],
                'SQExtName': i['SQExtName'],
                'SQFileHash': i['SQFileHash']
            }
            self.song_information.append(song)

    def File_normal_mp3(self, song_name, FileHash):
        # 该为下载酷狗音乐一般品质的方法，一般大小在10MB以下
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4041.0 Safari/537.36 Edg/81.0.410.1 chrome-extension',
            'referer': 'https://www.kugou.com/',
            'Cookie': 'kg_mid=b9549451fc08c8f895c4c7aa33bf1d78; kg_dfid=3Ljox00DuqF50gQvpw0MPFuK; '
                      'kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; '
                      'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1580798937,1580965509,1581226017,1581226439; '
                      'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1581254232 '
        }
        song_patch_url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(FileHash)
        res = self.session.get(song_patch_url, headers=headers)
        json = res.json()
        information = json['data']
        download_url = information['play_url']
        song_name = information['audio_name']
        res = requests.get(download_url, headers=self.headers,
                           stream=True)  # stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
        size = 0
        chunk_size = 4096 * 2  # 每次块大小为1024
        content_size = int(res.headers['content-length'])
        # 每次只获取一个chunk_size大小
        try:
            with open(self.position + '\\music_download\\' + song_name + '.mp3', 'wb') as file:
                for data in res.iter_content(chunk_size=chunk_size):  # 每次只获取一个chunk_size大小
                    file.write(data)  # 每次只写入data大小
                    size = len(data) + size
                    # 'r'每次重新从开始输出，end = ""是不换行
                    print('\r' + '正在下载：{}'.format(song_name) + "  已经下载：" + int(
                        size / content_size * 40) * "█" + " 【" + str(round(size / 1024 / 1024, 2)) + "MB】" + "【" + str(
                        round(float(size / content_size) * 100, 2)) + "%" + "】", end="")
        except:
            print('音乐自动命名失败！稍后交给用户为手动命名！')
            self.fail_name[song_name] = download_url
            print('歌曲名为：{}'.format(song_name))

    def File_HQ_mp3(self, song_name, FileHash):
        # 该为下载酷狗音乐HQ品质的方法，一般大小在10MB以上
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4041.0 Safari/537.36 Edg/81.0.410.1 chrome-extension',
            'referer': 'https://www.kugou.com/',
            'Cookie': self.cookies
        }
        song_patch_url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(FileHash)
        res = self.session.get(song_patch_url, headers=headers)
        json = res.json()
        information = json['data']
        download_url = information['play_url']
        song_name = information['audio_name']
        res = requests.get(download_url, headers=self.headers,
                           stream=True)  # stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
        size = 0
        chunk_size = 4096 * 2  # 每次块大小为1024
        content_size = int(res.headers['content-length'])
        # 每次只获取一个chunk_size大小
        with open(self.position + '\\music_download\\' + song_name + '.mp3', 'wb') as file:
            for data in res.iter_content(chunk_size=chunk_size):  # 每次只获取一个chunk_size大小
                file.write(data)  # 每次只写入data大小
                size = len(data) + size
                # 'r'每次重新从开始输出，end = ""是不换行
                print('\r' + '正在下载：{}'.format(song_name) + "  已经下载：" + int(size / content_size * 40) * "█" + " 【" + str(
                    round(size / 1024 / 1024, 2)) + "MB】" + "【" + str(
                    round(float(size / content_size) * 100, 2)) + "%" + "】", end="")

    def File_SQ_mp3(self, song_name, FileHash):
        # 该为下载酷狗音乐SQ品质的方法，一般大小在20MB以上
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4041.0 Safari/537.36 Edg/81.0.410.1 chrome-extension',
            'referer': 'https://www.kugou.com/',
            'Cookie': self.cookies
        }
        song_patch_url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(FileHash)
        res = self.session.get(song_patch_url, headers=headers)
        json = res.json()
        information = json['data']
        download_url = information['play_url']
        song_name = information['audio_name']
        res = requests.get(download_url, headers=self.headers,
                           stream=True)  # stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
        size = 0
        chunk_size = 4096 * 2  # 每次块大小为1024
        content_size = int(res.headers['content-length'])
        # 每次只获取一个chunk_size大小
        with open(self.position + '\\music_download\\' + song_name + '.flac', 'wb') as file:
            for data in res.iter_content(chunk_size=chunk_size):  # 每次只获取一个chunk_size大小
                file.write(data)  # 每次只写入data大小
                size = len(data) + size
                # 'r'每次重新从开始输出，end = ""是不换行
                print('\r' + '正在下载：{}'.format(song_name) + "  已经下载：" + int(size / content_size * 40) * "█" + " 【" + str(
                    round(size / 1024 / 1024, 2)) + "MB】" + "【" + str(
                    round(float(size / content_size) * 100, 2)) + "%" + "】", end="")
