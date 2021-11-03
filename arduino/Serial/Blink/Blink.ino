#include <FastLED.h>
#define NUM_LEDS 244

#define DATA_PIN 11

CRGB leds[NUM_LEDS];
#define BRIGHTNESS 180

void setup()
{
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  pinMode(DATA_PIN, OUTPUT);
  FastLED.setBrightness(BRIGHTNESS);
}
bool toggle = true;
void loop()
{
  for(int i = 0; i < 255; i++){
    leds[i].setRGB(0,0, (((i + toggle) % 2 == 0) ? 255: 0));
  }
  toggle = !toggle;
  delay(500);
  FastLED.show();                    // Refresh leds
}
