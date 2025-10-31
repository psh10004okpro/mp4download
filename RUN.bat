@echo off
REM Simple launcher - tries multiple Python commands

REM Try python
python --version >nul 2>&1
if not errorlevel 1 (
    set PY=python
    goto :run
)

REM Try py launcher
py --version >nul 2>&1
if not errorlevel 1 (
    set PY=py
    goto :run
)

REM Try python3
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PY=python3
    goto :run
)

REM Not found
echo Python not found in PATH
echo.
echo Please run START.bat instead for automatic setup
echo Or install Python from: https://www.python.org/downloads/
echo.
pause
exit /b 1

:run
echo Using: %PY%
%PY% -m pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo Installing packages...
    %PY% -m pip install customtkinter yt-dlp pillow
)

echo Starting program...
%PY% video_downloader_gui.py
pause
