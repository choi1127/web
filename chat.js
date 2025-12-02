document.getElementById("sendBtn").addEventListener("click", sendMessage);

async function sendMessage() {
    const userInput = document.getElementById("inputBox").value.trim();
    if (userInput === "") return;

    const outputEl = document.getElementById("output");
    outputEl.textContent = ""; // 기존 응답 지우기

    
const url = "https://ictrobot.hknu.ac.kr/ollama/api/chat";
    const payload = {
        model: "llama3.1",
        messages: [
            { role: "user", content: userInput }
        ]
    };

    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split("\n").filter(line => line.trim());

        for (const line of lines) {
            try {
                const json = JSON.parse(line);

                if (json.message && json.message.content) {
                    // 🔥 한 토큰씩 실시간 출력
                    outputEl.textContent += json.message.content;
                    outputEl.scrollTop = outputEl.scrollHeight; // 자동 스크롤
                }

            } catch (e) {
                // 파싱 중간 실패는 무시
            }
        }
    }
}
