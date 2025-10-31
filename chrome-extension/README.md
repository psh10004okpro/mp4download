# 🎥 Video Downloader Pro - Chrome 확장 프로그램

IDM(Internet Download Manager)처럼 동영상을 쉽게 다운로드할 수 있는 Chrome 확장 프로그램입니다!

## ✨ 주요 기능

### 🔍 자동 동영상 감지
- 웹페이지의 모든 HTML5 동영상 자동 감지
- HLS(.m3u8) 및 DASH(.mpd) 스트리밍 URL 자동 감지
- Blob URL로 재생되는 동영상도 감지
- 동적으로 추가되는 동영상도 실시간 감지

### 📥 원클릭 다운로드
- 동영상 위에 마우스를 올리면 다운로드 버튼 표시
- 버튼 클릭 한 번으로 즉시 다운로드
- 우클릭 메뉴에서도 다운로드 가능
- 확장 프로그램 팝업에서 모든 동영상 목록 확인

### 🔒 Referer 우회
- 사이트 내부 접근만 허용하는 동영상도 다운로드 가능
- 자동으로 Referer 및 User-Agent 헤더 설정
- 핫링크 보호 우회

### 📊 실시간 모니터링
- 확장 프로그램 아이콘에 감지된 동영상 수 표시
- 다운로드 진행률 알림
- 다운로드 성공/실패 알림

## 📥 설치 방법

### 방법 1: Chrome 웹 스토어에서 설치 (출시 후)
1. [Chrome 웹 스토어 링크] 접속
2. "Chrome에 추가" 버튼 클릭
3. 권한 확인 후 "확장 프로그램 추가" 클릭

### 방법 2: 개발자 모드로 설치 (현재)

1. **이 저장소 다운로드**
   ```bash
   git clone https://github.com/your-repo/mp4download.git
   cd mp4download/chrome-extension
   ```

2. **Chrome 확장 프로그램 페이지 열기**
   - Chrome 주소창에 `chrome://extensions/` 입력
   - 또는 메뉴 → 도구 더보기 → 확장 프로그램

3. **개발자 모드 활성화**
   - 우측 상단의 "개발자 모드" 토글 켜기

4. **압축해제된 확장 프로그램 로드**
   - "압축해제된 확장 프로그램을 로드합니다" 클릭
   - `chrome-extension` 폴더 선택

5. **설치 완료!**
   - 브라우저 툴바에 Video Downloader Pro 아이콘이 나타납니다

## 🚀 사용 방법

### 기본 사용법

1. **동영상이 있는 웹페이지 접속**
   - YouTube, Vimeo, 일반 사이트 등 어디든 가능

2. **동영상 감지 확인**
   - 확장 프로그램 아이콘에 숫자 배지가 표시됨
   - 예: 🎥(2) - 2개의 동영상 감지됨

3. **다운로드 방법 선택**

   **방법 A: 동영상 위 버튼 클릭**
   - 동영상에 마우스를 올리면 보라색 다운로드 버튼 표시
   - 버튼 클릭하면 즉시 다운로드 시작

   **방법 B: 우클릭 메뉴**
   - 동영상에서 우클릭
   - "동영상 다운로드" 선택

   **방법 C: 팝업에서 선택**
   - 확장 프로그램 아이콘 클릭
   - 감지된 동영상 목록에서 원하는 동영상 클릭

4. **다운로드 진행**
   - Chrome 다운로드 창에서 진행률 확인
   - 완료 알림 표시

### 고급 사용법

#### HLS/DASH 스트리밍 다운로드

일부 사이트는 HLS(.m3u8) 또는 DASH(.mpd) 형식을 사용합니다:

1. **자동 감지**
   - 확장 프로그램이 자동으로 .m3u8, .mpd URL 감지
   - 팝업에 스트리밍 URL 표시

2. **다운로드**
   - URL 클릭하면 .m3u8 또는 .mpd 파일 다운로드
   - 이 파일을 FFmpeg 등으로 변환 필요:
   ```bash
   ffmpeg -i playlist.m3u8 -c copy output.mp4
   ```

#### Blob URL 처리

Blob URL은 직접 다운로드가 불가능합니다:

1. **Blob URL 감지 시**
   - "⚠️ Blob URL 감지" 알림 표시
   - 실제 URL을 찾아야 함

2. **실제 URL 찾기**
   - F12 → Network 탭 열기
   - "Media" 또는 "XHR" 필터 선택
   - 동영상 재생 중 .m3u8 또는 .mp4 파일 찾기
   - 해당 URL 우클릭 → "Open in new tab"
   - URL 복사하여 사용

## 📂 파일 구조

```
chrome-extension/
├── manifest.json          # 확장 프로그램 설정
├── content.js            # 동영상 감지 및 버튼 주입
├── background.js         # 다운로드 관리
├── popup.html           # 팝업 UI
├── popup.js             # 팝업 기능
├── styles.css           # 스타일
├── icons/               # 아이콘 파일
│   ├── icon16.png
│   ├── icon48.png
│   ├── icon128.png
│   └── icon.svg         # 소스 SVG
└── README.md           # 이 파일
```

