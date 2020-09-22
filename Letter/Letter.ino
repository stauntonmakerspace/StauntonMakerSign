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
  last_update = millis();
}

int parseIntFast(int numberOfDigits)
{
  /*
  This function returns the converted integral number as an int value.
  If no valid conversion could be performed, it returns zero.*/
  char theNumberString[numberOfDigits + 1];
  int theNumber;
  for (int i = 0; i < numberOfDigits; theNumberString[i++] = Serial.read())
  {
    delay(5);
  };
  theNumberString[numberOfDigits] = 0x00;
  theNumber = atoi(theNumberString);
  return theNumber;
}

void loop()
{
  while (Serial.available() > 0)
  {
    if (Serial.read() == '#')
    {
      device_num = parseIntFast(1);
      if (device_num == 0)
      {
        led_num = parseIntFast(3);
        r = parseIntFast(3);
        g = parseIntFast(3);
        b = parseIntFast(3);
        leds[led_num].setRGB(r, g, b);
      }
      else
      {
        Serial.print("#");
        Serial.print(device_num - 1);
        for (int i = 0; i < 12; i++)
        {
          Serial.print(Serial.read());
          delay(5);
        }
      }
    }
  }
  if ((millis() - last_update) > 1000 / FRAME_RATE)
  {
    FastLED.show();
    last_update = millis();
  }
}
