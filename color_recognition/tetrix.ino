#include <PULSE.h>
PULSE pulse;


//***************************
void move(int a, int b) {
  move(a, b, 0);
}
void move(int a, int b, int del) {
  if (a == 0 && b == 0)
    pulse.setServoPosition(1, 90);
  else if (a < 0 && b < 0)
    pulse.setServoPosition(1, 45 + atan2( -b, -a) * (180 / PI));
  else
    pulse.setServoPosition(1, 45 + atan2(a, b) * (180 / PI));
  pulse.setMotorPower(1, a);
  pulse.setMotorPower(2, -b);
  delay(del);
}
//***************************



void setup() {
  pulse.PulseBegin();
  pulse.setServoSpeed(1, 100);
  Serial.begin(115200);
}


void loop() {
  char buffer[100];
  String inStr, comm;
  while (Serial.available() == 0) {
  }
  inStr = Serial.readString();
  inStr.toCharArray(buffer, 100);
  comm = strtok(buffer, " ");
  Serial.println(comm);

  if (comm == "move") {
    String speed1, speed2, del;
    speed1 = strtok(NULL, " ");
    speed2 = strtok(NULL, " ");
    del = strtok(NULL, " ");
    Serial.println(speed1);
    Serial.println(speed2);
    Serial.println(del);
    move(speed1.toInt(), speed2.toInt(), del.toInt());
  }
  
  delay(500);
  move(0, 0);

}
