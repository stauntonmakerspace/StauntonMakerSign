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
// https://stackoverflow.com/questions/9072320/split-string-into-string-array
String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
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
    cmd = Serial.readStringUntil(';');
    if (cmd[0] == '0')
    {
      
      leds[getValue(cmd,',',1).toInt()].setRGB(getValue(cmd,',',2).toInt(),getValue(cmd,',',3).toInt(),getValue(cmd,',',4).toInt());
      FastLED.show();
    }
    else
    {
      // Decrement and Pass it on
      cmd[0]--;
      Serial.print(cmd);
    }
  }
}
