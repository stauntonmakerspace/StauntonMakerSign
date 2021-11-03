#include <Wire.h>

void setup() {
  Wire.begin(); // join i2c bus (address optional for master)
}

const int device_cnt = 1;
int led_cnts[device_cnt] = {149};
int tail_pos[2];

void loop() {
  tail_pos[0] = 0;
  tail_pos[1] = 0;
  while (tail_pos[0] < device_cnt){
    // Trim Tail
    Wire.beginTransmission(1); // transmit to device #8
    Wire.write(tail_pos[1]);   // sends one byte
    Wire.write(0);              // sends one byte
    Wire.write(0);              // sends one byte
    Wire.write(0);              // sends one byte
    Wire.endTransmission();  
    // End Trim Tail 
    if (tail_pos[1] >= led_cnts[tail_pos[0]]) {
        tail_pos[0] += 1;
        tail_pos[1] = 0;
       }
    if (tail_pos[0] >= device_cnt){
      break;
      }
       
    for (int i = 1; i <= 9; i++){   
       Wire.beginTransmission(tail_pos[0] + 1); // transmit to device #8
       Wire.write(tail_pos[1] + i);              // sends one byte
       Wire.write((1<=i and i<4)?255:0);              // sends one byte
       Wire.write((4<=i and i<7)?255:0);              // sends one byte
       Wire.write((7<=i)?255:0);              // sends one byte
       Wire.endTransmission();   
    }
    tail_pos[1] += 1;
    Wire.beginTransmission(1); // transmit to device #8
    Wire.write(255);              // sends one byte
    Wire.write(0);              // sends one byte
    Wire.write(255);              // sends one byte
    Wire.write(255);              // sends one byte
    Wire.endTransmission();    
    
   // delay(1/24);
    }
    
    }