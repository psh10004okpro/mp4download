# 🎬 HLS 스트림 및 숨겨진 동영상 다운로드 가이드

## 📝 개요

많은 웹사이트들이 Blob URL이나 HLS/DASH 스트리밍을 사용하여 동영상을 제공합니다. 이 가이드는 이러한 "숨겨진" 동영상 URL을 찾아서 다운로드하는 방법을 설명합니다.

---

## 🤔 Blob URL이란?

### 특징
- **형식**: `blob:https://example.com/...`
- **용도**: 브라우저 내부에서만 사용되는 임시 메모리 주소
- **문제**: 실제 동영상 파일 위치가 아니므로 직접 다운로드 불가

### 해결 방법
Blob URL 대신 **실제 스트림 URL**을 찾아야 합니다!

---

## 🔍 실제 동영상 URL 찾는 방법

### 방법 1: Chrome/Edge 개발자 도구 사용 (추천) ⭐

#### 단계별 가이드

**1단계: 동영상 페이지 접속**
- 다운로드하려는 동영상이 있는 웹페이지를 엽니다

**2단계: 개발자 도구 열기**
- `F12` 키를 누릅니다
- 또는 우클릭 → "검사" 클릭
- 또는 `Ctrl + Shift + I` (Windows) / `Cmd + Option + I` (Mac)

**3단계: Network 탭 선택**
- 개발자 도구에서 "Network" (네트워크) 탭을 클릭합니다

**4단계: 필터 설정**
- 필터 드롭다운에서 **"Media"** 선택
- 또는 "All"을 선택한 후 검색창에 **"m3u8"** 입력

**5단계: 동영상 재생**
- 페이지를 새로고침 (`F5`)
- 또는 동영상 재생 버튼을 클릭

**6단계: 스트림 URL 찾기**

네트워크 목록에서 다음 중 하나를 찾습니다:

| 파일 확장자 | 설명 | 우선순위 |
|------------|------|---------|
| `.m3u8` | HLS 스트림 (가장 흔함) | ⭐⭐⭐ |
| `master.m3u8` | HLS 마스터 플레이리스트 | ⭐⭐⭐ |
| `playlist.m3u8` | HLS 플레이리스트 | ⭐⭐ |
| `.mpd` | DASH 스트림 | ⭐⭐ |
| `.mp4` | 직접 비디오 파일 | ⭐ |
| `.ts` | 비디오 세그먼트 | ⭐ |

**7단계: URL 복사**
- 해당 항목을 찾으면 우클릭
- "Copy" → **"Copy URL"** 선택
- 또는 해당 항목 클릭 → Headers 탭 → Request URL 복사

**8단계: 다운로드**
- 복사한 URL을 이 프로그램에 붙여넣기
- 자동으로 인식되어 "🎬 HLS/DASH 스트림 URL이 감지되었습니다!" 메시지 표시
- "동영상 검색하기" 버튼 클릭
- 다운로드!

---

### 방법 2: Firefox 개발자 도구 사용

#### 단계별 가이드

1. **동영상 페이지를 엽니다**

2. **개발자 도구 열기**
   - `F12` 키
   - 또는 `Ctrl + Shift + I`

3. **네트워크 탭 선택**
   - "네트워크" 탭 클릭

4. **필터 설정**
   - "Media" 선택
   - 또는 검색창에 "m3u8" 입력

5. **동영상 재생**
   - 페이지 새로고침 또는 동영상 재생

6. **URL 찾기**
   - `.m3u8`, `.mpd`, `.mp4` 파일 찾기

7. **URL 복사**
   - 우클릭 → "Copy Value" → "Copy URL"

8. **다운로드**
   - 이 프로그램에 붙여넣기

---

## 💡 꿀팁 & 트릭

### 검색 필터 활용

개발자 도구 네트워크 탭에서:

```
m3u8        ← HLS 스트림 찾기
mpd         ← DASH 스트림 찾기
master      ← 마스터 플레이리스트 찾기
video       ← 비디오 파일 찾기
```

### 파일 크기로 판단

