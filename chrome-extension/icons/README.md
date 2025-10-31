# 아이콘 생성 방법

## SVG를 PNG로 변환하기

`icon.svg` 파일을 다양한 크기의 PNG 파일로 변환해야 합니다.

### 방법 1: 온라인 변환기 사용

1. https://cloudconvert.com/svg-to-png 접속
2. `icon.svg` 업로드
3. 다음 크기로 각각 변환:
   - 16x16 → `icon16.png`
   - 48x48 → `icon48.png`
   - 128x128 → `icon128.png`

### 방법 2: ImageMagick 사용 (명령줄)

```bash
# ImageMagick 설치 (Windows)
# https://imagemagick.org/script/download.php

# 변환
magick icon.svg -resize 16x16 icon16.png
magick icon.svg -resize 48x48 icon48.png
magick icon.svg -resize 128x128 icon128.png
```

### 방법 3: Inkscape 사용

```bash
# Inkscape 설치 후
inkscape icon.svg -w 16 -h 16 -o icon16.png
inkscape icon.svg -w 48 -h 48 -o icon48.png
inkscape icon.svg -w 128 -h 128 -o icon128.png
```

### 방법 4: 온라인 편집기

1. https://www.photopea.com/ 접속
2. `icon.svg` 열기
3. Image → Image Size에서 크기 조정
4. File → Export As → PNG

## 필요한 파일

- `icon16.png` - 확장 프로그램 파비콘
- `icon48.png` - 확장 프로그램 관리 페이지
- `icon128.png` - Chrome 웹 스토어, 설치 시

## 디자인 변경

`icon.svg` 파일을 편집하여 원하는 디자인으로 변경할 수 있습니다.
현재 디자인은 보라색 그라데이션 배경에 동영상과 다운로드 화살표 아이콘입니다.
