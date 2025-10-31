# EXE 파일 빌드 가이드

## 🎯 목표: VideoDownloader.exe 생성하기

Windows에서 실행 가능한 독립형 EXE 파일을 만드는 방법을 안내합니다.

---

## 방법 1: Windows PC에서 직접 빌드 (추천) ⭐

### 준비물
- Windows 10/11 PC
- Python 3.8 이상 설치됨
- 이 프로젝트 파일들

### 단계별 실행

#### ✅ 초간단 방법 (배치 파일 사용)

1. 프로젝트 폴더 열기
2. `build.bat` 파일 더블클릭
3. 완료! 🎉

생성 위치: `dist/VideoDownloader.exe`

#### 📝 상세 방법 (명령어 사용)

**1단계: 명령 프롬프트 열기**
- 프로젝트 폴더에서 Shift + 우클릭 → "여기서 PowerShell 창 열기"

**2단계: 필요한 패키지 설치**
```bash
pip install -r requirements.txt
```

**3단계: EXE 빌드**
```bash
python build_exe.py
```

또는 PyInstaller 직접 사용:
```bash
pyinstaller --onefile --windowed --name "VideoDownloader" --clean video_downloader_gui.py
```

**4단계: EXE 파일 확인**
```
dist/VideoDownloader.exe
```

이 파일을 다른 Windows PC로 복사해도 실행됩니다! (Python 설치 불필요)

---

## 방법 2: GitHub Actions 자동 빌드 🤖

Windows PC가 없거나 자동화를 원한다면 GitHub Actions를 사용하세요.

### 설정 방법

1. **이 프로젝트를 GitHub에 푸시**
   ```bash
   git push origin your-branch
   ```

2. **GitHub에서 Actions 탭 확인**
   - 자동으로 빌드가 시작됩니다
   - 완료되면 "Artifacts" 섹션에서 다운로드

3. **빌드된 EXE 다운로드**
   - GitHub → Actions → 완료된 워크플로우 선택
   - "VideoDownloader-Windows" 다운로드

### 릴리즈 생성하기

태그를 푸시하면 자동으로 릴리즈가 생성됩니다:

```bash
# 버전 태그 생성
git tag v1.0.0

# 태그 푸시
git push origin v1.0.0
```

그러면 GitHub Releases에 자동으로 EXE 파일이 업로드됩니다!

---

## 방법 3: 다른 서비스 사용

### A. PyInstaller Windows용 Docker

```bash
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows "pyinstaller --onefile --windowed video_downloader_gui.py"
```

### B. Wine (Linux에서 Windows 실행 파일 빌드)

**주의**: 복잡하고 안정성이 낮음. 권장하지 않음.

```bash
# Wine 설치 (Ubuntu/Debian)
sudo apt-get install wine wine64

# Windows Python 설치
# ... (복잡한 과정 생략)
```

---

## 빌드 옵션 설명

### 기본 옵션
```bash
pyinstaller --onefile --windowed video_downloader_gui.py
```

- `--onefile`: 단일 EXE 파일 생성
- `--windowed`: 콘솔 창 숨김 (GUI만 표시)

### 추가 옵션

#### 아이콘 추가
```bash
pyinstaller --onefile --windowed --icon=icon.ico video_downloader_gui.py
```

#### 이름 지정
```bash
pyinstaller --onefile --windowed --name "나만의동영상다운로더" video_downloader_gui.py
```

#### 관리자 권한 요구
```bash
pyinstaller --onefile --windowed --uac-admin video_downloader_gui.py
```

#### 파일 크기 줄이기 (UPX 압축)
```bash
pyinstaller --onefile --windowed --upx-dir=/path/to/upx video_downloader_gui.py
```

---

## 문제 해결

### ❌ "pyinstaller: command not found"

**해결책**:
```bash
pip install pyinstaller
```

### ❌ "ModuleNotFoundError"

**해결책**: 모든 의존성 설치
```bash
pip install -r requirements.txt
```

### ❌ EXE 실행 시 바이러스 경고

**원인**: PyInstaller로 만든 파일은 일부 백신에서 오탐지

**해결책**:
1. 코드를 직접 확인 후 백신 예외 추가
2. 또는 Python으로 직접 실행

### ❌ EXE 파일이 너무 큼 (100MB+)

**정상입니다**: PyInstaller는 Python 런타임과 모든 라이브러리를 포함합니다.

**크기 줄이기**:
```bash
# UPX로 압축
pyinstaller --onefile --windowed --upx-dir=C:\upx video_downloader_gui.py

# 또는 필요없는 모듈 제외
pyinstaller --onefile --windowed --exclude-module matplotlib video_downloader_gui.py
```

### ❌ Windows Defender가 삭제함

**해결책**:
1. Windows 보안 → 바이러스 및 위협 방지 → 제외 추가
2. EXE 파일 또는 폴더 추가

---

## 빌드 후 배포

### EXE 파일 테스트

1. **다른 폴더에 복사하여 테스트**
2. **깨끗한 Windows PC에서 테스트** (Python 없는 환경)
3. **바이러스 검사**: https://www.virustotal.com

### 사용자에게 배포

#### 옵션 1: 직접 배포
- EXE 파일만 배포
- 또는 ZIP으로 압축하여 배포

#### 옵션 2: 인스톨러 생성

**Inno Setup** 사용:
```pascal
[Setup]
AppName=동영상 다운로더
AppVersion=1.0
DefaultDirName={pf}\VideoDownloader
OutputDir=output
OutputBaseFilename=VideoDownloader-Setup

[Files]
Source: "dist\VideoDownloader.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\동영상 다운로더"; Filename: "{app}\VideoDownloader.exe"
```

#### 옵션 3: GitHub Releases
```bash
# 태그 생성 및 푸시
git tag v1.0.0
git push origin v1.0.0

# GitHub에서 자동으로 릴리즈 생성됨
```

---

## 자동화 스크립트

### 완전 자동화 (build_and_test.bat)

```batch
@echo off
echo ========================================
echo 동영상 다운로더 빌드 및 테스트
echo ========================================

REM 빌드
call build.bat

REM 테스트
echo.
echo EXE 파일 테스트 중...
start "" "dist\VideoDownloader.exe"

echo.
echo 빌드 완료!
echo 파일 위치: dist\VideoDownloader.exe
echo 파일 크기:
dir "dist\VideoDownloader.exe"
pause
```

---

## 참고 자료

- [PyInstaller 공식 문서](https://pyinstaller.org/)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [CustomTkinter 문서](https://github.com/TomSchimansky/CustomTkinter)

---

## 요약

### 가장 쉬운 방법
Windows PC에서 `build.bat` 더블클릭!

### 자동화 방법
GitHub에 푸시하면 자동으로 빌드됨!

### 결과
`dist/VideoDownloader.exe` - 어디서나 실행 가능한 독립형 실행 파일! 🎉