- 작은 파일 (< 10KB): 플레이리스트 파일 (정답!)
- 큰 파일 (> 1MB): 비디오 세그먼트

### Type/Content-Type 확인

네트워크 항목의 Type 컬럼:

| Type | 의미 |
|------|------|
| `application/vnd.apple.mpegurl` | HLS 스트림 ✅ |
| `application/x-mpegURL` | HLS 스트림 ✅ |
| `application/dash+xml` | DASH 스트림 ✅ |
| `video/mp4` | MP4 파일 ✅ |
| `video/MP2T` | TS 세그먼트 |

### 여러 URL이 있을 때

1. **master.m3u8** 먼저 시도
2. 안 되면 **playlist.m3u8**
3. 그래도 안 되면 **index.m3u8**

---

## 🎬 지원하는 스트림 형식

### HLS (HTTP Live Streaming)

**확장자**: `.m3u8`, `.m3u`

**특징**:
- Apple이 개발한 프로토콜
- 가장 널리 사용됨
- iPhone, iPad 기본 지원

**예시**:
```
https://example.com/video/master.m3u8
https://example.com/playlist.m3u8
https://cdn.example.com/hls/stream.m3u8
```

### DASH (Dynamic Adaptive Streaming)

**확장자**: `.mpd`

**특징**:
- MPEG-DASH 표준
- YouTube 등에서 사용
- 적응형 비트레이트 스트리밍

**예시**:
```
https://example.com/video/manifest.mpd
https://example.com/dash/stream.mpd
```

### 직접 파일

**확장자**: `.mp4`, `.webm`, `.mkv`

**특징**:
- 스트리밍이 아닌 직접 파일
- 가장 다운로드하기 쉬움

**예시**:
```
https://example.com/videos/video.mp4
https://cdn.example.com/media/video.webm
```

---

## 🌐 사이트별 팁

### YouTube
- 이 프로그램에 YouTube URL 직접 입력 (자동 처리)
- 개발자 도구로 `.mpd` 찾을 필요 없음

### Vimeo
- YouTube와 동일하게 URL 직접 입력
- 또는 개발자 도구에서 `master.json` 찾기

### Facebook / Instagram
- 페이지 URL 직접 입력 시도
- 안 되면 개발자 도구에서 `.mp4` 찾기

### Twitch
- VOD URL 직접 입력
- 라이브는 `.m3u8` URL 찾기

### 기타 사이트
1. 페이지 URL 먼저 시도
2. 안 되면 개발자 도구 사용
3. `.m3u8` 또는 `.mpd` 찾기

---

## 🛠️ 고급 기법

### 1. URL 파라미터 확인

일부 스트림 URL에는 인증 토큰이 필요:

```
https://example.com/stream.m3u8?token=abc123&expires=1234567890
```

**중요**: 전체 URL을 복사해야 합니다 (파라미터 포함!)

### 2. Headers 확인

일부 사이트는 Referer 또는 User-Agent 체크:

- URL이 작동하지 않으면
- Headers 탭에서 추가 정보 확인
- (고급: curl 명령어로 다운로드 필요할 수 있음)

### 3. 플레이리스트 구조

HLS 구조 예시:

```
master.m3u8          ← 이것을 복사!
├─ 1080p.m3u8       ← 또는 이것
│  ├─ segment1.ts
│  ├─ segment2.ts
│  └─ segment3.ts
├─ 720p.m3u8
└─ 480p.m3u8
```

**팁**: `master.m3u8`를 복사하면 자동으로 최고 화질 선택

---

## ⚠️ 문제 해결

### "다운로드할 수 없습니다" 오류

**원인 1: DRM 보호**
- 해결: 다운로드 불가 (암호화되어 있음)

**원인 2: 인증 토큰 만료**
- 해결: URL을 다시 찾아서 복사

**원인 3: Geo-blocking (지역 제한)**
- 해결: VPN 사용 (합법적인 경우에만)

**원인 4: 잘못된 URL**
- 해결: `.ts` 세그먼트가 아닌 `.m3u8` 플레이리스트 복사

