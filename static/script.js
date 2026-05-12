async function sendMessage() {

    let input = document.getElementById("user-input")
    let message = input.value.trim()

    if (!message) return

    let chatBox = document.getElementById("chat-box")

    // USER MESSAGE
    let userMsg = document.createElement("p")
    userMsg.className = "user-message"
    userMsg.textContent = message
    chatBox.appendChild(userMsg)

    input.value = ""

    // THINKING START
    const thinking = showThinking(chatBox)

    // REQUEST
    let response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message })
    })

    let data = await response.json()

    const delay = data.delay ?? 0

    // WAIT + THEN SHOW ANSWER
    setTimeout(() => {

        clearInterval(thinking.interval)
        thinking.bubble.remove()

        let botMsg = document.createElement("p")
        botMsg.className = "bot-message"
        botMsg.textContent = data.answer
        chatBox.appendChild(botMsg)

        chatBox.scrollTop = chatBox.scrollHeight

    }, delay)
}