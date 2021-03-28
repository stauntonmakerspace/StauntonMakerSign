byte cmd_buffer[6] = {'#', 0, 0, 255, 0, 0};
byte reset_buffer[6] = {'#', 0, 255, 255, 0, 0};
void setup()
{
  // put your setup code here, to run once:
  Serial.begin(500000);
}

#define FRAME_RATE 5
#define DEVICE_CNT 10
int cnts[DEVICE_CNT] = {40, 40, 40, 40, 40, 20, 40, 40, 40, 40};
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
      delay(1);
    }}
      for (int j = DEVICE_CNT - 1; j >= 0; j--){
    reset_buffer[1] = j;
    Serial.write(reset_buffer, 6);
  }
  cmd_buffer[3] = cmd_buffer[3] == 0 ? 255 : 0; // Switch State
  delay((1000 / FRAME_RATE));
}
