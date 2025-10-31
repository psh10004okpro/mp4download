@echo off
REM Simple Video Downloader Launcher
REM No Korean characters - Works on all Windows systems

title Video Downloader - Auto Install

cls
echo.
echo ====================================================================
echo.
echo              VIDEO DOWNLOADER - Auto Installer
echo.
echo          YouTube, Vimeo, and 1000+ sites supported
echo.
echo ====================================================================
echo.
echo.

REM Check Python
echo [Step 1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR: Python is not installed!
    echo ====================================================================
    echo.
    echo Python is required to run this program.
    echo.
    echo How to install Python:
    echo   1. Download page will open in 5 seconds
    echo   2. Click "Download Python" button
    echo   3. Run the downloaded file
    echo   4. CHECK "Add Python to PATH" (Important!)
    echo   5. Click "Install Now"
    echo   6. After installation, run this file again
    echo.
    echo Opening Python download page in 5 seconds...
    timeout /t 5 >nul
    start https://www.python.org/downloads/
    echo.
    echo Please install Python and run this file again.
    echo.
    pause
    exit /b 1
)

echo OK - Python is installed
python --version
echo.

REM Check and install packages
echo [Step 2/3] Checking packages...
pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required packages...
    echo This may take a few minutes...
    echo.
    pip install customtkinter yt-dlp pillow
    echo.
    echo OK - All packages installed!
) else (
    echo OK - All packages are ready
    pip install --upgrade yt-dlp --quiet >nul 2>&1
)
echo.

REM Run program
echo [Step 3/3] Starting program...
echo.
echo ====================================================================
echo GUI window will open soon...
echo ====================================================================
echo.
timeout /t 1 >nul

python video_downloader_gui.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR: Program failed to start
    echo ====================================================================
    echo.
    echo Common solutions:
    echo   1. Restart your computer
    echo   2. Reinstall Python (check "Add to PATH")
    echo   3. Run this file again
    echo.
)

echo.
echo Press any key to close...
pause >nul
