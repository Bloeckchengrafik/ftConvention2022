#include <Arduino.h>
#include <ftSwarm.h>
#include <FastLED.h>

enum Trilean_t
{
    True,
    False,
    Maybe
};

enum SwarmTypeElement_t
{
    Digital
};

struct Node_t
{
    char *name;
    SwarmTypeElement_t type;
    FtSwarmSwitch *asSwitch;
    Trilean_t asSwitchState;

    Node_t *next;
};

FtSwarmSerialNumber_t fullSwarm[20];
FtSwarmSerialNumber_t *ctx;

Node_t head;
Node_t tail;
bool has_list_elems = false;

Trilean_t fromBool(bool in)
{
    if (in)
        return Trilean_t::True;
    else
        return Trilean_t::False;
}

int timedRead()
{
    int c;
    long _startMillis = millis();
    do {
        c = Serial.read();
        if(c >= 0) {
            return c;
        }
    } while(millis() - _startMillis < 3);
    return -1;     // -1 indicates timeout
}

void setup()
{
    Serial.begin(115200);

    fullSwarm[0] = ftSwarm.begin();
    ctx = &fullSwarm[0];

    Serial.println(F(">>>"));
}

void loop()
{
    if (Serial.available())
    {

        String command;
        int c = timedRead();
        while (c >= 0)
        {
            command += (char)c;
            c = timedRead();
        }

        command.replace("\r", "");
        command.replace("\n", "");

        if (command.equalsIgnoreCase("sub"))
        {
            Serial.println("#error Inputs are not implemented");
        }
        else if (command.equalsIgnoreCase("mot"))
        {
            Serial.println("#error Motors are not implemented");
        }
        else if (command.equalsIgnoreCase("led"))
        {
            Serial.println("#error LEDs are currently not implemented");
        }
        else if (command.equalsIgnoreCase("srv"))
        {
            Serial.println("#error Servos are not implemented");
        }
    }
}
