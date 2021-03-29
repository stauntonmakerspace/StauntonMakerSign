#include <FastLED.h>
#define NUM_LEDS 151

#define DATA_PIN 3

CRGB leds[NUM_LEDS];
#define BRIGHTNESS 180

byte cmd_buffer[5];
void setup()
{
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);

  pinMode(DATA_PIN, OUTPUT);

  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(500000);
}

void loop()
{
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
        if (cmd_buffer[1] == 255) // Check for screen refresh command
        {
          FastLED.show();                    // Refresh leds
        }
        else
        {
          leds[cmd_buffer[1]].setRGB(cmd_buffer[2], cmd_buffer[3], cmd_buffer[4]);
        }
      }
      else
      {
        Serial.print('#'); // Send Start Byte
        cmd_buffer[0]--;   // Decrement hops remaining
        Serial.write(cmd_buffer, 5);
        // delayMicroseconds(50);
      }
    }
  }
}
