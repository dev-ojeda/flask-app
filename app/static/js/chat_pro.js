const socketChat = io("/chat"); // Conecta con el servidor SocketIO en la ns Chat
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');
const btnSendMessge = document.getElementById('btnSendMessage')


btnSendMessge.addEventListener()

function sendMessage() {
    const messageText = chatInput.value.trim();
    if (messageText === '') return;

    // Add sent message
    const sentMessage = document.createElement('div');
    sentMessage.classList.add('message', 'sent');
    sentMessage.textContent = messageText;
    chatBody.appendChild(sentMessage);

    // Clear input
    chatInput.value = '';

    // Simulate received message
    setTimeout(() => {
        const receivedMessage = document.createElement('div');
        receivedMessage.classList.add('message', 'received');
        receivedMessage.textContent = 'This is a response to: ' + messageText;
        chatBody.appendChild(receivedMessage);

        // Scroll to the bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }, 1000);

    // Scroll to the bottom
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Allow sending messages with Enter key
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});