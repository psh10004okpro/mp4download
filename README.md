# 동영상 다운로더

웹사이트 URL을 입력하면 해당 페이지의 동영상을 검색하고 다운로드할 수 있는 웹 애플리케이션입니다.

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

## 설치 방법

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
python app.py
```

### 3. 브라우저에서 접속

```
http://localhost:5000
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
├── app.py                 # Flask 애플리케이션
├── requirements.txt       # Python 의존성
├── templates/
│   └── index.html        # 메인 웹 페이지
├── static/               # 정적 파일 (필요시)
└── downloads/            # 다운로드된 파일 저장 폴더
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
