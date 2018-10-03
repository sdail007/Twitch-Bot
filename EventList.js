var container;

window.onload = async () => {
    container = document.getElementById("container");

    AddEvent('Hello World');

    socket = new ReconnectingWebsocket('ws://127.0.0.1:1000');
    socket.onopen = (event) => {

    }
    socket.onmessage = (event) => {
        AddEvent(event.data);
    }
}

function AddEvent(event) {
    var itemsCount = container.childNodes.length;

    if(itemsCount == 3)
    {
        container.removeChild(container.childNodes[0]);
    }

    var node = document.createElement("li");
    node.innerHTML=event;
    container.appendChild(node);
}