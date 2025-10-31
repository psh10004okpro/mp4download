# 동영상 다운로더

웹사이트 URL을 입력하면 해당 페이지의 동영상을 검색하고 다운로드할 수 있는 프로그램입니다.

## 🎯 두 가지 버전 제공

### 1. Windows 데스크톱 프로그램 (추천) ⭐
- 사용하기 쉬운 GUI 인터페이스
- 설치 간편, 실행 파일(.exe) 제공
- 실시간 다운로드 진행률 표시
- **👉 [Windows 사용 가이드 보기](README_WINDOWS.md)**

### 2. 웹 애플리케이션
- 브라우저에서 실행
- 서버 형태로 배포 가능
- 아래 설명 참조

## 주요 기능

- 🔍 URL에서 동영상 자동 감지
- 📊 다양한 포맷 및 해상도 선택
- ⬇️ 원클릭 다운로드
- 🎨 반응형 UI 디자인
- 🚀 빠른 다운로드 속도

## 지원 사이트

yt-dlp를 사용하므로 다음 사이트들을 지원합니다:
- YouTube
- Vimeo
- Dailymotion
- Facebook
- Instagram
- Twitter
- 그 외 1000+ 사이트

## 빠른 시작

### Windows GUI 프로그램 (추천)

```bash
# 패키지 설치
pip install -r requirements.txt

# 프로그램 실행
python video_downloader_gui.py
```

또는 배치 파일 사용:
```bash
run.bat
```

상세한 사용법은 [Windows 가이드](README_WINDOWS.md)를 참조하세요.

### 웹 애플리케이션

```bash
# 패키지 설치
pip install -r requirements.txt

# 서버 실행
python app.py

# 브라우저에서 http://localhost:5000 접속
```

## 사용 방법

1. 웹 브라우저에서 애플리케이션을 엽니다
2. 다운로드하려는 동영상의 URL을 입력합니다
3. "검색" 버튼을 클릭합니다
4. 동영상 정보와 사용 가능한 포맷이 표시됩니다
5. 원하는 포맷의 "다운로드" 버튼을 클릭합니다
6. 다운로드가 완료되면 파일이 자동으로 저장됩니다

## 기술 스택

- **Backend**: Python Flask
- **Video Downloader**: yt-dlp
- **Frontend**: HTML5, CSS3, JavaScript
- **UI**: 그라데이션 디자인, 반응형 레이아웃

## 프로젝트 구조

```
mp4download/
├── video_downloader_gui.py    # Windows GUI 프로그램 (메인)
├── app.py                     # Flask 웹 서버
├── build_exe.py               # EXE 빌드 스크립트
├── run.bat                    # Windows 실행 스크립트
├── build.bat                  # Windows 빌드 스크립트
├── requirements.txt           # Python 의존성
├── README.md                  # 프로젝트 설명
├── README_WINDOWS.md          # Windows 상세 가이드
├── templates/
│   └── index.html            # 웹 인터페이스
└── downloads/                # 다운로드 폴더
```

## API 엔드포인트

### POST /api/video-info
동영상 정보를 가져옵니다.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

**Response:**
```json
{
  "title": "동영상 제목",
  "duration": 180,
  "thumbnail": "https://...",
  "uploader": "업로더 이름",
  "formats": [...]
}
```

### POST /api/download
동영상을 다운로드합니다.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "format_id": "best"
}
```

### GET /api/file/<filename>
다운로드된 파일을 전송합니다.

## 주의사항

- 저작권이 있는 콘텐츠는 개인적인 용도로만 사용하세요
- 일부 사이트는 다운로드를 제한할 수 있습니다
- 대용량 파일은 다운로드에 시간이 걸릴 수 있습니다

## 라이선스

MIT License
