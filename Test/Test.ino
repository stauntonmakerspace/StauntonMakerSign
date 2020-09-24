byte cmd_buffer[6] = {'#', 0, 0, 255, 0, 255};
byte cmd_buffer2[6] = {'#', 0, 0, 0, 0, 0};
byte reset_buffer[6] = {'#', 0, 255, 255, 0, 0};
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

#define FRAME_RATE 20
int cnts[4] = {151,57, 84, 43};
void loop() {
  // put your main code here, to run repeatedly:
  for (int j = 0; j < 4; j++) {
    cmd_buffer[1] = j;
    for (int i = 0; i < cnts[j]; i++) {
      cmd_buffer[2] = i;
      Serial.write(cmd_buffer, 6);
    }
  }
  for (int j = 0; j < 4; j++) {
    reset_buffer[1] = j;
    Serial.write(reset_buffer, 6);
    delay(20);
  }

  delay((1000 / FRAME_RATE) / 2);
  for (int j = 0; j < 4; j++) {
    cmd_buffer2[1] = j;
    for (int i = 0; i < cnts[j]; i++) {
      cmd_buffer2[2] = i;
      Serial.write(cmd_buffer2, 6);
    }
  }
  for (int j = 0; j < 4; j++) {
    reset_buffer[1] = j;
    Serial.write(reset_buffer, 6);
    delay(20);
  }

  delay((1000 / FRAME_RATE) / 2);
} 
