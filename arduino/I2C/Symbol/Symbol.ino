#include <FastLED.h>
#include <Wire.h>

#define NUM_LEDS 244

#define DATA_PIN 11
#define CMD_LENGTH 4

byte cmd_buffer[CMD_LENGTH];

CRGB leds[NUM_LEDS];
#define BRIGHTNESS 180

byte get_address()
{
    byte address_buffer = 0;
    pinMode(9, OUTPUT);
    digitalWrite(9, HIGH);
    // Read the 7 bit address
    for (int i = 6; i >= 0; i--)
    {
        int pin = 2 + i;
        pinMode(pin, INPUT);
        delay(200);
        Serial.print((digitalRead(pin) == HIGH));
        
        address_buffer = address_buffer | ((digitalRead(pin) == HIGH) << 6 - i);
    }
    Serial.println("0");
    
    Serial.print("Address: ");
    Serial.println(address_buffer);
    digitalWrite(10, LOW);
    return address_buffer;
}

void receiveEvent(int bytes)
{
    if (bytes == 4) // Led Num R,G,B TODO: Use HSV
    {
        for (int i = 0; i < 4; i++)
        {
            cmd_buffer[i] = Wire.read();
        }
        if (cmd_buffer[0] == 255) // Check for screen refresh command
        {
            FastLED.show(); // Refresh leds
        }
        else
        {
            leds[cmd_buffer[0]].setRGB(cmd_buffer[1], cmd_buffer[2], cmd_buffer[3]);
        }
    }
}
byte address = 0;
void setup()
{
    FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
    pinMode(DATA_PIN, OUTPUT);
    // TODO Join i2c with get_address

    Wire.begin(1);                // join i2c bus with address #4
    Wire.onReceive(receiveEvent); // register event
    FastLED.setBrightness(BRIGHTNESS);
}

void loop()
{
    delay(100);
}
