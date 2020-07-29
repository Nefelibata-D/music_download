# 音乐批量下载软件
## 本软件用于批量下载网易云音乐歌单内软件和酷狗音乐的单曲下载

### *使用说明：*
    1. 软件根目录下一共有三个.bat的文件
        1.1   run.bat : 直接运行软件的主程序
        1.2   pip install.bat : 用于安装软件依赖
        1.3   setup webdriver.bat : 由于软件的特殊性，需要使用chrome的webdriver完成爬虫任务
    
    2.在第一次使用前请先运行 ‘pip install.bat’(安装所需依赖) 和 ‘setup webdriver.bat’(安装控制浏览器的驱动)
        2.1  在使用pip install.bat时可能出现安装失败的情况，请推出重现安装直至成功为止。
        2.2  setup webdriver.bat会自动下载驱动，但不排除可能出错的可能，手动操作如下：
            *  查看chrome的版本： https://jingyan.baidu.com/article/bad08e1ed2d0d709c9512155.html
            *  下载对应的webdriver驱动 ：https://npm.taobao.org/mirrors/chromedriver/
               最终下载界面应该像 ：https://npm.taobao.org/mirrors/chromedriver/84.0.4147.30/
            *  解压 ， 复制chromedriver.exe 至 python的安装目录下的Scripts处
               python安装目录查看 ：cmd中输入 where python即可
        2.3  重新启动软件
    
    3.在软件中输入的任何密码均不会保存

### **注意事项**
    1. 软件中均采用chrome浏览器，其余浏览器也可以，有能力的大佬可以自行更改
    2. 请不要在pycharm中运行lib下的main.py ， 会出现无法输入密码的情况
    