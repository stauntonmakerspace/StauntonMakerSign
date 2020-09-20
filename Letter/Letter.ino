#include <FastLED.h>
#define NUM_LEDS 10
#define DATA_PIN 12
CRGB leds[NUM_LEDS];
#define BRIGHTNESS 180

void setup()
{
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  pinMode(DATA_PIN, OUTPUT);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(9600);
}

void loop()
{
  while (Serial.available() > 0)
  {
    byte device_num = Serial.read();
    if (device_num == "0")
    {
      int i = 0;
      int data[4]; // led_num, r,g,b
      char *p = (char *)payload;
      char *str;
      while ((str = strtok_r(p, ",", &p)) != NULL)
      {
        data[i++] = atoi(str);
      }
      leds[data[0]].setRGB(data[1],data[2],data[3]);
      FastLED.show();
    }
    else
    {
      // Decrement and Pass it on
      Serial.printf("%d%s:",atoi(device_num) - 1  + Serial.readStringUntil(":")));
    }
  }
}
