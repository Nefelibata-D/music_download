@ECHO OFF
echo. 检查pip是否有更新
python -m pip install --upgrade pip

echo.
echo. ============================
echo. 安装需要的依赖库,请不要退出
pip install BeautifulSoup4
pip install selenium
pip install requests

pause