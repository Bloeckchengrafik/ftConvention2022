#include <Arduino.h>
#include <ftSwarm.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <FastLED.h>

AsyncWebServer server(81);
AsyncWebSocket ws("/ws");

FtSwarmMotor *disc;

void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len)
{
    switch (type)
    {
    case WS_EVT_CONNECT:
        Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
        break;
    case WS_EVT_DISCONNECT:
        Serial.printf("WebSocket client #%u disconnected\n", client->id());
        break;
    case WS_EVT_DATA:
        Serial.printf("WebSocket client sent message\n");
        break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
        break;
    }
}

void setup()
{
  Serial.begin(115200);

  FtSwarmSerialNumber_t local = ftSwarm.begin();

  disc = new FtSwarmMotor(local, FTSWARM_M2);

  ws.onEvent(onEvent);
  server.addHandler(&ws);
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            { request->send(404); });

  server.begin();
}

void loop()
{
  ws.cleanupClients();
  delay(1000);
}
