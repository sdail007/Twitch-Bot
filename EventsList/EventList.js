var container;

window.onload = async () => {
    container = document.getElementById("container");

    socket = new ReconnectingWebsocket('ws://127.0.0.1:1000');
    socket.onopen = (event) => {

    }
    socket.onmessage = (event) => {
        AddEvent(event.data);
    }
}

function AddEvent(event) {
    console.log(event);
    e = JSON.parse(event)
    var itemsCount = container.childNodes.length;

    if(itemsCount == 3)
    {
        container.removeChild(container.childNodes[0]);
    }

    var node = document.createElement("li");
    node.innerHTML= `${e.EventText} (${e.ValueChange > 0 ? "+" : "-"}${e.ValueChange})`;
    container.appendChild(node);
}