#include <FastLED.h>
#define NUM_LEDS 10
#define DATA_PIN 3
CRGB leds[NUM_LEDS];
#define BRIGHTNESS 180
#define FRAME_RATE 15
unsigned long last_update;
int device_num;
int led_num;
int r;
int g;
int b;
void setup()
{
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  pinMode(DATA_PIN, OUTPUT);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(9600);
}

byte cmd_buffer[5];
void loop()
{
  // NOTE: Increase buffer size to 256 in HardwareSerial.h
  if (Serial.available() >= 6) // Full Command is in buffer including start byte
  {
    if (Serial.read() == '#') // Check Start Byte
    {
      for (int i = 0; i < 5; i++)
      { // Read Command Array Bytes
        cmd_buffer[i] = Serial.read();
      }
      if (cmd_buffer[0] == 0) // Command has zero hops remaining
      {
        if (cmd_buffer[1] < 0) // Check for screen refresh command
        {
          FastLED.show(); // Refresh led screen
        }
        else
        {
          leds[cmd_buffer[1]].setRGB(cmd_buffer[2], cmd_buffer[3], cmd_buffer[4]);
        }
      }
      else
      {
        Serial.print('#');
        cmd_buffer[0]--; // Decrement hops remaining
        Serial.write(cmd_buffer, 5);
      }
    }
  }
}
