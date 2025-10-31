# 동영상 다운로더 - Windows 프로그램

웹사이트 URL을 입력하면 동영상을 검색하고 다운로드할 수 있는 Windows 데스크톱 애플리케이션입니다.

![Windows Application](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-orange)

## 주요 기능

- 🎯 **직관적인 GUI** - 사용하기 쉬운 현대적인 인터페이스
- 🔍 **자동 검색** - URL만 입력하면 동영상 자동 감지
- 📊 **포맷 선택** - 다양한 해상도와 포맷 중 선택 가능
- 📈 **실시간 진행률** - 다운로드 진행 상황 실시간 표시
- 💾 **저장 위치 선택** - 원하는 폴더에 다운로드
- 🌐 **1000+ 사이트 지원** - YouTube, Vimeo, Facebook 등

## 지원 사이트

yt-dlp를 사용하므로 다음 사이트들을 지원합니다:

- ✅ YouTube
- ✅ Vimeo
- ✅ Dailymotion
- ✅ Facebook
- ✅ Instagram
- ✅ Twitter / X
- ✅ TikTok
- ✅ Twitch
- ✅ 그 외 1000개 이상의 동영상 사이트

전체 지원 사이트 목록: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## 설치 및 실행 방법

### 방법 1: Python으로 실행 (개발자용)

#### 1단계: Python 설치
- Python 3.8 이상 필요
- https://www.python.org/downloads/ 에서 다운로드

#### 2단계: 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

#### 3단계: 프로그램 실행
```bash
python video_downloader_gui.py
```

### 방법 2: EXE 파일로 빌드 (배포용)

#### 1단계: 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

#### 2단계: EXE 파일 생성
```bash
python build_exe.py
```

또는 직접 PyInstaller 사용:
```bash
pyinstaller --onefile --windowed --name "VideoDownloader" video_downloader_gui.py
```

#### 3단계: 실행
```
dist/VideoDownloader.exe
```

생성된 `VideoDownloader.exe` 파일은 다른 Windows PC에서도 Python 설치 없이 실행 가능합니다.

## 사용 방법

### 기본 사용법

1. **프로그램 실행**
   - `video_downloader_gui.py`를 실행하거나 `VideoDownloader.exe`를 실행합니다

2. **URL 입력**
   - 다운로드하려는 동영상의 URL을 입력란에 붙여넣습니다
   - 예: `https://www.youtube.com/watch?v=...`

3. **검색**
   - "🔍 검색" 버튼을 클릭하거나 Enter 키를 누릅니다
   - 동영상 정보와 사용 가능한 포맷이 표시됩니다

4. **저장 위치 선택** (선택사항)
   - "📁 저장 위치" 버튼을 클릭하여 다운로드 폴더를 변경할 수 있습니다
   - 기본값: Windows 다운로드 폴더

5. **포맷 선택 및 다운로드**
   - 원하는 화질/포맷의 "다운로드" 버튼을 클릭합니다
   - "🌟 최고 품질" 옵션을 선택하면 최상의 품질로 다운로드됩니다

6. **다운로드 진행**
   - 하단의 진행률 바에서 다운로드 상태를 확인할 수 있습니다
   - 완료되면 알림 메시지가 표시됩니다

### 팁

- **빠른 검색**: URL 입력 후 Enter 키를 누르면 바로 검색됩니다
- **최고 품질**: 화질에 민감한 경우 "최고 품질" 옵션을 선택하세요
- **용량 절약**: 파일 크기를 줄이려면 낮은 해상도를 선택하세요
- **다운로드 폴더**: 자주 사용하는 폴더를 선택해두면 편리합니다

## 프로젝트 구조

```
mp4download/
├── video_downloader_gui.py    # Windows GUI 애플리케이션 (메인)
├── app.py                     # Flask 웹 서버 (선택사항)
├── build_exe.py              # EXE 빌드 스크립트
├── requirements.txt          # Python 의존성
├── templates/
│   └── index.html           # 웹 인터페이스
└── README_WINDOWS.md        # Windows 사용 설명서
```

## 기술 스택

- **언어**: Python 3.8+
- **GUI 프레임워크**: CustomTkinter
- **다운로더**: yt-dlp
- **빌드 도구**: PyInstaller

## 문제 해결

### 프로그램이 실행되지 않아요

1. Python이 올바르게 설치되어 있는지 확인:
   ```bash
   python --version
   ```

2. 필요한 패키지가 설치되어 있는지 확인:
   ```bash
   pip install -r requirements.txt
   ```

3. 오류 메시지를 확인하고 누락된 패키지를 설치하세요

### 다운로드가 안 돼요

1. **인터넷 연결 확인**: 인터넷에 연결되어 있는지 확인하세요

2. **URL 확인**: 올바른 동영상 URL인지 확인하세요

3. **사이트 지원 확인**: 해당 사이트가 지원되는지 확인하세요
   - 지원 사이트 목록: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

4. **yt-dlp 업데이트**: 최신 버전으로 업데이트하세요
   ```bash
   pip install --upgrade yt-dlp
   ```

### 바이러스 백신이 경고해요

- PyInstaller로 만든 exe 파일은 일부 백신 프로그램에서 오탐지될 수 있습니다
- 이는 정상적인 현상이며, 소스 코드를 직접 확인하고 Python으로 실행하거나
- 백신 프로그램의 예외 목록에 추가하실 수 있습니다

### EXE 파일 크기가 너무 커요

- PyInstaller는 필요한 모든 라이브러리를 포함하므로 파일이 클 수 있습니다
- 일반적으로 50-100MB 정도의 크기가 정상입니다
- UPX를 사용하여 압축할 수 있습니다:
  ```bash
  pyinstaller --onefile --windowed --upx-dir=/path/to/upx video_downloader_gui.py
  ```

## 주의사항

⚠️ **중요**: 이 프로그램은 개인적인 용도로만 사용하세요

- 저작권이 있는 콘텐츠는 저작권자의 허가 없이 다운로드하지 마세요
- 상업적 목적으로 사용하지 마세요
- 일부 사이트는 다운로드를 제한할 수 있습니다
- 대용량 파일은 다운로드에 시간이 걸릴 수 있습니다

## 업데이트

프로그램을 최신 버전으로 유지하세요:

```bash
# yt-dlp 업데이트
pip install --upgrade yt-dlp

# 모든 패키지 업데이트
pip install --upgrade -r requirements.txt
```

## 라이선스

MIT License

## 기여

버그 리포트나 기능 제안은 GitHub Issues를 통해 제출해주세요.

## 감사의 말

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 강력한 비디오 다운로더
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - 현대적인 GUI 프레임워크
