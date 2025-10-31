// Video Downloader Pro - Content Script
// 페이지의 모든 동영상을 감지하고 다운로드 버튼 추가

console.log('Video Downloader Pro: Content script loaded');

// 감지된 동영상 목록
const detectedVideos = new Set();

// 유효한 동영상 URL 확인
function isValidVideoUrl(url) {
    if (!url || typeof url !== 'string') {
        return false;
    }

    // http:// 또는 https://로 시작해야 함
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        return false;
    }

    // 잘못된 확장자 필터링 (웹페이지 파일)
    const invalidExtensions = [
        '.html', '.htm', '.shtml', '.php', '.asp', '.aspx',
        '.jsp', '.cgi', '.pl', '.py', '.rb'
    ];

    const urlLower = url.toLowerCase();
    for (const ext of invalidExtensions) {
        if (urlLower.includes(ext)) {
            console.log('Rejected non-video URL:', url);
            return false;
        }
    }

    // 유효한 동영상 확장자
    const validExtensions = [
        '.mp4', '.webm', '.ogg', '.m3u8', '.mpd',
        '.m4v', '.mov', '.avi', '.mkv', '.flv',
        '.ts', '.m4s' // 스트리밍 세그먼트
    ];

    // 확장자가 명확한 경우
    for (const ext of validExtensions) {
        if (urlLower.includes(ext)) {
            return true;
        }
    }

    // 쿼리 파라미터 제거 후 확인
    const urlWithoutQuery = url.split('?')[0].toLowerCase();
    for (const ext of validExtensions) {
        if (urlWithoutQuery.endsWith(ext)) {
            return true;
        }
    }

    // Blob URL은 별도 처리
    if (url.startsWith('blob:')) {
        console.warn('Blob URL detected - cannot download directly:', url);
        return false;
    }

    // 확장자가 없지만 의심스러운 패턴
    // video, stream, media 등의 키워드 포함
    const videoKeywords = ['video', 'stream', 'media', 'play', 'watch'];
    const hasVideoKeyword = videoKeywords.some(keyword => urlLower.includes(keyword));

    if (hasVideoKeyword) {
        // URL에 확장자가 없지만 비디오 관련 키워드가 있음
        // 사용자에게 경고하고 시도는 허용
        console.warn('Detected possible video URL without extension:', url);
        return true;
    }

    // 기본적으로 거부
    console.log('Rejected unknown URL format:', url);
    return false;
}

// 다운로드 버튼 생성
function createDownloadButton(videoElement, videoUrl) {
    // 이미 버튼이 있으면 생성하지 않음
    if (videoElement.dataset.vdpButton) {
        return;
    }

    const button = document.createElement('div');
    button.className = 'vdp-download-button';
    button.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
            <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
        </svg>
        <span>다운로드</span>
    `;

    button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        downloadVideo(videoUrl, videoElement);
    });

    // 동영상 컨테이너 찾기
    const container = findVideoContainer(videoElement);
    if (container) {
        container.style.position = 'relative';
        container.appendChild(button);
        videoElement.dataset.vdpButton = 'true';
    }
}

// 동영상 컨테이너 찾기
function findVideoContainer(videoElement) {
    let parent = videoElement.parentElement;
    let depth = 0;
    const maxDepth = 5;

    while (parent && depth < maxDepth) {
        const style = window.getComputedStyle(parent);
        if (style.position === 'relative' || style.position === 'absolute') {
            return parent;
        }
        parent = parent.parentElement;
        depth++;
    }

    // 적절한 컨테이너를 못 찾으면 직접 부모 사용
    return videoElement.parentElement;
}

// 동영상 다운로드
function downloadVideo(url, videoElement) {
    console.log('Downloading video:', url);

    // 파일명 생성
    const title = document.title || 'video';
    const sanitizedTitle = title.replace(/[^a-z0-9가-힣]/gi, '_').substring(0, 50);
    const extension = url.includes('.m3u8') ? 'm3u8' :
                     url.includes('.mpd') ? 'mpd' :
                     url.split('.').pop().split('?')[0] || 'mp4';
    const filename = `${sanitizedTitle}.${extension}`;

    // 백그라운드 스크립트로 다운로드 요청
    chrome.runtime.sendMessage({
        action: 'download',
        url: url,
        filename: filename,
        referer: window.location.href
    }, (response) => {
        if (response && response.success) {
            showNotification('다운로드 시작!', 'success');
        } else {
            showNotification('다운로드 실패: ' + (response?.error || '알 수 없는 오류'), 'error');
        }
    });
}

// 알림 표시
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `vdp-notification vdp-notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('vdp-notification-show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('vdp-notification-show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// HTML5 Video 태그 감지
function detectVideoElements() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        if (!video.dataset.vdpProcessed) {
            video.dataset.vdpProcessed = 'true';

            // src 속성에서 URL 가져오기
            if (video.src && isValidVideoUrl(video.src)) {
                console.log('Found valid video (src):', video.src);
                detectedVideos.add(video.src);
                createDownloadButton(video, video.src);
            }

            // source 태그에서 URL 가져오기
            const sources = video.querySelectorAll('source');
            sources.forEach(source => {
                if (source.src && isValidVideoUrl(source.src)) {
                    console.log('Found valid video (source):', source.src);
                    detectedVideos.add(source.src);
                    createDownloadButton(video, source.src);
                }
            });

            // currentSrc 체크 (재생 중인 소스)
            if (video.currentSrc && isValidVideoUrl(video.currentSrc)) {
                console.log('Found valid video (currentSrc):', video.currentSrc);
                detectedVideos.add(video.currentSrc);
                createDownloadButton(video, video.currentSrc);
            }
        }
    });
}

