@echo off
REM EXE 파일 빌드 스크립트

echo ========================================
echo 동영상 다운로더 - EXE 빌드
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

REM PyInstaller 설치 확인
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller가 설치되어 있지 않습니다.
    echo PyInstaller를 설치합니다...
    pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo [오류] PyInstaller 설치에 실패했습니다.
        pause
        exit /b 1
    )
)

echo.
echo 필요한 패키지를 확인하는 중...
pip install -r requirements.txt

echo.
echo EXE 파일 빌드를 시작합니다...
echo 이 작업은 몇 분 정도 걸릴 수 있습니다.
echo.

REM PyInstaller로 빌드
pyinstaller --onefile --windowed --name "VideoDownloader" --clean video_downloader_gui.py

if errorlevel 1 (
    echo.
    echo [오류] 빌드에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 빌드 완료!
echo ========================================
echo.
echo 실행 파일 위치: dist\VideoDownloader.exe
echo.
echo 이 파일을 다른 Windows PC에서도 실행할 수 있습니다.
echo.
pause
