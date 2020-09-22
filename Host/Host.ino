String html_1 = R"=====(
<!DOCTYPE html>
<html>

<head>
    <title></title>
    <meta charset='utf-8'>
    <style>
        body {
            margin: 0;
        }

        .cnvs {
            outline: #000000 1px solid;
        }
    </style>

    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
</head>

<body>
    <div id='canvasesdiv' style='position:relative; width:900px; height:500px'>
        <canvas id='paint_layer' style='z-index: 1;
                position:absolute;
                left:0px;
                top:0px;
                ' height='500px' width='900px'>
            This text is displayed if your browser does not support HTML5 Canvas.
        </canvas>
        <canvas id='word_layer' style='z-index: 2;
                position:absolute;
                left:0px;
                top:0px;
                ' height='500px' width='900px'>
            This text is displayed if your browser does not support HTML5 Canvas.
        </canvas>
    </div>

    <div>
        <input type='color' id='color'>
        <button type='button' id='reset'>Reset Canvas</button>
        <input type='submit' id='send'>

        <p>Rerecord Led Layout:</p>
        <table>
            <tr>
                <th>Paint</th>
                <th>M</th>
                <th>a</th>
                <th>k</th>
                <th>e</th>
                <th>r</th>
                <th>S</th>
                <th>P</th>
                <th>A</th>
                <th>C</th>
                <th>e</th>
            </tr>
            <tr>
                <td><input type='radio' name='letter' checked='true' value='Paint'></td>
                <td><input type='radio' name='letter' value=0></td>
                <td><input type='radio' name='letter' value=1></td>
                <td><input type='radio' name='letter' value=2></td>
                <td><input type='radio' name='letter' value=3></td>
                <td><input type='radio' name='letter' value=4></td>
                <td><input type='radio' name='letter' value=5></td>
                <td><input type='radio' name='letter' value=6></td>
                <td><input type='radio' name='letter' value=7></td>
                <td><input type='radio' name='letter' value=8></td>
                <td><input type='radio' name='letter' value=9></td>
            </tr>
        </table>
        <p>Points Remaining:
        <div id='remaining'></div>
        </p>
        <button type='button' id='clear'>Clear Points</button>
    </div>
    <video width="250" id='video' src='https://upload.wikimedia.org/wikipedia/commons/e/e1/Example_of_a_glitch_art_video.ogv'
    controls='false' crossorigin='anonymous'></video>

    <iframe src="https://giphy.com/embed/la3211WGwbYYw" width="480" height="309" frameBorder="0" class="giphy-embed"
        allowFullScreen></iframe>

    <script>
        // Main Function 
        (function (w, d) {
            'use strict';

            var action = 'up',
                canvas = d.querySelector('#paint_layer'),
                paint_ctx = canvas.getContext('2d'),
                words = d.querySelector('#word_layer'),
                words_ctx = words.getContext('2d'),
                color = d.querySelector('#color'),
                record = d.querySelector('#record'),
                body = d.querySelector('body'),
                offset = 1000,
                points = [],
                bufer = paint_ctx.getImageData(0, 0, canvas.width, canvas.height),
                radio_selection = 'Paint',
                led_counts = { 0: 151, 1: 57, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10 },
                control_points = { 0: [[0, 0]], 1: [[0, 0]], 2: [[0, 0]], 3: [[0, 0]], 4: [[0, 0]], 5: [[0, 0]], 6: [[0, 0]], 7: [[0, 0]], 8: [[0, 0]], 9: [[0, 0]] },
                point_history = {};

            // Setup initial text borders 
            words_ctx.lineWidth = 3;
            words_ctx.strokeStyle = 'black';
            words_ctx.font = ' 150px Arial';
            words_ctx.strokeText('MakerSPACe', 0, 250);

            var video = document.getElementById('video');
            video.addEventListener('play', function () {
                var $this = this; //cache
                (function loop() {
                    if (!$this.paused && !$this.ended) {
                        //Resize Video
                        var hRatio = (canvas.width / video.videoWidth) * video.videoHeight;
                        paint_ctx.drawImage($this, 0, 0, canvas.width, hRatio);
                        setTimeout(loop, 1000 / 30); // drawing at 30fps
                    }
                })();
            });
            // Generate Arduino Requests
            var connection = new WebSocket('ws://' + w.location.hostname + ':81/', ['arduino']);
            connection.onopen = function () {
                connection.send('Connect ' + new Date());
            };
            connection.onerror = function (error) {
                console.log('WebSocket Error ', error);
            };
            connection.onmessage = function (e) {
                console.log('Server: ', e.data);
            };
            connection.onclose = function () {
                console.log('WebSocket connection closed');
            };

            function samplePoint(x, y) {
                var img_data = paint_ctx.getImageData(x, y, 1, 1).data;
                var R = img_data[0];
                var G = img_data[1];
                var B = img_data[2];
                return [R, G, B];
            }
            function sampleCapturePoints() {
                for (const [device_num, points] of Object.entries(control_points)) {
                    for (const [index, point] of Object.entries(points)) {
                        var rgb = samplePoint(point[0], point[1]);
                        var led_ind = device_num.toString() + index.toString().padStart(3, "0");
                        var cmd = rgb[0].toString().padStart(3, "0") + rgb[1].toString().padStart(3, "0") + rgb[2].toString().padStart(3, "0");
                        if (point_history[led_ind] != cmd) {
                            if (connection.readyState === WebSocket.OPEN) {
                                connection.send(led_ind+cmd);
                            } else {
                                console.log(led_ind+cmd);
                            }
                            point_history[led_ind] = cmd;
                        }
                    }
                }
            }
            function setCapturePoints() {
                control_points[radio_selection] = points;
                points = [];
            }
            function resetCanvas() {
                paint_ctx.clearRect(0, 0, canvas.width, canvas.height);
                paint_ctx.lineWidth = 15;
                paint_ctx.shadowColor = '#000000';
                paint_ctx.shadowBlur = 20;
                paint_ctx.shadowOffsetX = -offset;
                bufer = paint_ctx.getImageData(0, 0, canvas.width, canvas.height);
            }
            function runCanvas() {
                if (points.length > 0) {
                    if (radio_selection == 'Paint') { // Painting 
                        paint_ctx.beginPath();
                        paint_ctx.moveTo(points[0][0] + offset, points[0][1]);
                        for (var i = 1; i < points.length; i++) {
                            paint_ctx.lineTo(points[i][0] + offset, points[i][1]);
                        }
                    } else {
                        paint_ctx.beginPath();
                        for (var i = 1; i < points.length; i++) {
                            paint_ctx.rect(points[i][0] + offset, points[i][1], 3, 3);
                        }
                    }
                }
                sampleCapturePoints();
                setTimeout(runCanvas, 1000 / 24); // drawing at 24fps
            }
            d.getElementById('reset').onclick = resetCanvas;
            body.addEventListener('mouseup', function () {
                action = 'up';
                if (radio_selection === 'Paint') { // Painting 
                    points = [];
                    bufer = paint_ctx.getImageData(0, 0, canvas.width, canvas.height);
                } else {
                    if (points.length === led_counts[radio_selection]) {
                        setCapturePoints();
                    }
                }
            });
            body.addEventListener('mousedown', function (e) {
                action = 'down';
                points.push([e.pageX, e.pageY]);
            });
            body.addEventListener('mousemove', function (e) {
                if (action === 'down') {
                    paint_ctx.putImageData(bufer, 0, 0); // Redraw Previous Frame 
                    if (radio_selection == 'Paint') {
                        points.push([e.pageX, e.pageY]);
                    } else {
                        if (points.length < led_counts[radio_selection]) {
                            if (Math.sqrt((e.pageX - points[points.length - 1][0]) ** 2 + (e.pageY - points[points.length - 1][1]) ** 2) > 2.3) {
                                points.push([e.pageX, e.pageY]);
                            }
                        }
                    }
                    paint_ctx.stroke();
                }
            });
            $('input[type=radio][name=letter]').change(function () {
                points = [];
                paint_ctx.putImageData(bufer, 0, 0); // Clear Marks 

                if (this.value === 'Paint') {
                    paint_ctx.restore(); // Restore Paint Settings  
                } else {
                    if (radio_selection == 'Paint') {
                        paint_ctx.save();
                    }
                    paint_ctx.lineWidth = 2;
                    paint_ctx.shadowBlur = 1;
                    paint_ctx.shadowColor = '000000'
                    for (const [index, point] of Object.entries(control_points[this.value])) {
                        paint_ctx.strokeRect(point[0] + offset, point[1], 5, 5);
                    }
                } radio_selection = this.value;
            });
            color.addEventListener('change', function (e) {
                paint_ctx.shadowColor = e.target.value;
            });

            resetCanvas();
            runCanvas();
        }(window, document));

    </script>

