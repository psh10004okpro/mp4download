from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import yt_dlp
import os
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

# 다운로드 디렉토리 설정
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/video-info', methods=['POST'])
def get_video_info():
    """URL에서 동영상 정보 추출"""
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL이 필요합니다'}), 400

        # yt-dlp 옵션 설정
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # 포맷 정보 추출
            formats = []
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                        format_info = {
                            'format_id': f.get('format_id'),
                            'ext': f.get('ext'),
                            'resolution': f.get('resolution', 'audio only' if f.get('vcodec') == 'none' else 'unknown'),
                            'filesize': f.get('filesize', 0),
                            'vcodec': f.get('vcodec', 'none'),
                            'acodec': f.get('acodec', 'none'),
                            'format_note': f.get('format_note', ''),
                        }
                        formats.append(format_info)

            video_info = {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'formats': formats,
            }

            return jsonify(video_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download_video():
    """동영상 다운로드"""
    try:
        data = request.json
        url = data.get('url')
        format_id = data.get('format_id', 'best')

        if not url:
            return jsonify({'error': 'URL이 필요합니다'}), 400

        # 파일명 생성을 위한 정보 추출
        ydl_opts_info = {
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            ext = info.get('ext', 'mp4')

        # 안전한 파일명 생성
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).rstrip()
        output_filename = f"{safe_title}.%(ext)s"
        output_path = str(DOWNLOAD_DIR / output_filename)

        # 다운로드 옵션
        ydl_opts = {
            'format': format_id if format_id != 'best' else 'best',
            'outtmpl': output_path,
            'quiet': False,
        }

        # 다운로드 실행
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 다운로드된 파일 찾기
        downloaded_files = list(DOWNLOAD_DIR.glob(f"{safe_title}.*"))
        if not downloaded_files:
            return jsonify({'error': '다운로드된 파일을 찾을 수 없습니다'}), 500

        file_path = downloaded_files[0]

        return jsonify({
            'message': '다운로드 완료',
            'filename': file_path.name,
            'download_url': f'/api/file/{file_path.name}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file/<filename>')
def download_file(filename):
    """다운로드된 파일 전송"""
    try:
        file_path = DOWNLOAD_DIR / filename
        if not file_path.exists():
            return jsonify({'error': '파일을 찾을 수 없습니다'}), 404

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """다운로드 폴더 정리"""
    try:
        for file in DOWNLOAD_DIR.glob('*'):
            if file.is_file():
                file.unlink()
        return jsonify({'message': '정리 완료'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
