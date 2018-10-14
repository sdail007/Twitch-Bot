var label

window.onload = async () => {
    label = document.getElementById("balance");

    socket = new ReconnectingWebsocket('ws://127.0.0.1:1112');

    socket.onopen = (event) => {

    }
    socket.onmessage = (event) => {
        e = JSON.parse(event.data)
        label.innerHTML= `Current Balance: ${e.balance}`;
    }
}