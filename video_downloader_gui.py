import customtkinter as ctk
import yt_dlp
import threading
import os
import json
import re
from pathlib import Path
from tkinter import filedialog, messagebox
from datetime import datetime
import tkinter as tk

# CustomTkinter 설정
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VideoDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.title("🎥 동영상 다운로더 - 쉽고 빠른 다운로드")
        self.geometry("1000x750")
        self.minsize(900, 650)

        # 설정 파일 경로
        self.config_file = Path("config.json")
        self.history_file = Path("history.json")

        # 설정 로드
        self.load_config()

        # 현재 동영상 정보
        self.current_video_info = None
        self.is_downloading = False
        self.download_history = []

        # 히스토리 로드
        self.load_history()

        # UI 구성
        self.create_widgets()

        # 클립보드 모니터링 시작
        self.last_clipboard = ""
        self.monitor_clipboard()

        # 종료 시 설정 저장
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        """설정 파일 로드"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.download_path = config.get('download_path', str(Path.home() / "Downloads"))
                    self.auto_paste = config.get('auto_paste', True)
            except:
                self.download_path = str(Path.home() / "Downloads")
                self.auto_paste = True
        else:
            self.download_path = str(Path.home() / "Downloads")
            self.auto_paste = True

    def save_config(self):
        """설정 파일 저장"""
        config = {
            'download_path': self.download_path,
            'auto_paste': self.auto_paste
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """다운로드 히스토리 로드"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.download_history = json.load(f)
            except:
                self.download_history = []
        else:
            self.download_history = []

    def save_history(self):
        """다운로드 히스토리 저장"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.download_history[-50:], f, ensure_ascii=False, indent=2)  # 최근 50개만 저장

    def create_widgets(self):
        """UI 생성"""
        # 메인 컨테이너 설정
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ===== 헤더 =====
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        title_label = ctk.CTkLabel(
            header_frame,
            text="🎥 동영상 다운로더",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="YouTube, Vimeo 등 1000개 이상의 사이트 지원",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        subtitle_label.pack()

        # ===== URL 입력 영역 =====
        input_frame = ctk.CTkFrame(self, border_width=2, border_color="#3b8ed0")
        input_frame.grid(row=1, column=0, padx=20, pady=15, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        # 안내 텍스트
        guide_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        guide_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        guide_label = ctk.CTkLabel(
            guide_frame,
            text="💡 팁: URL을 복사하면 자동으로 입력됩니다! 또는 아래 입력란에 직접 붙여넣으세요.",
            font=ctk.CTkFont(size=12),
            text_color="#3b8ed0"
        )
        guide_label.pack(side="left")

        # URL 입력
        url_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        url_container.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        url_container.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            url_container,
            placeholder_text="여기에 동영상 URL을 붙여넣으세요 (예: https://www.youtube.com/watch?v=...)",
            height=50,
            font=ctk.CTkFont(size=14),
            border_width=2
        )
        self.url_entry.grid(row=0, column=0, sticky="ew")
        self.url_entry.bind("<Return>", lambda e: self.search_video())
        self.url_entry.bind("<Control-v>", lambda e: self.after(10, self.on_paste))

        # 버튼 영역
        button_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_container.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        button_container.grid_columnconfigure(0, weight=2)
        button_container.grid_columnconfigure(1, weight=1)
        button_container.grid_columnconfigure(2, weight=1)

        self.search_button = ctk.CTkButton(
            button_container,
            text="🔍 동영상 검색하기",
            command=self.search_video,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10
        )
        self.search_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.path_button = ctk.CTkButton(
            button_container,
            text=f"📁 저장 위치",
            command=self.select_download_path,
            height=50,
            font=ctk.CTkFont(size=13),
            fg_color="#2b2b2b",
            hover_color="#3b3b3b",
            corner_radius=10
        )
        self.path_button.grid(row=0, column=1, padx=(5, 5), sticky="ew")

        self.history_button = ctk.CTkButton(
            button_container,
            text="📜 히스토리",
            command=self.show_history,
            height=50,
            font=ctk.CTkFont(size=13),
            fg_color="#2b2b2b",
            hover_color="#3b3b3b",
            corner_radius=10
        )
        self.history_button.grid(row=0, column=2, padx=(5, 0), sticky="ew")

        # 현재 저장 위치 표시
        self.path_label = ctk.CTkLabel(
            input_frame,
            text=f"💾 현재 저장 위치: {self.download_path}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.path_label.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="w")

        # ===== 동영상 정보 영역 =====
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        # 초기 도움말 메시지
        self.welcome_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.welcome_frame.pack(expand=True)

        welcome_title = ctk.CTkLabel(
            self.welcome_frame,
            text="👋 환영합니다!",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome_title.pack(pady=(20, 10))

        instructions = [
            "1️⃣  동영상 URL을 복사하세요 (자동으로 입력됩니다)",
            "2️⃣  또는 위의 입력란에 직접 붙여넣으세요",
            "3️⃣  '동영상 검색하기' 버튼을 클릭하세요",
            "4️⃣  원하는 화질을 선택하고 다운로드하세요",
            "",
            "✨ 지원 사이트: YouTube, Vimeo, Facebook, Instagram, Twitter 등"
        ]

        for instruction in instructions:
            ctk.CTkLabel(
                self.welcome_frame,
                text=instruction,
                font=ctk.CTkFont(size=14),
                text_color="gray" if instruction else "transparent"
            ).pack(pady=3)

        # ===== 진행률 영역 =====
        progress_container = ctk.CTkFrame(self)
        progress_container.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.progress_label = ctk.CTkLabel(
            progress_container,
            text="",
            font=ctk.CTkFont(size=13)
        )
        self.progress_label.pack(padx=20, pady=(15, 5))

        self.progress_bar = ctk.CTkProgressBar(progress_container, height=20)
        self.progress_bar.pack(padx=20, pady=(5, 15), fill="x")
        self.progress_bar.set(0)

    def monitor_clipboard(self):
        """클립보드 모니터링 (URL 자동 감지)"""
        if self.auto_paste:
            try:
                clipboard = self.clipboard_get()
                if clipboard != self.last_clipboard and self.is_url(clipboard):
                    self.last_clipboard = clipboard
                    if not self.url_entry.get():  # 입력란이 비어있을 때만
                        self.url_entry.delete(0, 'end')
                        self.url_entry.insert(0, clipboard)
                        self.show_notification("📋 URL이 자동으로 입력되었습니다!")
            except:
                pass

        # 500ms마다 체크
        self.after(500, self.monitor_clipboard)

    def is_url(self, text):
        """URL 여부 확인"""
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        return bool(url_pattern.match(text))

    def show_notification(self, message):
        """알림 메시지 표시"""
        self.progress_label.configure(text=message, text_color="#3b8ed0")
        self.after(3000, lambda: self.progress_label.configure(text=""))

    def on_paste(self):
        """붙여넣기 시 이벤트"""
        text = self.url_entry.get()
        if self.is_url(text):
            self.show_notification("✅ URL이 입력되었습니다. 검색 버튼을 눌러주세요!")

    def select_download_path(self):
        """다운로드 경로 선택"""
        path = filedialog.askdirectory(initialdir=self.download_path, title="다운로드 저장 위치 선택")
        if path:
            self.download_path = path
            self.path_label.configure(text=f"💾 현재 저장 위치: {self.download_path}")
            self.save_config()
            self.show_notification(f"✅ 저장 위치가 변경되었습니다!")

    def show_history(self):
        """다운로드 히스토리 표시"""
        if not self.download_history:
            messagebox.showinfo("히스토리", "다운로드 히스토리가 없습니다.")
            return

        # 히스토리 창 생성
        history_window = ctk.CTkToplevel(self)
        history_window.title("📜 다운로드 히스토리")
        history_window.geometry("700x500")

        # 제목
        title = ctk.CTkLabel(
            history_window,
            text="📜 다운로드 히스토리",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)

        # 스크롤 프레임
        scroll_frame = ctk.CTkScrollableFrame(history_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 히스토리 항목 표시
        for i, item in enumerate(reversed(self.download_history[-20:])):  # 최근 20개
            item_frame = ctk.CTkFrame(scroll_frame)
            item_frame.pack(fill="x", pady=5)

            title_label = ctk.CTkLabel(
                item_frame,
                text=f"📹 {item.get('title', 'Unknown')}",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w"
            )
            title_label.pack(fill="x", padx=15, pady=(10, 5))

            info_label = ctk.CTkLabel(
                item_frame,
                text=f"🕐 {item.get('date', 'Unknown')} | {item.get('url', '')}",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w"
            )
            info_label.pack(fill="x", padx=15, pady=(0, 10))

        # 닫기 버튼
        close_btn = ctk.CTkButton(
            history_window,
            text="닫기",
            command=history_window.destroy,
            width=150
        )
        close_btn.pack(pady=(0, 20))

    def search_video(self):
        """동영상 정보 검색"""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("오류", "URL을 입력해주세요!")
            return

        if not self.is_url(url):
            messagebox.showerror("오류", "올바른 URL을 입력해주세요!")
            return

        # UI 비활성화
        self.search_button.configure(state="disabled", text="🔍 검색 중...")
        self.progress_label.configure(text="🔄 동영상 정보를 가져오는 중... 잠시만 기다려주세요!", text_color="white")

        # 환영 메시지 제거
        if hasattr(self, 'welcome_frame'):
            self.welcome_frame.destroy()

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
        title_frame = ctk.CTkFrame(scroll_frame, fg_color="#1f538d")
        title_frame.pack(fill="x", pady=(10, 15), padx=5)

        title_label = ctk.CTkLabel(
            title_frame,
            text=f"📹 {info.get('title', 'Unknown')}",
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=850,
            justify="left"
        )
        title_label.pack(pady=15, padx=15, anchor="w")

        # 동영상 정보
        info_frame = ctk.CTkFrame(scroll_frame)
        info_frame.pack(fill="x", pady=(0, 15), padx=5)

        info_details = [
            f"📺 업로더: {info.get('uploader', 'Unknown')}",
            f"⏱️ 길이: {self.format_duration(info.get('duration', 0))}",
            f"👁️ 조회수: {info.get('view_count', 0):,}회" if info.get('view_count') else ""
        ]

        for detail in info_details:
            if detail:
                ctk.CTkLabel(
                    info_frame,
                    text=detail,
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(fill="x", padx=15, pady=5)

        # 포맷 섹션
        format_header = ctk.CTkLabel(
            scroll_frame,
            text="⬇️ 다운로드 옵션 (원하는 화질을 선택하세요):",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        format_header.pack(pady=(15, 10), padx=5, anchor="w")

        # 최고 품질 옵션 (강조)
        best_frame = ctk.CTkFrame(scroll_frame, fg_color="#1a4d2e", border_width=2, border_color="#4caf50")
        best_frame.pack(fill="x", pady=8, padx=5)

        best_container = ctk.CTkFrame(best_frame, fg_color="transparent")
        best_container.pack(fill="x", padx=15, pady=15)
        best_container.grid_columnconfigure(0, weight=1)

        best_info = ctk.CTkLabel(
            best_container,
            text="🌟 최고 품질 (추천)\n최상의 화질과 음질로 다운로드합니다",
            font=ctk.CTkFont(size=15, weight="bold"),
            justify="left"
        )
        best_info.grid(row=0, column=0, sticky="w")

        best_btn = ctk.CTkButton(
            best_container,
            text="⬇️ 다운로드",
            command=lambda: self.download_video('best'),
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4caf50",
            hover_color="#45a049"
        )
        best_btn.grid(row=0, column=1, padx=(10, 0))

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
                if height and height not in seen_heights and len(unique_formats) < 6:
                    seen_heights.add(height)
                    unique_formats.append(fmt)

            for fmt in unique_formats:
                format_frame = ctk.CTkFrame(scroll_frame)
                format_frame.pack(fill="x", pady=5, padx=5)

                format_container = ctk.CTkFrame(format_frame, fg_color="transparent")
                format_container.pack(fill="x", padx=15, pady=12)
                format_container.grid_columnconfigure(0, weight=1)

                resolution = fmt.get('resolution', 'unknown')
                ext = fmt.get('ext', 'mp4')
                filesize = fmt.get('filesize', 0)
                format_note = fmt.get('format_note', '')

                format_text = f"📹 {resolution} ({ext})"
                if format_note:
                    format_text += f" - {format_note}"
                if filesize:
                    format_text += f"\n💾 파일 크기: {self.format_filesize(filesize)}"

                format_info = ctk.CTkLabel(
                    format_container,
                    text=format_text,
                    font=ctk.CTkFont(size=13),
                    justify="left"
                )
                format_info.grid(row=0, column=0, sticky="w")

                format_btn = ctk.CTkButton(
                    format_container,
                    text="⬇️ 다운로드",
                    command=lambda f=fmt['format_id']: self.download_video(f),
                    width=150,
                    height=40,
                    font=ctk.CTkFont(size=13, weight="bold")
                )
                format_btn.grid(row=0, column=1, padx=(10, 0))

        # 검색 버튼 재활성화
        self.search_button.configure(state="normal", text="🔍 동영상 검색하기")
        self.progress_label.configure(text="✅ 동영상 정보를 불러왔습니다! 원하는 화질을 선택하세요.", text_color="#4caf50")

    def download_video(self, format_id):
        """동영상 다운로드"""
        if self.is_downloading:
            messagebox.showwarning("경고", "이미 다운로드가 진행 중입니다!")
            return

        url = self.url_entry.get().strip()

        self.is_downloading = True
        self.progress_bar.set(0)
        self.progress_label.configure(text="⏳ 다운로드 준비 중...", text_color="white")

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
                            speed = d.get('speed', 0)
                            eta = d.get('eta', 0)

                            speed_text = f"{self.format_filesize(speed)}/s" if speed else ""
                            eta_text = f"남은 시간: {int(eta)}초" if eta else ""

                            status = f"⬇️ 다운로드 중: {int(percent * 100)}% ({self.format_filesize(downloaded)} / {self.format_filesize(total)})"
                            if speed_text:
                                status += f" | 속도: {speed_text}"
                            if eta_text:
                                status += f" | {eta_text}"

                            self.after(0, self.update_progress, percent, status)
                        else:
                            self.after(0, self.update_progress, 0,
                                     f"⬇️ 다운로드 중: {self.format_filesize(downloaded)}")
                    except:
                        pass

                elif d['status'] == 'finished':
                    self.after(0, self.update_progress, 1.0, "✨ 다운로드 완료! 파일 처리 중...")

            ydl_opts = {
                'format': format_id if format_id != 'best' else 'best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': False,
                'no_warnings': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # 히스토리에 추가
            if self.current_video_info:
                self.download_history.append({
                    'title': self.current_video_info.get('title', 'Unknown'),
                    'url': url,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                self.save_history()

            self.after(0, self.download_complete)

        except Exception as e:
            self.after(0, self.download_error, str(e))

    def update_progress(self, value, text):
        """진행률 업데이트"""
        self.progress_bar.set(value)
        self.progress_label.configure(text=text, text_color="white")

    def download_complete(self):
        """다운로드 완료"""
        self.is_downloading = False
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="✅ 다운로드가 완료되었습니다! 🎉", text_color="#4caf50")

        # 완료 메시지
        result = messagebox.askyesno(
            "다운로드 완료",
            f"다운로드가 완료되었습니다!\n\n저장 위치: {self.download_path}\n\n폴더를 여시겠습니까?"
        )

        if result:
            # 탐색기에서 폴더 열기
            os.startfile(self.download_path)

    def download_error(self, error_msg):
        """다운로드 오류"""
        self.is_downloading = False
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
        self.show_error(f"다운로드 오류가 발생했습니다:\n\n{error_msg}\n\n다른 URL을 시도해보세요.")

    def show_error(self, message):
        """오류 메시지 표시"""
        self.search_button.configure(state="normal", text="🔍 동영상 검색하기")
        self.progress_label.configure(text="❌ 오류가 발생했습니다", text_color="#f44336")
        messagebox.showerror("오류", message)

    def on_closing(self):
        """프로그램 종료"""
        self.save_config()
        self.destroy()

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
        if not bytes or bytes == 0:
            return "알 수 없음"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"


def main():
    """프로그램 시작"""
    app = VideoDownloaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
