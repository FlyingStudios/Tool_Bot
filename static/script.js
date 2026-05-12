async function sendMessage() {

    let input = document.getElementById("user-input")
    let message = input.value.trim()

    if (!message) return

    let chatBox = document.getElementById("chat-box")

    // =========================
    // USER MESSAGE (safe)
    // =========================
    let userMsg = document.createElement("p")
    userMsg.className = "user-message"
    userMsg.textContent = message
    chatBox.appendChild(userMsg)

    input.value = ""

    // =========================
    // LOADING MESSAGE
    // =========================
    let loadingMessage = document.createElement("p")
    loadingMessage.className = "bot-message"
    chatBox.appendChild(loadingMessage)

    const frames = ["...", "..", ".", ".."]
    let index = 0

    let animation = setInterval(() => {
        loadingMessage.textContent = "Wird berechnet " + frames[index]
        index = (index + 1) % frames.length
    }, 400)

    try {

        let response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        })

        if (!response.ok) {
            throw new Error("Server Error")
        }

        let data = await response.json()

        clearInterval(animation)
        loadingMessage.textContent = data.answer

    } catch (error) {

        clearInterval(animation)
        loadingMessage.textContent = "Fehler beim Verbinden mit dem Server."

    }

    chatBox.scrollTop = chatBox.scrollHeight
}