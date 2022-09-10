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
    Digital,
    Motor
};

class Node
{
public:
    String name;
    SwarmTypeElement_t type;

    FtSwarmSwitch *asSwitch;
    Trilean_t asSwitchState;

    FtSwarmMotor *asMotor;

    Node *next;
    bool has_next;
};

FtSwarmSerialNumber_t fullSwarm[20];
FtSwarmSerialNumber_t *ctx;

Node *head;
Node *tail;
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
    do
    {
        c = Serial.read();
        if (c >= 0)
        {
            return c;
        }
    } while (millis() - _startMillis < 3);
    return -1; // -1 indicates timeout
}

void appendNode(Node *node)
{
    if (!has_list_elems)
    {
        head = node;
        has_list_elems = true;
        tail = node;

        Serial.printf("#warn %s\r\n", head->name);

        return;
    }

    tail->next = node;
    tail = node;
}

void printNodes()
{
    if (!has_list_elems)
    {
        Serial.println("#debug nodes = []");
        return;
    }

    Serial.println("#debug nodes = [");

    Node *current = head;

    while (1)
    {
        Serial.printf("#debug '%s',\r\n", current->name);

        if (!current->has_next) break;

        current = current->next;
    };
    
    Serial.println("#debug ]");
}

bool containsNode(const char *name)
{
    if (!has_list_elems)
        return false;

    Node *current = head;


    while (1)
    {
        if (current->name.equals(name))
        {
            return true;
        }

        if (!current->has_next) break;

        current = current->next;
    }
    return false;
}

Node *getNode(const char *name)
{
    if (!has_list_elems)
        return NULL;

    Node *current = head;


    while (1)
    {
        if (current->name.equals(name))
        {
            return current;
        }

        if (!current->has_next) break;

        current = current->next;
    }
    return NULL;
}

void doDigital(Node *node) {
    Trilean_t actual = fromBool(node->asSwitch->getState());
    
    if (actual == node->asSwitchState) return;

    Serial.printf("!%s %d\r\n", node->name, node->asSwitch->getState());
    node->asSwitchState = actual;
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
    // Work on Commands by the Controller
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

        String args = command.substring(command.indexOf(" "));

        if (command.startsWith("sub"))
        {
            command = command.substring(4);

            if (command.startsWith("digital"))
            {
                command = command.substring(8);

                if (containsNode(command.c_str()))
                {
                    Serial.printf("#info Already Subscribed to Button Press on %s\r\n", command);
                    Serial.println("neu sub");
                    return;
                }

                Node *node = new Node();

                char cached_name[100];
                strcpy(cached_name, command.c_str());

                node->name = command;
                node->type = SwarmTypeElement_t::Digital;
                node->asSwitch = new FtSwarmSwitch(cached_name);
                node->asSwitchState = Maybe;
                node->has_next = false;

                appendNode(node);

                Serial.printf("#debug Subscribed to Button Press on %s\r\n", command);
                Serial.println("suc sub");
                return;
            }

            Serial.println("err sub");
        }
        else if (command.startsWith("mot"))
        {
            
            command = command.substring(4);

            int index = command.indexOf(" ");
            String value = command.substring(index+1);
            command = command.substring(0, index);


            Node *node;

            if (!containsNode(command.c_str())){
                node = new Node();

                char cached_name[100];
                strcpy(cached_name, command.c_str());

                node->name = command;
                node->type = SwarmTypeElement_t::Motor;
                node->asMotor = new FtSwarmMotor(cached_name);
                node->has_next = false;

                appendNode(node);
            } else {
                node = getNode(command.c_str());
            }

            node->asMotor->setSpeed(value.toInt());
            Serial.println("suc mot");
        }
        else if (command.startsWith("led"))
        {
            Serial.println("#error LEDs are currently not implemented");
            Serial.println("err led");
        }
        else if (command.startsWith("srv"))
        {
            Serial.println("#error Servos are not implemented");
            Serial.println("err srv");
        }
        else if (command.startsWith("nod"))
        {
            printNodes();
            Serial.println("suc nod");
        }
    }

    // Input Loop

    if (!has_list_elems) return;

    Node *current = head;

    while (1)
    {
        switch (current->type) {
            case Digital:
                doDigital(current);
                break;
        }

        if (!current->has_next) break;

        current = current->next;
    }
}
