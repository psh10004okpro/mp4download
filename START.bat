@echo off
REM Video Downloader - Smart Python Detection
REM Tries multiple methods to find Python

title Video Downloader

cls
echo.
echo ====================================================================
echo              VIDEO DOWNLOADER - Starting...
echo ====================================================================
echo.

REM Try method 1: python command
echo Checking Python installation...
python --version >nul 2>&1
if not errorlevel 1 (
    echo Found: Python command works
    set PYTHON_CMD=python
    goto :found_python
)

REM Try method 2: py launcher
py --version >nul 2>&1
if not errorlevel 1 (
    echo Found: Python Launcher (py) works
    set PYTHON_CMD=py
    goto :found_python
)

REM Try method 3: python3 command
python3 --version >nul 2>&1
if not errorlevel 1 (
    echo Found: Python3 command works
    set PYTHON_CMD=python3
    goto :found_python
)

REM Python not found
echo.
echo ====================================================================
echo Python is NOT detected
echo ====================================================================
echo.
echo Possible reasons:
echo   1. Python is not installed
echo   2. Python is installed but not in PATH
echo.
echo Let's check if Python is actually installed...
echo.

REM Check common Python installation paths
echo Checking common installation locations...
if exist "C:\Python*\python.exe" (
    echo Found Python in C:\Python*\ but PATH not configured!
    goto :path_issue
)
if exist "%LOCALAPPDATA%\Programs\Python\*\python.exe" (
    echo Found Python in AppData but PATH not configured!
    goto :path_issue
)

REM Really not installed
echo Python is not installed on this system.
echo Opening download page in 5 seconds...
timeout /t 5 >nul
start https://www.python.org/downloads/
echo.
echo IMPORTANT: When installing Python:
echo   - CHECK the box "Add Python to PATH"
echo   - This is the most important step!
echo.
pause
exit /b 1

:path_issue
echo.
echo ====================================================================
echo FOUND THE PROBLEM!
echo ====================================================================
echo.
echo Python IS installed, but Windows cannot find it.
echo This is a PATH configuration issue.
echo.
echo SOLUTION 1: Reinstall Python
echo   1. Uninstall current Python
echo   2. Download and install again
echo   3. CHECK "Add Python to PATH" during installation
echo.
echo SOLUTION 2: Use Python Launcher
echo   - Windows 10/11 includes "py" launcher
echo   - Open Microsoft Store and search "Python"
echo   - Install Python from Microsoft Store
echo.
echo Opening Python download page...
timeout /t 3 >nul
start https://www.python.org/downloads/
echo.
pause
exit /b 1

:found_python
echo Python is ready!
%PYTHON_CMD% --version
echo.

REM Check packages
echo Checking required packages...
%PYTHON_CMD% -m pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing packages... (this may take 2-3 minutes)
    %PYTHON_CMD% -m pip install customtkinter yt-dlp pillow
    if errorlevel 1 (
        echo.
        echo ERROR: Package installation failed!
        echo.
        echo Try running as Administrator:
        echo   - Right-click START.bat
        echo   - Select "Run as administrator"
        echo.
        pause
        exit /b 1
    )
    echo Packages installed successfully!
) else (
    echo Packages OK
    %PYTHON_CMD% -m pip install --upgrade yt-dlp --quiet >nul 2>&1
)
echo.

REM Run program
echo Starting GUI...
echo.
%PYTHON_CMD% video_downloader_gui.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo Program error occurred
    echo ====================================================================
    echo.
    echo Check the error message above.
    echo.
)

echo.
pause
