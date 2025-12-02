// 메시지 전송 기능
async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-container');
    const message = inputField.value.trim();
    
    if (!message) return; // 내용이 없으면 중단

    // 1. 내 질문 화면에 표시
    appendMessage(message, 'user-message');
    inputField.value = ''; // 입력창 초기화

    // 2. AI 응답 준비 ('...' 표시)
    const aiMessageDiv = appendMessage('...', 'ai-message');
    aiMessageDiv.innerText = ''; 

    try {
        // 3. 백엔드 서버(app.py)로 전송
        // ★주의: 서버가 다른 곳에 있다면 localhost 대신 IP 주소 입력
        const response = await fetch('https://ictrobot.hknu.ac.kr/ollama/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        // 4. 스트리밍 데이터 처리 (타자 효과)
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            // 데이터 조각을 글자로 변환 후 추가
            const chunk = decoder.decode(value);
            aiMessageDiv.innerText += chunk;
            
            // 스크롤을 항상 맨 아래로
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (error) {
        console.error("에러 발생:", error);
        aiMessageDiv.innerText = "서버 연결에 실패했습니다.";
    }
}

// 화면에 말풍선을 추가하는 함수
function appendMessage(text, className) {
    const chatBox = document.getElementById('chat-container');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    msgDiv.innerText = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
}