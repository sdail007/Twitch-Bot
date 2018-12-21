 window.onload = async () => {
    socket = new ReconnectingWebsocket('ws://192.168.1.5:12345');
    socket.onopen = (event) => {
        Move()
    }
    socket.onmessage = (event) => {
        if(trigger == event.data){
            Move()
        }
    }
}

function Move() {
    var image = document.getElementById("image");
    var x = 0;
    var inc = 0.1;
    var myDude = setInterval(Animate, 1000 / 30);
    function Animate(){
        if(x > 4 * Math.PI) {
            x = 0;
            clearInterval(myDude);
            image.style.bottom = 0 + "px";
        }
        else {
            x += inc;
            inc *= 1.08
            y = Math.sin(x);
            height = Math.abs(60 * y)
            image.style.bottom = height + "px";
        }
    }
}