</body>

</html>
)=====";
 
#include <ESP8266WiFi.h>
#include <WebSocketsServer.h>
 
WiFiServer server(80);
WebSocketsServer webSocket = WebSocketsServer(81);
 
String header = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: text/html\r\n\r\n";
 
 
char ssid[] = "StauntonMakerspace";  // use your own network ssid and password
char pass[] = "hackstaunton";

void webSocketEvent(byte num, WStype_t type, uint8_t * payload, size_t length);
void setup()
{
  Serial.begin(9600);
  Serial.println();
  Serial.println("Serial started at 115200");
  Serial.println();
 
  // Connect to a WiFi network
  Serial.print(F("Connecting to "));  Serial.println(ssid);
  WiFi.begin(ssid,pass);
 
  // connection with timeout
  int count = 0; 
  while ( (WiFi.status() != WL_CONNECTED) && count < 17) 
  {
      Serial.print(".");  delay(500);  count++;
  }
 
  if (WiFi.status() != WL_CONNECTED)
  { 
     Serial.println("");  Serial.print("Failed to connect to ");  Serial.println(ssid);
     while(1);
  }
 
  Serial.println("");
  Serial.println(F("[CONNECTED]"));   Serial.print("[IP ");  Serial.print(WiFi.localIP()); 
  Serial.println("]");
 
  // start a server
  server.begin();
  Serial.println("Server started");
 
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}
 
void loop()
{
    webSocket.loop();
 
    WiFiClient client = server.available();     // Check if a client has connected
    if (!client)  {  return;  }
 
    client.flush();
    client.print( header );
    client.print( html_1 ); 
    Serial.println("New page served");
 
    delay(5);
}

void webSocketEvent(byte num, WStype_t type, uint8_t * payload, size_t length)
{
  
  if(type == WStype_TEXT)
  {
        Serial.print('#');
        Serial.print((char *)payload); 
  }
  else 
  {
    Serial.print("WStype = ");   Serial.println(type);  
    Serial.print("WS payload = ");
    for(int i = 0; i < length; i++) { Serial.print((char) payload[i]); }
    Serial.println();
 
  }
}
