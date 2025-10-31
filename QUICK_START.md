# ⚡ 빠른 시작 가이드

## 🎯 원하는 것에 따라 선택하세요

---

## 1️⃣ 지금 바로 사용하기 (Python 실행)

### Windows에서:

```bash
# 패키지 설치
pip install -r requirements.txt

# 프로그램 실행
python video_downloader_gui.py
```

또는 더 쉽게:
```bash
run.bat
```

---

## 2️⃣ EXE 파일 만들기

### ✨ 가장 쉬운 방법 (Windows PC에서)

1. `build.bat` 파일 더블클릭
2. 완료! → `dist/VideoDownloader.exe` 생성

### 📱 또는 명령어로:

```bash
pip install -r requirements.txt
python build_exe.py
```

결과: `dist/VideoDownloader.exe` (어디서나 실행 가능!)

---

## 3️⃣ GitHub에서 자동으로 빌드받기

### Windows PC가 없다면?

1. 이 프로젝트를 GitHub에 푸시
2. GitHub → Actions 탭 확인
3. 빌드 완료 후 EXE 다운로드!

**자동 빌드 설정이 이미 되어있습니다!** (`.github/workflows/build-exe.yml`)

---

## 📖 상세 가이드

- **일반 사용법**: [README.md](README.md)
- **Windows 가이드**: [README_WINDOWS.md](README_WINDOWS.md)
- **빌드 상세 가이드**: [BUILD_GUIDE.md](BUILD_GUIDE.md)

---

## 💡 추천

- **개발/테스트**: `python video_downloader_gui.py`
- **일반 사용자**: `VideoDownloader.exe`
- **배포**: GitHub Actions 자동 빌드

---

## 🆘 도움이 필요하신가요?

### 일반적인 문제

**"Python이 설치되어 있지 않습니다"**
→ https://www.python.org/downloads/ 에서 다운로드

**"pip: command not found"**
→ Python 재설치 (PATH 옵션 체크)

**"ModuleNotFoundError"**
→ `pip install -r requirements.txt`

**"EXE를 만들 수 없어요"**
→ [BUILD_GUIDE.md](BUILD_GUIDE.md) 참조

---

## 🎉 완료!

이제 동영상 다운로더를 사용할 준비가 되었습니다!

URL을 입력하고 다운로드 버튼만 누르면 끝! 😊
