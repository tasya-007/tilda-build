@echo off
setlocal
cd /d %~dp0
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
.venv\Scripts\pyinstaller --noconfirm TILDA.spec
echo Result: dist\TILDA.exe
pause