// Network 요청에서 동영상 URL 감지
function interceptNetworkRequests() {
    // XMLHttpRequest 가로채기
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        if (isValidVideoUrl(url)) {
            console.log('Detected valid video URL (XHR):', url);
            detectedVideos.add(url);
            notifyVideoDetected(url);
        }
        return originalOpen.apply(this, arguments);
    };

    // Fetch API 가로채기
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        if (typeof url === 'string' && isValidVideoUrl(url)) {
            console.log('Detected valid video URL (Fetch):', url);
            detectedVideos.add(url);
            notifyVideoDetected(url);
        }
        return originalFetch.apply(this, arguments);
    };
}

// 동영상 감지 알림
function notifyVideoDetected(url) {
    chrome.runtime.sendMessage({
        action: 'videoDetected',
        url: url,
        pageUrl: window.location.href,
        pageTitle: document.title
    });
}

// MutationObserver로 동적으로 추가되는 동영상 감지
function observeDOM() {
    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            if (mutation.addedNodes.length) {
                detectVideoElements();
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// MediaSource API 감지 (HLS, DASH 등)
function detectMediaSource() {
    const originalAddSourceBuffer = MediaSource.prototype.addSourceBuffer;
    MediaSource.prototype.addSourceBuffer = function(mimeType) {
        console.log('MediaSource detected:', mimeType);

        // 현재 재생 중인 비디오 요소 찾기
        const videos = document.querySelectorAll('video');
        videos.forEach(video => {
            if (video.currentSrc && isValidVideoUrl(video.currentSrc)) {
                console.log('Valid MSE video source:', video.currentSrc);
                detectedVideos.add(video.currentSrc);
            }
        });

        return originalAddSourceBuffer.apply(this, arguments);
    };
}

// Blob URL 감지
function detectBlobUrls() {
    const originalCreateObjectURL = URL.createObjectURL;
    URL.createObjectURL = function(blob) {
        const blobUrl = originalCreateObjectURL.apply(this, arguments);

        if (blob.type && blob.type.includes('video')) {
            console.log('Detected Blob video:', blobUrl, 'Type:', blob.type);
            // Blob URL은 직접 다운로드 불가능하지만 감지는 함
            showNotification('Blob 동영상 감지됨 (직접 다운로드 불가)', 'info');
        }

        return blobUrl;
    };
}

// 초기화
function init() {
    console.log('Video Downloader Pro: Initializing...');

    // 기존 동영상 감지
    detectVideoElements();

    // Network 요청 감지
    interceptNetworkRequests();

    // DOM 변경 감시
    observeDOM();

    // MediaSource API 감지
    detectMediaSource();

    // Blob URL 감지
    detectBlobUrls();

    // 주기적으로 동영상 재확인 (동적 로딩 대응)
    setInterval(detectVideoElements, 2000);

    console.log('Video Downloader Pro: Ready!');
}

// 페이지 로드 완료 후 초기화
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// 메시지 수신
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getDetectedVideos') {
        sendResponse({
            videos: Array.from(detectedVideos),
            pageUrl: window.location.href,
            pageTitle: document.title
        });
    }
    return true;
});
