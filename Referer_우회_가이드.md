# 🔒 Referer 제한 사이트 다운로드 가이드

## 📝 개요

많은 동영상 사이트들이 외부에서 직접 동영상 파일에 접근하는 것을 막기 위해 **Referer 검증**을 사용합니다. 이 프로그램은 자동으로 이를 우회하여 다운로드할 수 있게 합니다.

---

## 🤔 Referer 제한이란?

### 작동 원리

```
일반 다운로드:
┌──────────┐     요청      ┌──────────┐
│ 다운로더  │ ─────────────>│  서버    │
└──────────┘              └──────────┘
                            ❌ 거부!
                            (Referer가 없음)

프로그램 다운로드:
┌──────────┐   Referer:     ┌──────────┐
│ 다운로더  │   example.com  │  서버    │
└──────────┘ ─────────────>└──────────┘
                            ✅ 허용!
                            (사이트 내부 접근으로 인식)
```

### 왜 사용하나?

1. **핫링크 방지** - 다른 사이트에서 직접 링크하는 것 방지
2. **대역폭 보호** - 무단 다운로드로 인한 트래픽 비용 절감
3. **저작권 보호** - 쉬운 다운로드 차단

---

## ✨ 프로그램의 자동 우회 기능

### 자동으로 처리되는 것들

이 프로그램은 다운로드 시 자동으로 다음을 설정합니다:

#### 1. **Referer 헤더**
```
입력 URL: https://example.com/video/12345.m3u8

자동 설정:
Referer: https://example.com/
Origin: https://example.com
```

#### 2. **User-Agent**
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
            AppleWebKit/537.36 (KHTML, like Gecko)
            Chrome/120.0.0.0 Safari/537.36
```

최신 Chrome 브라우저로 위장하여 정상적인 브라우저 접근으로 인식되게 합니다.

#### 3. **기타 헤더**
```
Accept: text/html,application/xhtml+xml,application/xml;...
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
DNT: 1
```

실제 브라우저와 동일한 헤더를 전송하여 감지를 피합니다.

---

## 🎯 사용 방법

### 기본 사용 (자동 처리)

**일반 동영상 URL:**
```
1. URL 복사: https://example.com/video/movie.mp4
2. 프로그램에 붙여넣기
3. 다운로드 클릭
4. 자동으로 Referer 설정됨!
5. 다운로드 성공 ✅
```

**HLS 스트림 URL:**
```
1. .m3u8 URL 복사: https://example.com/stream/video.m3u8
2. 프로그램에 붙여넣기
3. "🎬 HLS 스트림 감지!" 메시지
4. 다운로드 클릭
5. Referer 자동 설정 + 다운로드 성공 ✅
```

**아무것도 추가로 할 필요 없음! 프로그램이 모두 자동 처리합니다.**

---

## 🛠️ 기술적 세부사항

### Referer 추출 로직

프로그램은 URL을 분석하여 자동으로 Referer를 생성합니다:

```python
URL 입력:
https://example.com/videos/watch?v=12345

자동 추출:
- 프로토콜: https
- 도메인: example.com
- Referer: https://example.com/
- Origin: https://example.com
```

### 적용되는 경우

✅ **자동 적용**:
- 일반 동영상 URL (.mp4, .webm 등)
- HLS 스트림 (.m3u8)
- DASH 스트림 (.mpd)
- YouTube, Vimeo 등 모든 사이트
- 개발자 도구로 찾은 직접 URL

✅ **언제나 작동**:
- 검색 시 (동영상 정보 가져올 때)
- 다운로드 시
- 스트림 세그먼트 다운로드 시

---

## 📊 실전 예제

### 예제 1: 일반 제한된 사이트

**시나리오**: 강의 사이트에서 직접 URL로 접근 불가

**해결**:
```
URL: https://lecture.com/course/video.mp4

자동 처리:
- Referer: https://lecture.com/
- User-Agent: Chrome 120
- Origin: https://lecture.com

결과: ✅ 다운로드 성공!
```

### 예제 2: HLS 스트림 + Referer 제한

**시나리오**: .m3u8 URL에 Referer 필요

**해결**:
```
URL: https://cdn.example.com/hls/stream.m3u8

자동 처리:
- Referer: https://cdn.example.com/
- User-Agent: Chrome 120
- 모든 세그먼트에 동일 헤더 적용

결과: ✅ 전체 스트림 다운로드 성공!
```

### 예제 3: 복잡한 쿼리 파라미터

**시나리오**: 토큰과 Referer 둘 다 필요

**해결**:
```
URL: https://video.com/play?token=abc123&id=456

자동 처리:
- Referer: https://video.com/
- Origin: https://video.com
- 쿼리 파라미터 보존
- 토큰 유지

