// Flash RGB 

byte cmd_buffer[6] = {'#', 0, 0, 255, 0, 0};
byte reset_buffer[6] = {'#', 0, 255, 255, 0, 0};
void setup()
{
  // put your setup code here, to run once:
  Serial.begin(500000);
}

// #define FRAME_RATE 24
#define DEVICE_CNT 10
int cnts[DEVICE_CNT] = {244, 244, 244, 244, 244, 244, 244, 244, 244, 244};
void loop()
{
  // put your main code here, to run repeatedly:
  for (int j = DEVICE_CNT - 1; j >= 0; j--)
  {
    cmd_buffer[1] = j;
    for (int i = 0; i < cnts[j]; i++)
    {
      cmd_buffer[2] = i;
      Serial.write(cmd_buffer, 6);
      delayMicroseconds(50);
    }}
      for (int j = DEVICE_CNT - 1; j >= 0; j--){
    reset_buffer[1] = j;
    Serial.write(reset_buffer, 6);
  }
  if (cmd_buffer[5] == 255){
    cmd_buffer[3] = 255;
    cmd_buffer[4] = 0;
    cmd_buffer[5] = 0;
   } else if (cmd_buffer[3] == 255){
    cmd_buffer[3] = 0;
    cmd_buffer[4] = 255;
    cmd_buffer[5] = 0;
   } else if (cmd_buffer[4] == 255){
    cmd_buffer[3] = 0;
    cmd_buffer[4] = 0;
    cmd_buffer[5] = 255;
   } 
  //delay((1000 / FRAME_RATE));
}
