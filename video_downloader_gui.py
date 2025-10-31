import customtkinter as ctk
import yt_dlp
import threading
import os
from pathlib import Path
from tkinter import filedialog, messagebox
import json

# CustomTkinter 설정
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VideoDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.title("동영상 다운로더")
        self.geometry("900x700")
        self.minsize(800, 600)

        # 다운로드 경로 설정
        self.download_path = str(Path.home() / "Downloads")

        # 현재 동영상 정보
        self.current_video_info = None
        self.is_downloading = False

        # UI 구성
        self.create_widgets()

    def create_widgets(self):
        # 메인 컨테이너
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 헤더
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        title_label = ctk.CTkLabel(
            header_frame,
            text="🎥 동영상 다운로더",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack()

        # URL 입력 섹션
        url_frame = ctk.CTkFrame(self)
        url_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        url_frame.grid_columnconfigure(0, weight=1)

        url_label = ctk.CTkLabel(
            url_frame,
            text="동영상 URL:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        url_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="YouTube, Vimeo, Facebook 등의 동영상 URL을 입력하세요...",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.url_entry.bind("<Return>", lambda e: self.search_video())

        button_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.search_button = ctk.CTkButton(
            button_frame,
            text="🔍 검색",
            command=self.search_video,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.search_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.path_button = ctk.CTkButton(
            button_frame,
            text="📁 저장 위치: " + self.download_path,
            command=self.select_download_path,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="#2b2b2b",
            hover_color="#3b3b3b"
        )
        self.path_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # 동영상 정보 섹션
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        # 초기 메시지
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="위에 URL을 입력하고 검색 버튼을 클릭하세요",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.info_label.pack(expand=True)

        # 진행률 섹션
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(padx=20, pady=(15, 5))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(padx=20, pady=(5, 15), fill="x")
        self.progress_bar.set(0)

    def select_download_path(self):
        """다운로드 경로 선택"""
        path = filedialog.askdirectory(initialdir=self.download_path)
        if path:
            self.download_path = path
            self.path_button.configure(text=f"📁 저장 위치: {self.download_path}")

    def search_video(self):
        """동영상 정보 검색"""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("오류", "URL을 입력해주세요")
            return

        # UI 비활성화
        self.search_button.configure(state="disabled", text="검색 중...")
        self.info_label.configure(text="동영상 정보를 가져오는 중...")

        # 백그라운드에서 검색
        thread = threading.Thread(target=self._search_video_thread, args=(url,))
        thread.daemon = True
        thread.start()

    def _search_video_thread(self, url):
        """동영상 정보 검색 (백그라운드)"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.current_video_info = info

                # UI 업데이트 (메인 스레드에서)
                self.after(0, self.display_video_info, info)

        except Exception as e:
            self.after(0, self.show_error, str(e))

    def display_video_info(self, info):
        """동영상 정보 표시"""
        # 기존 위젯 제거
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # 스크롤 가능한 프레임
        scroll_frame = ctk.CTkScrollableFrame(self.info_frame)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 동영상 제목
        title_label = ctk.CTkLabel(
            scroll_frame,
            text=info.get('title', 'Unknown'),
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=800
        )
        title_label.pack(pady=(10, 5), anchor="w")

        # 동영상 정보
        info_text = f"📺 업로더: {info.get('uploader', 'Unknown')}\n"
        info_text += f"⏱️ 길이: {self.format_duration(info.get('duration', 0))}"

        info_detail = ctk.CTkLabel(
            scroll_frame,
            text=info_text,
            font=ctk.CTkFont(size=13),
            text_color="gray",
            justify="left"
        )
        info_detail.pack(pady=(0, 15), anchor="w")

        # 포맷 섹션
        format_label = ctk.CTkLabel(
            scroll_frame,
            text="다운로드 옵션:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        format_label.pack(pady=(10, 10), anchor="w")

        # 최고 품질 옵션
        best_frame = ctk.CTkFrame(scroll_frame)
        best_frame.pack(fill="x", pady=5)

        best_info = ctk.CTkLabel(
            best_frame,
            text="🌟 최고 품질 (비디오 + 오디오)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        best_info.pack(side="left", padx=15, pady=15)

        best_btn = ctk.CTkButton(
            best_frame,
            text="다운로드",
            command=lambda: self.download_video('best'),
            width=120,
            height=35
        )
        best_btn.pack(side="right", padx=15, pady=10)

        # 포맷 목록
        if 'formats' in info:
            formats = info['formats']

            # 비디오+오디오 포맷 필터링
            video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none']

            # 해상도별 정렬
            video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)

            # 중복 제거 및 주요 포맷만 표시
            seen_heights = set()
            unique_formats = []

            for fmt in video_formats:
                height = fmt.get('height', 0)
                if height and height not in seen_heights and len(unique_formats) < 5:
                    seen_heights.add(height)
                    unique_formats.append(fmt)

            for fmt in unique_formats:
                format_frame = ctk.CTkFrame(scroll_frame)
                format_frame.pack(fill="x", pady=5)

                resolution = fmt.get('resolution', 'unknown')
                ext = fmt.get('ext', 'mp4')
                filesize = fmt.get('filesize', 0)
                format_note = fmt.get('format_note', '')

                format_text = f"📹 {resolution} ({ext})"
                if format_note:
                    format_text += f" - {format_note}"
                if filesize:
                    format_text += f" - {self.format_filesize(filesize)}"

                format_info = ctk.CTkLabel(
                    format_frame,
                    text=format_text,
                    font=ctk.CTkFont(size=13)
                )
                format_info.pack(side="left", padx=15, pady=12)

                format_btn = ctk.CTkButton(
                    format_frame,
                    text="다운로드",
                    command=lambda f=fmt['format_id']: self.download_video(f),
                    width=120,
                    height=35
                )
                format_btn.pack(side="right", padx=15, pady=10)

        # 검색 버튼 재활성화
        self.search_button.configure(state="normal", text="🔍 검색")

    def download_video(self, format_id):
        """동영상 다운로드"""
        if self.is_downloading:
            messagebox.showwarning("경고", "이미 다운로드가 진행 중입니다")
            return

        url = self.url_entry.get().strip()

        self.is_downloading = True
        self.progress_bar.set(0)
        self.progress_label.configure(text="다운로드 준비 중...")

        # 백그라운드에서 다운로드
        thread = threading.Thread(target=self._download_video_thread, args=(url, format_id))
        thread.daemon = True
        thread.start()

    def _download_video_thread(self, url, format_id):
        """동영상 다운로드 (백그라운드)"""
        try:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        downloaded = d.get('downloaded_bytes', 0)
                        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

                        if total > 0:
                            percent = downloaded / total
                            self.after(0, self.update_progress, percent,
                                     f"다운로드 중: {int(percent * 100)}% ({self.format_filesize(downloaded)} / {self.format_filesize(total)})")
                        else:
                            self.after(0, self.update_progress, 0,
                                     f"다운로드 중: {self.format_filesize(downloaded)}")
                    except:
                        pass

                elif d['status'] == 'finished':
                    self.after(0, self.update_progress, 1.0, "다운로드 완료! 파일 처리 중...")

            ydl_opts = {
                'format': format_id if format_id != 'best' else 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': False,
                'no_warnings': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.after(0, self.download_complete)

        except Exception as e:
            self.after(0, self.download_error, str(e))

    def update_progress(self, value, text):
        """진행률 업데이트"""
        self.progress_bar.set(value)
        self.progress_label.configure(text=text)

    def download_complete(self):
        """다운로드 완료"""
        self.is_downloading = False
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="✅ 다운로드가 완료되었습니다!")
        messagebox.showinfo("완료", f"다운로드가 완료되었습니다!\n저장 위치: {self.download_path}")

    def download_error(self, error_msg):
        """다운로드 오류"""
        self.is_downloading = False
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
        self.show_error(f"다운로드 오류: {error_msg}")

    def show_error(self, message):
        """오류 메시지 표시"""
        self.search_button.configure(state="normal", text="🔍 검색")
        self.info_label.configure(text="오류가 발생했습니다")
        messagebox.showerror("오류", message)

    @staticmethod
    def format_duration(seconds):
        """초를 시:분:초 형식으로 변환"""
        if not seconds:
            return "0:00"

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    @staticmethod
    def format_filesize(bytes):
        """바이트를 읽기 쉬운 형식으로 변환"""
        if bytes == 0:
            return "크기 정보 없음"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"


def main():
    app = VideoDownloaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
