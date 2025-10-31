@echo off
REM 이 창은 자동으로 닫히지 않습니다!
REM 모든 메시지를 확인할 수 있습니다.

title 동영상 다운로더 GUI 시작

echo.
echo ========================================
echo    동영상 다운로더 GUI 프로그램
echo ========================================
echo.
echo 이 창은 닫히지 않으므로 에러를 확인할 수 있습니다.
echo.
echo ----------------------------------------
echo.

REM Python 확인
echo [단계 1/4] Python 설치 확인...
python --version
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Python이 설치되어 있지 않습니다!
    echo ========================================
    echo.
    echo Python을 먼저 설치해야 합니다:
    echo.
    echo 1. https://www.python.org/downloads/ 접속
    echo 2. "Download Python 3.xx" 버튼 클릭
    echo 3. 다운로드한 파일 실행
    echo 4. 설치 시 "Add Python to PATH" 반드시 체크!
    echo 5. "Install Now" 클릭
    echo 6. 설치 완료 후 컴퓨터 재시작
    echo 7. 이 프로그램 다시 실행
    echo.
    echo ========================================
    echo 아무 키나 누르면 이 창이 닫힙니다.
    pause
    exit /b 1
)

echo    OK - Python 설치됨!
echo.

REM pip 확인
echo [단계 2/4] pip 확인...
pip --version >nul 2>&1
if errorlevel 1 (
    echo    ERROR - pip가 설치되지 않았습니다!
    echo    Python을 재설치하세요.
    echo.
    pause
    exit /b 1
)
echo    OK - pip 사용 가능!
echo.

REM 패키지 설치
echo [단계 3/4] 필요한 패키지 확인...
pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo    customtkinter가 없습니다. 설치 중...
    echo.
    pip install customtkinter yt-dlp pillow
    echo.
    if errorlevel 1 (
        echo    ERROR - 패키지 설치 실패!
        echo.
        echo    인터넷 연결을 확인하고 다시 시도하거나
        echo    관리자 권한으로 실행해보세요.
        echo.
        pause
        exit /b 1
    )
    echo    OK - 패키지 설치 완료!
) else (
    echo    OK - 모든 패키지 설치됨!
)
echo.

REM 프로그램 실행
echo [단계 4/4] GUI 프로그램 시작...
echo.
echo ========================================
echo GUI 창이 곧 열립니다...
echo (GUI 창을 닫으면 이 창도 닫힙니다)
echo ========================================
echo.

python video_downloader_gui.py

REM 프로그램 종료 후
echo.
echo.
if errorlevel 1 (
    echo ========================================
    echo ERROR: 프로그램 실행 중 오류 발생!
    echo ========================================
    echo.
    echo 위의 에러 메시지를 확인하세요.
    echo.
    echo 일반적인 원인:
    echo - video_downloader_gui.py 파일이 없음
    echo - Python 패키지 누락
    echo - 파일 권한 문제
    echo.
) else (
    echo ========================================
    echo 프로그램이 정상 종료되었습니다.
    echo ========================================
)

echo.
echo 아무 키나 누르면 창이 닫힙니다.
pause
