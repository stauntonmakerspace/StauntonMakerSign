#include<FastLED.h>
byte cmd_buffer[6] = {'#', 0, 0, 255, 0, 0};
byte reset_buffer[6] = {'#', 0, 255, 255, 0, 0};
void setup()
{
  // put your setup code here, to run once:
  Serial.begin(500000);
}

#define FRAME_RATE 100
#define DEVICE_CNT 4
int cnts[DEVICE_CNT] = {151, 57, 84, 43};
CRGB rgb;

int l;
int hue = 0;
void loop()
{
  // put your main code here, to run repeatedly:
  l = 0;
  hue = hue > 255 ? 0 : hue + 1;
  for (int j = DEVICE_CNT - 1; j >= 0; j--)
  {
    cmd_buffer[1] = j;
    for (int i = 0; i < cnts[j]; i++)
    { // NOTE: Adapt
      CHSV hsv(l++ % 255 - (hue * 2), 255, 255); /* The higher the value 4 the less fade there is and vice versa */
      
      hsv2rgb_rainbow(hsv, rgb);
      cmd_buffer[2] = i;
      cmd_buffer[3] = rgb.r;
      cmd_buffer[4] = rgb.g;
      cmd_buffer[5] = rgb.b;
      Serial.write(cmd_buffer, 6);
    }
  }
  for (int j = DEVICE_CNT - 1; j >= 0; j--) {
    reset_buffer[1] = j;
    Serial.write(reset_buffer, 6);
  }
  delay((1000 / FRAME_RATE));
}