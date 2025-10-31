"""
Windows 실행 파일(.exe) 빌드 스크립트

사용법:
    python build_exe.py

또는 직접 PyInstaller 명령어 사용:
    pyinstaller --onefile --windowed --name "VideoDownloader" --icon=icon.ico video_downloader_gui.py
"""

import os
import subprocess
import sys


def build_exe():
    """PyInstaller를 사용하여 exe 파일 생성"""

    print("=" * 60)
    print("동영상 다운로더 - Windows 실행 파일 빌드")
    print("=" * 60)
    print()

    # PyInstaller 명령어 구성
    command = [
        "pyinstaller",
        "--onefile",  # 단일 실행 파일로 생성
        "--windowed",  # 콘솔 창 숨기기 (GUI 모드)
        "--name", "VideoDownloader",  # 실행 파일 이름
        "--clean",  # 이전 빌드 정리
        # 필요한 데이터 파일 포함 (있는 경우)
        # "--add-data", "icon.png;.",
    ]

    # 아이콘 파일이 있으면 포함
    if os.path.exists("icon.ico"):
        command.extend(["--icon", "icon.ico"])

    command.append("video_downloader_gui.py")

    print(f"실행 명령어: {' '.join(command)}")
    print()
    print("빌드를 시작합니다...")
    print()

    try:
        # PyInstaller 실행
        result = subprocess.run(command, check=True)

        print()
        print("=" * 60)
        print("✅ 빌드 완료!")
        print("=" * 60)
        print()
        print(f"실행 파일 위치: dist/VideoDownloader.exe")
        print()
        print("참고:")
        print("  - dist 폴더에서 VideoDownloader.exe를 찾을 수 있습니다")
        print("  - 이 파일을 다른 Windows PC에서도 실행할 수 있습니다")
        print("  - 바이러스 백신이 경고할 수 있으나 정상입니다")
        print()

    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("❌ 빌드 실패!")
        print("=" * 60)
        print()
        print(f"오류: {e}")
        print()
        print("해결 방법:")
        print("  1. PyInstaller가 설치되어 있는지 확인: pip install pyinstaller")
        print("  2. requirements.txt의 모든 패키지가 설치되어 있는지 확인")
        print()
        sys.exit(1)

    except FileNotFoundError:
        print()
        print("=" * 60)
        print("❌ PyInstaller를 찾을 수 없습니다!")
        print("=" * 60)
        print()
        print("PyInstaller를 설치해주세요:")
        print("  pip install pyinstaller")
        print()
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
