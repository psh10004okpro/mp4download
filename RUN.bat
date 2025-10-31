@echo off
REM Ultra-simple launcher - No fancy output

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed!
    echo.
    echo Opening download page...
    start https://www.python.org/downloads/
    echo.
    echo Install Python and run this file again.
    pause
    exit /b 1
)

echo Checking packages...
pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo Installing packages...
    pip install customtkinter yt-dlp pillow
)

echo Starting program...
python video_downloader_gui.py

pause
