#!/usr/bin/env python3
"""
간단한 아이콘 생성 스크립트
PNG 라이브러리 없이 기본 PNG 생성
"""

def create_simple_png(size, filename):
    """간단한 보라색 사각형 PNG 생성"""
    # PNG 헤더와 간단한 보라색 이미지
    # 실제 사용 시에는 icon.svg를 변환하여 사용하세요

    import struct
    import zlib

    # PNG 시그니처
    png_signature = b'\x89PNG\r\n\x1a\n'

    # IHDR 청크 (이미지 헤더)
    width = height = size
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr_chunk = struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)

    # IDAT 청크 (이미지 데이터) - 보라색 (#764ba2)
    scanlines = b''
    for y in range(height):
        scanline = b'\x00'  # 필터 타입
        for x in range(width):
            # 보라색 그라데이션
            r = int(102 + (118 - 102) * (x / width))
            g = int(126 + (75 - 126) * (x / width))
            b = int(234 + (162 - 234) * (x / width))
            scanline += bytes([r, g, b])
        scanlines += scanline

    compressed_data = zlib.compress(scanlines, 9)
    idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
    idat_chunk = struct.pack('>I', len(compressed_data)) + b'IDAT' + compressed_data + struct.pack('>I', idat_crc)

    # IEND 청크
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    iend_chunk = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)

    # PNG 파일 작성
    with open(filename, 'wb') as f:
        f.write(png_signature)
        f.write(ihdr_chunk)
        f.write(idat_chunk)
        f.write(iend_chunk)

    print(f"✅ {filename} 생성 완료 ({size}x{size})")

if __name__ == '__main__':
    import os

    print("Chrome 확장 프로그램 아이콘 생성 중...")
    print("⚠️  이것은 임시 플레이스홀더입니다.")
    print("📝 실제 사용 시 icon.svg를 PNG로 변환하세요!\n")

    # 아이콘 디렉토리
    icon_dir = os.path.dirname(os.path.abspath(__file__))

    # 각 크기별 아이콘 생성
    sizes = [16, 48, 128]
    for size in sizes:
        filename = os.path.join(icon_dir, f'icon{size}.png')
        create_simple_png(size, filename)

    print("\n✨ 아이콘 생성 완료!")
    print("\n다음 단계:")
    print("1. icon.svg 파일을 열어 디자인 확인")
    print("2. 온라인 변환기나 ImageMagick으로 SVG를 PNG로 변환")
    print("3. 생성된 PNG 파일로 icon16.png, icon48.png, icon128.png 교체")
