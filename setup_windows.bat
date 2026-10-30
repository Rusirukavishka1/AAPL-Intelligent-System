@echo off
cd /d "%~dp0"
py -3.11 -c "import sys" >nul 2>&1
if not errorlevel 1 (
 py -3.11 -m venv .venv
 goto install
)
py -3.12 -c "import sys" >nul 2>&1
if not errorlevel 1 (
 py -3.12 -m venv .venv
 goto install
)
python -c "import sys; assert sys.version_info[:2] in [(3,11),(3,12)]" >nul 2>&1
if not errorlevel 1 (
 python -m venv .venv
 goto install
)
echo Python 3.11 or 3.12 was not found.
echo If you use Anaconda, open Anaconda Prompt in this folder and run:
echo conda create -n aapl_dashboard python=3.11 -y
echo conda activate aapl_dashboard
echo python -m pip install -r requirements.txt
echo python -m streamlit run app.py
pause
exit /b 1
:install
if not exist .venv\Scripts\python.exe goto fail
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fail
echo Setup complete. Double-click run_windows.bat.
pause
exit /b 0
:fail
echo Setup failed. Review the error above.
pause
exit /b 1
