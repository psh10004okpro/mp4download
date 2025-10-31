@echo off
chcp 65001 >nul 2>&1
title 바탕화면 바로가기 만들기

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              바탕화면 바로가기 생성                             ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM 현재 폴더 경로
set "CURRENT_DIR=%~dp0"

REM 바탕화면 경로
set "DESKTOP=%USERPROFILE%\Desktop"

REM 바로가기 파일 경로
set "SHORTCUT=%DESKTOP%\동영상 다운로더.lnk"

echo  현재 폴더: %CURRENT_DIR%
echo  바탕화면: %DESKTOP%
echo.

REM PowerShell로 바로가기 생성
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%CURRENT_DIR%설치_및_실행.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.IconLocation = 'imageres.dll,181'; $Shortcut.Description = '동영상 다운로더 - 쉽고 빠른 다운로드'; $Shortcut.Save()"

if exist "%SHORTCUT%" (
    echo ✓ 바로가기 생성 완료!
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║           바탕화면에 "동영상 다운로더" 바로가기가             ║
    echo ║                  생성되었습니다!                               ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo  이제 바탕화면 바로가기를 더블클릭하면
    echo  바로 프로그램이 실행됩니다!
    echo.
) else (
    echo ✗ 바로가기 생성 실패
    echo.
    echo  수동으로 바로가기 만드는 방법:
    echo  1. "설치_및_실행.bat" 파일 우클릭
    echo  2. "바로 가기 만들기" 선택
    echo  3. 생성된 바로가기를 바탕화면으로 이동
    echo.
)

pause
