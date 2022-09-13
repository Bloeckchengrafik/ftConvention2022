term = $("#term").terminal()

term.clear()

term.echo(`
▄▄▄▄▄▄▄▄▄▄▄             
███████████      
██████████████████████████████████████████████████████████████████████    |
██▌                                                                ▐██    |
██▌      ██████████████                                            ▐██    |         Welcome to the Sorter Shell
██▌      ███        ███                                            ▐██    |
██▌      ██████████████                                            ▐██    |                  v1.0.0
██▌                                                                ▐██    |
██▌                                                                ▐██    |
██▌                     ▄█▄▄                                       ▐██    |
██▌                      ▀████▄                                    ▐██    |       You'll be notified here for most events
██▌                         ▀▀████▄                                ▐██    |
██▌                            ▄████▌                              ▐██    |
██▌                         ▄████▀▀                                ▐██    |
██▌                      ▄███▀▀     ▄▄▄▄▄▄▄▄▄▄                     ▐██    |
██▌                      ▀▀         ▀▀▀▀▀▀▀▀▀▀                     ▐██    |
██▌                                                                ▐██    |
██▌                                                                ▐██    |
██▌                                                                ▐██    |
██████████████████████████████████████████████████████████████████████    |

`)

const cam = new Webcam(document.getElementById("cam"), 'element', document.getElementById("can"))
cam.start()

function connect() {
    var ws = new WebSocket('ws://localhost:8000');
    ws.onopen = function () {
        term.echo("Connected to Websocket Server") 
    };

    ws.onmessage = function (e) {
        term.echo('Message:' + e.data);

        if (e.data == "pls img\n") {
            term.echo("Taking image...")
            sn = cam.snap()
            ws.send(sn)
            
        }
    };

    ws.onclose = function (e) {
        term.echo('Socket is closed. Reconnect will be attempted in 1 second: ' +  e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };

    ws.onerror = function (err) {
        term.echo('Socket encountered error: ' + err.message + ' Closing socket');
        ws.close();
    };
}

connect();