## ⚙️ 권한 설명

확장 프로그램이 요청하는 권한과 이유:

| 권한 | 이유 |
|------|------|
| `downloads` | 동영상 파일 다운로드 |
| `storage` | 감지된 동영상 목록 저장 |
| `tabs` | 현재 탭의 URL 및 제목 가져오기 |
| `webRequest` | 네트워크 요청 모니터링 (.m3u8, .mpd 감지) |
| `contextMenus` | 우클릭 메뉴에 다운로드 옵션 추가 |
| `<all_urls>` | 모든 웹사이트에서 동영상 감지 |

**개인정보 보호**: 이 확장 프로그램은 어떠한 데이터도 외부로 전송하지 않습니다. 모든 처리는 로컬에서 이루어집니다.

## 🎯 지원 사이트

### 완벽 지원
- ✅ YouTube
- ✅ Vimeo
- ✅ Dailymotion
- ✅ Facebook
- ✅ Twitter
- ✅ Instagram
- ✅ HTML5 동영상을 사용하는 모든 사이트

### 부분 지원 (HLS/DASH)
- ⚠️ Twitch (m3u8 URL 제공, FFmpeg 변환 필요)
- ⚠️ 일부 스트리밍 사이트

### 지원 불가
- ❌ Netflix, Disney+ 등 DRM 보호 콘텐츠
- ❌ Flash 기반 동영상 (이미 대부분 지원 종료)

## 🔧 문제 해결

### 동영상이 감지되지 않아요

**확인 사항:**
1. 페이지를 완전히 로드했나요?
2. 동영상을 재생해보세요 (일부 동영상은 재생해야 감지됨)
3. F12 → Console에서 오류 메시지 확인
4. 페이지 새로고침 후 다시 시도

### 다운로드 버튼이 보이지 않아요

**해결 방법:**
1. 확장 프로그램이 활성화되어 있는지 확인
2. 동영상에 직접 마우스를 올려보세요
3. 팝업을 열어 목록에서 다운로드 시도
4. 우클릭 메뉴 사용

### 다운로드가 실패해요

**가능한 원인:**
1. **Referer 제한**: 일부 사이트는 외부 다운로드 차단
   - 이 확장 프로그램은 자동으로 Referer 설정함
   - 그래도 실패하면 사이트 정책상 차단된 것

2. **로그인 필요**: 로그인해야 다운로드 가능한 동영상
   - Chrome에서 해당 사이트에 로그인 후 다시 시도

3. **DRM 보호**: 저작권 보호된 콘텐츠
   - 다운로드 불가능 (Netflix, Disney+ 등)

### Blob URL이에요

Blob URL은 임시 메모리 주소로 다운로드 불가:

1. **F12 → Network 탭** 열기
2. **Media** 필터 선택
3. 동영상 재생하며 **.m3u8** 또는 **.mp4** 파일 찾기
4. 해당 URL 사용

상세 가이드: [HLS_스트림_가이드.md](../HLS_스트림_가이드.md)

## 🛠️ 개발자 정보

### 로컬 개발

```bash
# 저장소 클론
git clone https://github.com/your-repo/mp4download.git
cd mp4download/chrome-extension

# 파일 수정 후
# Chrome에서 확장 프로그램 새로고침 (chrome://extensions/)
```

### 디버깅

1. **Content Script 디버깅**
   - 웹페이지에서 F12
   - Console에서 로그 확인

2. **Background Script 디버깅**
   - chrome://extensions/
   - Video Downloader Pro → "서비스 워커" 클릭
   - DevTools 열림

3. **Popup 디버깅**
   - 팝업 열기
   - 팝업에서 우클릭 → 검사

### 기여하기

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## ⚠️ 법적 고지

- 이 확장 프로그램은 개인적인 용도로만 사용하세요
- 저작권이 있는 콘텐츠는 무단 배포하지 마세요
- 다운로드한 콘텐츠의 사용은 사용자 책임입니다
- 일부 사이트의 이용약관에서 다운로드를 금지할 수 있습니다

## 🔗 관련 링크

- [Windows GUI 버전](../README_WINDOWS.md)
- [HLS 스트림 가이드](../HLS_스트림_가이드.md)
- [Referer 우회 가이드](../Referer_우회_가이드.md)
- [빌드 가이드](../BUILD_GUIDE.md)

## 📞 지원

문제가 있거나 제안사항이 있으시면:
- [Issues](https://github.com/your-repo/mp4download/issues) 등록
- [Discussions](https://github.com/your-repo/mp4download/discussions) 참여

## 🎉 감사합니다!

Video Downloader Pro를 사용해주셔서 감사합니다!
별표⭐를 눌러주시면 개발에 큰 힘이 됩니다.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-31
