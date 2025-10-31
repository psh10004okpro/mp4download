# 🔍 실제 동영상 URL 찾는 방법

Chrome 확장 프로그램이 잘못된 URL(.shtml)을 감지할 때 실제 동영상 URL을 찾는 방법입니다.

## 📋 단계별 가이드

### 1단계: 개발자 도구 열기

1. 동영상 페이지에서 **F12** 키를 누르세요
2. 또는 우클릭 → **검사(Inspect)**

### 2단계: Network 탭 이동

1. 개발자 도구 상단의 **Network** 탭 클릭
2. **Media** 필터 클릭 (동영상/오디오 파일만 표시)
3. 또는 **XHR** 필터 클릭 (스트리밍 URL용)

### 3단계: 페이지 새로고침

1. **Ctrl + R** 또는 **F5**로 페이지 새로고침
2. 또는 Network 탭의 녹화 버튼이 빨간색인지 확인 (●)

### 4단계: 동영상 재생

1. 동영상 재생 버튼 클릭
2. Network 탭에서 파일들이 로드되는 것을 관찰

### 5단계: 동영상 파일 찾기

다음과 같은 파일을 찾으세요:

#### A. MP4 파일 (가장 쉬움)
- 파일명에 `.mp4` 포함
- Size가 몇 MB 이상 (보통 10MB+)
- Type이 `video/mp4`

#### B. M3U8 스트리밍 (HLS)
- 파일명에 `.m3u8` 포함
- Type이 `application/vnd.apple.mpegurl` 또는 `application/x-mpegURL`
- 예: `playlist.m3u8`, `index.m3u8`, `master.m3u8`

#### C. MPD 스트리밍 (DASH)
- 파일명에 `.mpd` 포함
- Type이 `application/dash+xml`

#### D. TS 세그먼트 파일
- 파일명에 `.ts` 포함
- 많은 작은 파일들 (각 2-10초)
- 이 경우 `.m3u8` 파일을 찾으세요

### 6단계: URL 확인

1. 찾은 파일을 **클릭**
2. 우측 패널에서 **Headers** 탭 확인
3. **Request URL** 복사:
   ```
   https://example.com/videos/video123.mp4
   또는
   https://example.com/stream/playlist.m3u8
   ```

### 7단계: URL 테스트

1. **새 탭 열기**
2. 복사한 URL 붙여넣기
3. 결과 확인:
   - ✅ **MP4**: 동영상이 재생됨 → 우클릭 "다른 이름으로 저장"
   - ✅ **M3U8/MPD**: 파일이 다운로드됨 → FFmpeg로 변환 필요

---

## 🎯 실전 예시

### 예시 1: MP4 파일

```
Network 탭에서 찾은 항목:
Name: video_720p.mp4
Size: 45.3 MB
Type: video/mp4
Request URL: https://cdn.example.com/videos/abc123/video_720p.mp4
```

**해결:**
1. URL을 새 탭에서 열기
2. 동영상 재생 확인
3. 우클릭 → "다른 이름으로 비디오 저장"

### 예시 2: M3U8 스트리밍

```
Network 탭에서 찾은 항목:
Name: master.m3u8
Size: 1.2 KB
Type: application/x-mpegURL
Request URL: https://stream.example.com/hls/video123/master.m3u8
```

**해결:**

**방법 A: Windows GUI 프로그램 사용 (권장!)**
```
1. video_downloader_gui.py 실행
2. URL 붙여넣기: https://stream.example.com/hls/video123/master.m3u8
3. 다운로드 클릭 → 자동으로 MP4로 변환됨
```

**방법 B: FFmpeg 직접 사용**
```bash
ffmpeg -i "https://stream.example.com/hls/video123/master.m3u8" -c copy output.mp4
```

### 예시 3: 여러 TS 파일

```
Network 탭에서 보이는 항목들:
segment0.ts
segment1.ts
segment2.ts
...
```

**해결:**
1. `.m3u8` 파일을 먼저 찾으세요 (위로 스크롤)
2. 없다면 Filter에서 **All** 선택 후 "m3u8" 검색
3. 찾은 .m3u8 URL 사용

---

## 🚫 주의사항

### .shtml 파일은 무시하세요!

```
❌ 잘못된 예:
Name: items1.shtml
Type: text/html
```

이것은 동영상 파일이 아닙니다! HTML 페이지입니다.

### Blob URL

```
⚠️ 문제가 있는 예:
blob:https://example.com/abc-123-def
```

**Blob URL은 임시 메모리 주소**입니다:
- 직접 다운로드 불가능
- Network 탭에서 실제 소스 찾아야 함
- Filter를 **All**로 변경하고 큰 파일 찾기

---

## 💡 팁

### Network 탭 정렬

1. **Size** 컬럼 클릭하여 크기 순 정렬
2. 가장 큰 파일이 보통 동영상입니다

### 필터 활용

```
Media  - MP4, WebM 등 직접 재생 가능한 파일
XHR    - M3U8, MPD 스트리밍 URL
All    - 모든 요청 (잘 안 찾아질 때)
```

### 검색 기능

1. Network 탭에서 **Ctrl + F**
2. 검색어 입력:
   - `mp4`
   - `m3u8`
   - `mpd`
   - `video`

---

## 🛠️ 문제 해결

### 동영상 파일이 안 보여요

**원인 1: 페이지를 새로고침하지 않음**
- 해결: F5로 새로고침 후 동영상 재생

**원인 2: Network 탭 녹화 중지됨**
- 해결: 빨간 점(●)이 켜져있는지 확인

**원인 3: 동영상을 재생하지 않음**
- 해결: 동영상 재생해야 URL 로드됨

### URL을 복사했는데 작동 안 해요

**원인 1: 시간 제한 토큰**
- 일부 URL은 몇 분 후 만료됨
- 해결: 빠르게 다운로드하거나 Windows GUI 프로그램 사용

**원인 2: Referer 제한**
- 직접 접근 차단됨
- 해결: Windows GUI 프로그램 사용 (자동으로 Referer 설정)

---

## ✅ 성공 체크리스트

- [ ] F12로 개발자 도구 열기
- [ ] Network → Media 탭 선택
- [ ] 페이지 새로고침
- [ ] 동영상 재생
- [ ] .mp4 또는 .m3u8 파일 찾기
- [ ] Request URL 복사
- [ ] 새 탭에서 URL 테스트
- [ ] 다운로드 성공!

---

## 🎓 추가 학습

- [HLS 스트림 가이드](../HLS_스트림_가이드.md) - M3U8 파일 상세 설명
- [Referer 우회 가이드](../Referer_우회_가이드.md) - 제한된 사이트 다운로드
- [Windows GUI 가이드](../README_WINDOWS.md) - 자동화된 다운로드

---

**행운을 빕니다!** 🎥✨

실제 동영상 URL을 찾으면 Chrome 확장 프로그램이나 Windows GUI 프로그램으로
성공적으로 다운로드할 수 있습니다.
