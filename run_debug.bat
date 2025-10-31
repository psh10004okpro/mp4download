@echo off
REM 동영상 다운로더 디버그 실행 스크립트
REM 이 파일은 에러를 확인하기 위해 창을 열어둡니다

echo ========================================
echo 동영상 다운로더 디버그 모드
echo ========================================
echo.

REM Python 설치 확인
echo [1/4] Python 설치 확인 중...
python --version
if errorlevel 1 (
    echo.
    echo ========================================
    echo [오류] Python이 설치되어 있지 않습니다!
    echo ========================================
    echo.
    echo Python 설치 방법:
    echo 1. https://www.python.org/downloads/ 접속
    echo 2. "Download Python 3.xx" 버튼 클릭
    echo 3. 다운로드한 파일 실행
    echo 4. "Add Python to PATH" 체크 (중요!)
    echo 5. "Install Now" 클릭
    echo.
    pause
    exit /b 1
)

echo Python 설치됨!
echo.

REM pip 확인
echo [2/4] pip 확인 중...
pip --version
if errorlevel 1 (
    echo.
    echo [오류] pip가 설치되어 있지 않습니다.
    pause
    exit /b 1
)
echo.

REM 필요한 패키지 확인
echo [3/4] 필요한 패키지 확인 중...
pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo customtkinter가 설치되지 않았습니다.
    echo 필요한 패키지를 설치합니다...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [오류] 패키지 설치에 실패했습니다.
        echo.
        echo 수동 설치를 시도하세요:
        echo pip install customtkinter yt-dlp pillow
        echo.
        pause
        exit /b 1
    )
) else (
    echo 필요한 패키지가 모두 설치되어 있습니다.
)
echo.

REM 프로그램 실행
echo [4/4] 프로그램 실행 중...
echo.
echo ========================================
echo GUI 창이 열립니다...
echo ========================================
echo.

python video_downloader_gui.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo [오류] 프로그램 실행 중 오류 발생!
    echo ========================================
    echo.
    echo 위의 에러 메시지를 확인해주세요.
    echo.
)

echo.
echo 프로그램이 종료되었습니다.
echo.
pause
