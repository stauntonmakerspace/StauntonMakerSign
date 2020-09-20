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

String cmd;
void SetColor(String incoming) //incoming looks like this -> Q:0x00FF00
{
  String colorString = incoming.substring(2); // remove Q:
  long color = strtol(colorString.c_str(), NULL, 16);

  leds[0] = color;
  leds[15] = color;
}

char* string2char(String command){
    if(command.length()!=0){
        char *p = const_cast<char*>(command.c_str());
        return p;
    }
}

void loop()
{
  while (Serial.available() > 0)
  {
    cmd = Serial.readString();
    if (cmd[0] == "0")
    {
      int i = 0;
      int data[5]; // led_num, r,g,b
      char *p = string2char(Serial.readStringUntil(";"));
      
      char *str;
      while ((str = strtok_r(p, ",", &p)) != NULL) data[i++] = atoi(str);
      
      leds[data[0]].setRGB(data[1],data[2],data[3]);
      FastLED.show();
    }
    else
    {
      // Decrement and Pass it on
      //Serial.printf("%d%s:",atoi(device_num) - 1  + Serial.readStringUntil(":")));
    }
  }
}