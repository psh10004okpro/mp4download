@echo off
REM 동영상 다운로더 실행 스크립트

echo ========================================
echo 동영상 다운로더 시작
echo ========================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python을 설치해주세요: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python이 설치되어 있습니다.
echo.

REM 필요한 패키지 설치 여부 확인
echo 필요한 패키지를 확인하는 중...
pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo.
    echo 필요한 패키지를 설치합니다...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [오류] 패키지 설치에 실패했습니다.
        pause
        exit /b 1
    )
)

echo.
echo 프로그램을 실행합니다...
echo.

REM GUI 프로그램 실행
python video_downloader_gui.py

if errorlevel 1 (
    echo.
    echo [오류] 프로그램 실행 중 오류가 발생했습니다.
    pause
    exit /b 1
)

echo.
echo 프로그램이 종료되었습니다.
pause
