#include <PULSE.h>
PULSE pulse;

void setup() {
  Serial.begin(115200);
  pulse.PulseBegin();
  pulse.setServoSpeed(1, 100);
  Serial.println("isStart");
  pulse.setServoPosition(1, 87);
  move(100, 100);
}

enum T {
  waitingComand1,  //1
  waitingSpeed1,     //2
  waitingSpeed2,     //4
  waitingDel
};


int sost = waitingComand1;

void move(int a, int b) {
  if (a == 0 && b == 0)
    pulse.setServoPosition(1, 87);
  else if ((a < 0 ) && ( b < 0))
    pulse.setServoPosition(1, (41.9 + atan2(-a, -b) * (180 / PI)));
  else
    pulse.setServoPosition(1, (41.9 + atan2(a, b) * (180 / PI)));
  pulse.setMotorPower(1, a);
  pulse.setMotorPower(2, -b);
}

void myStop() {
  move(0, 0);
  Serial.println("Stoped");
}

int speedA = 0;
int speedB = 0;
int del = 0;

int notFlagA = 1;
int notFlagB = 1;



unsigned long timer = 0;

bool flag = false;
bool oldFlag = false;

/*
  A - скорость первого мотора
  B - скорость второго мотора
  D - время работы моторов
*/

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '#')
      myStop();
    switch (sost) {
      case waitingComand1:
        if (c == 'A') {
          sost = waitingSpeed1;
          speedA = 0;
        }
        break;
      case waitingSpeed1:
        if ((c >= '0') && (c <= '9'))
          speedA = speedA * 10 + (c - '0');
        else if (c == '-')
          notFlagA = -1;
        else if (c == 'B') {
          sost = waitingSpeed2;
          speedB = 0;
        }
        break;

      case waitingSpeed2:
        if ((c >= '0') && (c <= '9'))
          speedB = speedB * 10 + (c - '0');
        else if (c == '-')
          notFlagB = -1;
        else if (c == 'D') {
          sost = waitingDel;
          del = 0;
        }
        else
          sost = waitingComand1;
        break;
      case waitingDel:
        if ((c >= '0') && (c <= '9'))
          del = del * 10 + (c - '0');
        else if (c == 'A') {
          sost = waitingComand1;
          speedA = 0;
        }
        else {
          sost = waitingComand1;
          timer = millis();
          flag = true;
          oldFlag = true;
          move(speedA * notFlagA, speedB * notFlagB);

          Serial.print('A');
          Serial.print(speedA * notFlagA);
          Serial.print('B');
          Serial.print(speedB * notFlagB);
          Serial.print('D');
          Serial.println(del);

          notFlagA = 1;
          notFlagB = 1;
        }

        break;
    }
  }


  if (sost == waitingComand1)
    if (timer + del > millis()) {

    } else {
      flag = false;
    }

  if (!flag && oldFlag) {
    Serial.println("OK");
    oldFlag = flag;
    move(0, 0);
  }
}



/*char c = Serial.read();*/
