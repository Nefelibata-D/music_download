import os
import requests
from bs4 import BeautifulSoup
import zipfile
import time

print('=====================================')
print('尝试 下载 / 更新 chromedriver_win32驱动中…………')
position = os.getcwd()

print('查找目标文件夹和谷歌版本')
python_position = os.popen('where python').read().split('\n')[0].split('\\')[0:-1]
a = ''
times = 0
for i in python_position:
    if times == 0:
        a = a + i
        times += 1
    else:
        a = a + '\\' + i
Scripts = a + r'\Scripts'
chrome_position = "C:\\Program Files (x86)\\Google\\Chrome\\Application"
chrome_version = os.popen('cd {} && dir /a:d /o:n'.format(chrome_position)).read().split('<DIR>')[3].split('\n')[0]
version_first = chrome_version.split('.')[0][-2] + chrome_version.split('.')[0][-1] + '.' + chrome_version.split('.')[1]+ '.' + chrome_version.split('.')[2]

print('搜索谷歌版本对应的驱动')
chromedriver = {}
url = ''
res = requests.get('https://npm.taobao.org/mirrors/chromedriver')
soup = BeautifulSoup(res.text, 'html.parser')
link = soup.select('a')
for i in link:
    try:
        int(i.text.split('.')[0])
        int(i.text.split('.')[-1].split('/')[0])
        version = i.text
        url = 'https://npm.taobao.org' + i['href']
        if version[0:len(version_first)] == version_first:
            break
    except:
        continue

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
download_link = soup.select('pre a')[3]['href']
download_name = soup.select('pre a')[3].text

res = requests.get('https://npm.taobao.org' + download_link)
goal_position = position + '\\' + download_name
with open(goal_position, 'wb') as file:
    file.write(res.content)
    print('成功下载对应webdriver')

print('移动文件……')
zip_file = zipfile.ZipFile(goal_position)
zip_list = zip_file.namelist()  # 得到压缩包里所有文件

for f in zip_list:
    zip_file.extract(f, position)  # 循环解压文件到指定目录

zip_file.close()  # 关闭文件，必须有，释放内存

os.popen('move {} {}'.format('"' + position + '\\chromedriver.exe' + '"', Scripts))
time.sleep(1)
