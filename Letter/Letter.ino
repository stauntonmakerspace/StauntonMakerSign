#include <FastLED.h>
#define NUM_LEDS 84

#define TX_BUFFER_SIZE 32 // * 5 bytes
unsigned int cmds_buffered = 0;

#define READY2RECIEVE 8
#define RECEIVER_READY 8
#define DATA_PIN 3

CRGB leds[NUM_LEDS];
#define BRIGHTNESS 180

void setup()
{
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);

  pinMode(DATA_PIN, OUTPUT);
  pinMode(RECEIVER_READY, INPUT);
  pinMode(READY2RECIEVE, OUTPUT);

  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(115200);
}

byte waiting_cmd_buffer[TX_BUFFER_SIZE][5]
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
        if (cmd_buffer[1] == 255) // Check for screen refresh command
        {
          digitalWrite(READY2RECIEVE, HIGH); // Not ready to recieve data 
          FastLED.show(); // Refresh leds
          digitalWrite(READY2RECIEVE, LOW);
        }
        else
        {
          leds[cmd_buffer[1]].setRGB(cmd_buffer[2], cmd_buffer[3], cmd_buffer[4]);
        }
      }
      else
      {
        if (digitalRead(RECEIVER_READY) == LOW) {
          // Empty Buffered Commands
          while (cmds_buffered > 0) {
            Serial.print('#');
            Serial.write(waiting_cmd_buffer[--cmds_buffered], 5);
          }
          Serial.print('#'); // Send Start Byte
          cmd_buffer[0]--; // Decrement hops remaining
          Serial.write(cmd_buffer, 5);
        } else {
          if (cmds_buffered < TX_BUFFER_SIZE){
          waiting_cmd_buffer[cmds_buffered++] = cmd_buffer;
          }
        }
      }
    }
  }
}
