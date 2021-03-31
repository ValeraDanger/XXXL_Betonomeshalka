#include <PULSE.h>
PULSE pulse;

void setup() {
  Serial.begin(115200);
  pulse.PulseBegin();
  pulse.setServoSpeed(1, 100);
  Serial.println("isStart");
}

enum T {
  waitingComand1,  //1
  waitingNum1,     //2
  waitingNum2,     //4
  waitingNum3
};


int sost = waitingComand1;

void move(int a, int b) {
  if (a == 0 && b == 0)
    pulse.setServoPosition(1, 90);
  else if (a < 0 && b < 0)
    pulse.setServoPosition(1, 45 + atan2( -b, -a) * (180 / PI));
  else
    pulse.setServoPosition(1, 45 + atan2(a, b) * (180 / PI));
  pulse.setMotorPower(1, a);
  pulse.setMotorPower(2, -b);
}

void myStop() {
  move(0, 0);
  Serial.println("Stoped");
}

int seedA = 0;
int seedB = 0;
int del = 0;

int notFlagA = 1;
int notFlagB = 1;



unsigned long timer = 0;

bool flag = false;
bool oldFlag = false;

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '#')
      myStop();
    switch (sost) {
      case waitingComand1:
        if (c == 'A') {
          sost = waitingNum1;
          seedA = 0;
        }
        break;
      case waitingNum1:
        if ((c >= '0') && (c <= '9'))
          seedA = seedA * 10 + (c - '0');
        else if (c == '-')
          notFlagA = -1;
        else if (c == 'B') {
          sost = waitingNum2;
          seedB = 0;
        }
        break;

      case waitingNum2:
        if ((c >= '0') && (c <= '9'))
          seedB = seedB * 10 + (c - '0');
        else if (c == '-')
          notFlagB = -1;
        else if (c == 'D') {
          sost = waitingNum3;
          del = 0;
        }
        else
          sost = waitingComand1;
        break;
      case waitingNum3:
        if ((c >= '0') && (c <= '9'))
          del = del * 10 + (c - '0');
        else if (c == 'A') {
          sost = waitingNum1;
          seedB = 0;
        }
        else {
          sost = waitingComand1;
          timer = millis();
          flag = true;
          oldFlag = true;
          move(seedA * notFlagA, seedB * notFlagB);
          /*
                    Serial.print('A');
                    Serial.print(seedA);
                    Serial.print('B');
                    Serial.print(seedB);
                    Serial.print('D');
                    Serial.println(del);
          */
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