결과: ✅ 다운로드 성공!
```

---

## 🔍 문제 해결

### "403 Forbidden" 오류

**원인**: Referer 검증 실패 또는 추가 인증 필요

**해결 방법**:

1. **URL 전체 복사**
   - 쿼리 파라미터 포함 (`?token=...`)
   - 세션 정보 포함

2. **브라우저에서 로그인**
   - 사이트에 로그인
   - 로그인 후 동영상 URL 복사
   - 쿠키가 필요한 경우 별도 설정 필요

3. **다른 URL 시도**
   - 페이지 URL 대신 직접 .m3u8 URL
   - master.m3u8 대신 playlist.m3u8

### "401 Unauthorized" 오류

**원인**: 인증 토큰 필요

**해결**:
```
1. 개발자 도구(F12) 열기
2. Network 탭에서 요청 확인
3. Headers 탭 확인
4. 추가 헤더 필요 시 별도 설정
```

**현재 버전에서는**: 기본적인 Referer/User-Agent만 지원
**향후 버전**: 사용자 정의 헤더 추가 기능 예정

### 여전히 다운로드 안 됨

**가능한 원인**:

1. **DRM 보호** - 암호화된 콘텐츠 (다운로드 불가)
2. **IP 차단** - 특정 지역에서만 접근 가능
3. **세션 쿠키 필요** - 로그인 세션 필요
4. **시간 제한 토큰** - URL이 만료됨

**해결**:
- DRM: 다운로드 불가 (합법적 방법 없음)
- IP: VPN 사용 (합법적인 경우만)
- 쿠키: 브라우저 확장 프로그램 사용 필요
- 토큰: URL 다시 복사

---

## 💡 추가 팁

### 1. URL 유효 기간 확인

일부 URL은 시간 제한이 있습니다:
```
예시: ...?expires=1234567890&token=abc...

✅ 확인:
- URL 복사 후 빨리 다운로드
- 만료되면 다시 복사
```

### 2. 쿼리 파라미터 보존

URL의 모든 부분을 복사하세요:
```
❌ 잘못된 예:
https://example.com/video.m3u8

✅ 올바른 예:
https://example.com/video.m3u8?token=abc&expires=123
```

### 3. 여러 URL 형식 시도

같은 동영상의 다른 URL:
```
1. master.m3u8 (최고 품질 플레이리스트)
2. playlist.m3u8 (특정 품질 플레이리스트)
3. 직접 .ts 세그먼트 (비추천)
```

---

## 🎓 이론 설명

### HTTP Referer 헤더

**정의**:
현재 페이지를 참조한 이전 페이지의 URL을 나타내는 HTTP 헤더

**예시**:
```
사용자 행동:
1. https://example.com 방문
2. 동영상 재생 버튼 클릭
3. https://example.com/video.mp4 요청

HTTP 요청:
GET /video.mp4 HTTP/1.1
Host: example.com
Referer: https://example.com/
```

### 서버의 검증 로직

```python
# 서버 측 코드 (예시)
if request.headers.get('Referer') != 'https://example.com/':
    return 403  # Forbidden
else:
    return video_file  # OK
```

### 프로그램의 우회 방법

```python
# 프로그램 코드
http_headers = {
    'Referer': 'https://example.com/',
    'User-Agent': 'Mozilla/5.0...',
    'Origin': 'https://example.com'
}

# 서버는 정상 접근으로 인식!
```

---

## ⚖️ 법적 및 윤리적 고려사항

### ✅ 정당한 사용

- 본인이 구매한 콘텐츠
- 공개된 무료 콘텐츠
- 교육 목적의 자료
- 저작권 소유자의 허가 받은 콘텐츠

### ❌ 부적절한 사용

- 유료 콘텐츠 무단 다운로드
- 저작권 침해
- 불법 재배포
- 서비스 약관 위반

### ⚠️ 주의사항

- Referer 우회는 기술적 보호를 무력화하는 것입니다
- 합법적인 목적으로만 사용하세요
- 사이트의 이용 약관을 확인하세요
- 과도한 다운로드는 IP 차단의 원인이 될 수 있습니다

---

## 🔗 관련 문서

- **HLS 스트림 가이드**: `HLS_스트림_가이드.md`
- **사용 설명서**: `사용설명서.md`
- **Windows 가이드**: `README_WINDOWS.md`

---

## 📞 요약

### 핵심 포인트

1. ✅ **자동 처리** - 아무것도 할 필요 없음
2. ✅ **URL만 복사** - 프로그램이 Referer 자동 설정
3. ✅ **모든 사이트** - YouTube부터 제한된 사이트까지
4. ✅ **HLS/DASH** - 스트리밍 프로토콜도 지원

### 사용자 경험

```
이전: URL 복사 → 403 오류 → 포기

현재: URL 복사 → 붙여넣기 → 다운로드 성공! 🎉
```

### 기술적 우수성

- 자동 Referer 추출
- 최신 Chrome User-Agent
- 완전한 HTTP 헤더
- 세그먼트별 헤더 적용
- 쿼리 파라미터 보존

**이제 어떤 사이트든 쉽게 다운로드하세요!** 🚀
