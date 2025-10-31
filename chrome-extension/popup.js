// Video Downloader Pro - Popup Script

document.addEventListener('DOMContentLoaded', () => {
    loadVideos();

    // 새로고침 버튼
    document.getElementById('refreshBtn').addEventListener('click', () => {
        loadVideos();
    });
});

// 동영상 목록 로드
async function loadVideos() {
    const container = document.getElementById('videoListContainer');
    const countElement = document.getElementById('videoCount');

    // 로딩 표시
    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>동영상 검색 중...</p>
        </div>
    `;

    try {
        // 현재 탭 가져오기
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Content script에서 동영상 목록 가져오기
        const response = await chrome.tabs.sendMessage(tab.id, {
            action: 'getDetectedVideos'
        });

        const videos = response?.videos || [];

        // 동영상 수 업데이트
        countElement.textContent = videos.length;

        // 동영상 목록 표시
        if (videos.length === 0) {
            container.innerHTML = `
                <div class="empty-message">
                    <div class="empty-message-icon">📹</div>
                    <p>이 페이지에서 동영상을 찾을 수 없습니다.</p>
                    <p style="font-size: 12px; margin-top: 10px; opacity: 0.7;">
                        동영상을 재생하면 자동으로 감지됩니다!
                    </p>
                </div>
            `;
        } else {
            const listHtml = videos.map((url, index) => {
                const filename = extractFilename(url);
                return `
                    <div class="video-item" data-url="${escapeHtml(url)}" data-index="${index}">
                        <div class="video-title">📹 ${filename}</div>
                        <div class="video-url">${truncateUrl(url)}</div>
                    </div>
                `;
            }).join('');

            container.innerHTML = `<div class="video-list">${listHtml}</div>`;

            // 클릭 이벤트 추가
            document.querySelectorAll('.video-item').forEach(item => {
                item.addEventListener('click', () => {
                    const url = item.dataset.url;
                    downloadVideo(url, response.pageTitle);
                });
            });
        }
    } catch (error) {
        console.error('Error loading videos:', error);
        container.innerHTML = `
            <div class="empty-message">
                <div class="empty-message-icon">⚠️</div>
                <p>동영상을 불러올 수 없습니다.</p>
                <p style="font-size: 12px; margin-top: 10px; opacity: 0.7;">
                    페이지를 새로고침해주세요.
                </p>
            </div>
        `;
        countElement.textContent = '0';
    }
}

// 동영상 다운로드
async function downloadVideo(url, pageTitle) {
    try {
        // 파일명 생성
        const title = pageTitle || 'video';
        const sanitizedTitle = title.replace(/[^a-z0-9가-힣]/gi, '_').substring(0, 50);
        const extension = url.includes('.m3u8') ? 'm3u8' :
                         url.includes('.mpd') ? 'mpd' :
                         url.split('.').pop().split('?')[0] || 'mp4';
        const filename = `${sanitizedTitle}_${Date.now()}.${extension}`;

        // 현재 탭 URL 가져오기
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // 백그라운드 스크립트로 다운로드 요청
        const response = await chrome.runtime.sendMessage({
            action: 'download',
            url: url,
            filename: filename,
            referer: tab.url
        });

        if (response.success) {
            showMessage('✅ 다운로드 시작!', 'success');
        } else {
            showMessage('❌ 다운로드 실패: ' + response.error, 'error');
        }
    } catch (error) {
        console.error('Download error:', error);
        showMessage('❌ 오류: ' + error.message, 'error');
    }
}

// 메시지 표시
function showMessage(message, type) {
    const container = document.getElementById('videoListContainer');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    `;
    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.remove();
    }, 2000);
}

// URL에서 파일명 추출
function extractFilename(url) {
    try {
        const urlObj = new URL(url);
        const pathname = urlObj.pathname;
        const filename = pathname.split('/').pop();
        return filename || 'video';
    } catch {
        return 'video';
    }
}

// URL 축약
function truncateUrl(url, maxLength = 50) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// HTML 이스케이프
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
