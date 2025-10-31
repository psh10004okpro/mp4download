// Video Downloader Pro - Background Script
// 다운로드 처리 및 백그라운드 작업

console.log('Video Downloader Pro: Background script loaded');

// 감지된 동영상 저장
const detectedVideos = new Map();

// 다운로드 처리
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'download') {
        handleDownload(message, sender)
            .then(result => sendResponse(result))
            .catch(error => sendResponse({ success: false, error: error.message }));
        return true; // 비동기 응답을 위해 true 반환
    }

    if (message.action === 'videoDetected') {
        handleVideoDetected(message, sender);
        sendResponse({ success: true });
    }

    if (message.action === 'getVideos') {
        const videos = Array.from(detectedVideos.values());
        sendResponse({ videos: videos });
    }

    return true;
});

// 다운로드 처리
async function handleDownload(message, sender) {
    try {
        const { url, filename, referer } = message;

        console.log('Starting download:', { url, filename, referer });

        // Chrome Downloads API 사용
        const downloadId = await chrome.downloads.download({
            url: url,
            filename: filename,
            saveAs: false, // 자동으로 다운로드 폴더에 저장
            conflictAction: 'uniquify', // 파일명 중복 시 번호 추가
            headers: [
                {
                    name: 'Referer',
                    value: referer || url
                },
                {
                    name: 'User-Agent',
                    value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            ]
        });

        console.log('Download started with ID:', downloadId);

        // 다운로드 상태 모니터링
        monitorDownload(downloadId);

        return { success: true, downloadId: downloadId };
    } catch (error) {
        console.error('Download error:', error);
        return { success: false, error: error.message };
    }
}

// 다운로드 상태 모니터링
function monitorDownload(downloadId) {
    chrome.downloads.onChanged.addListener(function listener(delta) {
        if (delta.id === downloadId) {
            if (delta.state && delta.state.current === 'complete') {
                console.log('Download completed:', downloadId);
                showNotification('다운로드 완료!', 'success');
                chrome.downloads.onChanged.removeListener(listener);
            } else if (delta.state && delta.state.current === 'interrupted') {
                console.log('Download interrupted:', downloadId);
                showNotification('다운로드 실패', 'error');
                chrome.downloads.onChanged.removeListener(listener);
            } else if (delta.error) {
                console.log('Download error:', delta.error);
                showNotification('다운로드 오류: ' + delta.error.current, 'error');
                chrome.downloads.onChanged.removeListener(listener);
            }
        }
    });
}

// 동영상 감지 처리
function handleVideoDetected(message, sender) {
    const { url, pageUrl, pageTitle } = message;
    const tabId = sender.tab?.id;

    // 동영상 정보 저장
    detectedVideos.set(url, {
        url: url,
        pageUrl: pageUrl,
        pageTitle: pageTitle,
        tabId: tabId,
        detectedAt: new Date().toISOString()
    });

    // 배지 업데이트 (감지된 동영상 수)
    if (tabId) {
        const count = Array.from(detectedVideos.values())
            .filter(v => v.tabId === tabId)
            .length;
        updateBadge(tabId, count);
    }

    console.log('Video detected and saved:', url);
}

// 배지 업데이트
function updateBadge(tabId, count) {
    if (count > 0) {
        chrome.action.setBadgeText({
            text: count.toString(),
            tabId: tabId
        });
        chrome.action.setBadgeBackgroundColor({
            color: '#4caf50',
            tabId: tabId
        });
    } else {
        chrome.action.setBadgeText({
            text: '',
            tabId: tabId
        });
    }
}

// 알림 표시
function showNotification(message, type = 'info') {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: 'Video Downloader Pro',
        message: message,
        priority: 2
    });
}

// 탭이 닫히면 해당 탭의 동영상 정보 삭제
chrome.tabs.onRemoved.addListener((tabId) => {
    for (const [url, video] of detectedVideos.entries()) {
        if (video.tabId === tabId) {
            detectedVideos.delete(url);
        }
    }
});

// 탭 업데이트 시 배지 초기화
chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
    if (changeInfo.status === 'loading') {
        // 페이지 로딩 시작 시 해당 탭의 동영상 정보 삭제
        for (const [url, video] of detectedVideos.entries()) {
            if (video.tabId === tabId) {
                detectedVideos.delete(url);
            }
        }
        updateBadge(tabId, 0);
    }
});

// 컨텍스트 메뉴 생성
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: 'downloadVideo',
        title: '동영상 다운로드',
        contexts: ['video']
    });

    chrome.contextMenus.create({
        id: 'downloadLink',
        title: '링크를 동영상으로 다운로드',
        contexts: ['link']
    });
});

// 컨텍스트 메뉴 클릭 처리
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'downloadVideo' && info.srcUrl) {
        handleDownload({
            url: info.srcUrl,
            filename: 'video_' + Date.now() + '.mp4',
            referer: info.pageUrl
        }, { tab: tab });
    } else if (info.menuItemId === 'downloadLink' && info.linkUrl) {
        handleDownload({
            url: info.linkUrl,
            filename: 'video_' + Date.now() + '.mp4',
            referer: info.pageUrl
        }, { tab: tab });
    }
});

console.log('Video Downloader Pro: Background script ready!');