### "URL을 찾을 수 없습니다"

**해결 방법**:
1. 페이지를 새로고침하고 다시 시도
2. 동영상을 처음부터 재생
3. 캐시 삭제 후 재시도
4. 다른 브라우저에서 시도

### 다운로드가 매우 느림

**원인**: HLS는 작은 세그먼트로 구성됨

**해결**:
- 인내심을 가지고 기다림
- 네트워크 연결 확인
- 다른 시간대에 시도

---

## 📱 모바일에서 URL 찾기

### Android (Chrome)

1. **Kiwi Browser** 설치 (데스크톱 확장 지원)
2. Chrome DevTools 확장 프로그램 설치
3. 위의 Chrome 방법과 동일하게 진행

### iOS (Safari)

1. **Web Inspector** 활성화 (Mac 필요)
2. Mac에서 Safari → 개발 → [기기명] → [페이지]
3. 네트워크 탭에서 확인

**더 쉬운 방법**: PC에서 찾기!

---

## 🎓 실전 예제

### 예제 1: 간단한 HLS 스트림

**시나리오**: 강의 사이트의 동영상 다운로드

1. 강의 페이지 접속
2. F12 → Network → Media 필터
3. 동영상 재생
4. `lecture_01.m3u8` 찾음
5. 우클릭 → Copy URL
6. 프로그램에 붙여넣기
7. 다운로드! ✅

### 예제 2: 다중 화질 DASH 스트림

**시나리오**: 스포츠 스트리밍 사이트

1. 경기 페이지 접속
2. F12 → Network → "mpd" 검색
3. 경기 재생 시작
4. `manifest.mpd` 발견
5. URL 복사 (쿼리 파라미터 포함!)
6. 프로그램에 붙여넣기
7. 화질 선택
8. 다운로드! ✅

### 예제 3: Blob URL인 경우

**시나리오**: Blob URL만 보이는 사이트

1. F12 → Network → All 선택
2. 페이지 새로고침
3. "m3u8" 검색
4. `stream.m3u8` 발견 (Blob가 아닌 실제 URL!)
5. URL 복사
6. 프로그램에 붙여넣기
7. 다운로드! ✅

---

## ✅ 체크리스트

다운로드 전 확인사항:

- [ ] F12로 개발자 도구를 열었는가?
- [ ] Network 탭을 선택했는가?
- [ ] Media 필터 또는 "m3u8" 검색을 했는가?
- [ ] 동영상을 재생했는가?
- [ ] `.m3u8`, `.mpd`, 또는 `.mp4` 파일을 찾았는가?
- [ ] 전체 URL을 복사했는가? (파라미터 포함)
- [ ] 프로그램에 붙여넣었는가?
- [ ] "🎬 HLS/DASH 스트림 URL이 감지되었습니다!" 메시지가 나타났는가?

---

## 🔗 유용한 링크

- **yt-dlp 지원 사이트**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
- **HLS 프로토콜 설명**: https://developer.apple.com/streaming/
- **DASH 프로토콜 설명**: https://dashif.org/

---

## 📞 추가 도움

### 여전히 URL을 찾을 수 없나요?

1. **프로그램의 "❓ 도움말" 버튼** 클릭
2. 단계별 가이드를 다시 확인
3. 다른 브라우저에서 시도
4. 페이지 URL을 직접 입력해보기 (자동 감지될 수 있음)

### 다운로드가 실패하나요?

1. URL이 만료되지 않았는지 확인
2. 인터넷 연결 확인
3. yt-dlp 업데이트: `pip install --upgrade yt-dlp`
4. 다른 화질/포맷 시도

---

## 🎉 성공!

이제 어떤 동영상이든 다운로드할 수 있습니다!

**기억하세요**:
- Blob URL은 사용 불가 → 실제 `.m3u8` URL 찾기
- 개발자 도구 = 가장 강력한 도구
- `.m3u8` 파일을 찾으면 80% 성공!
- 이 프로그램이 자동으로 처리해드립니다!

**Happy Downloading! 🚀**
