import serial
import time

ser = serial.Serial(port='COM9', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)

'''
    A - скорость первого мотора
    B - скорость второго мотора
    D - время работы моторов
'''

print(ser.readline())
print('-----------------')
ser.write(b'A-100B0D2000\n')
print(ser.readline())
ser.write(b'A100B100D2000\n')
print(ser.readline())
ser.write(b'A-100B100D2000\n')
print(ser.readline())
ser.write(b'A50B0D2000\n')
print(ser.readline())
ser.write(b'A-50B0D2000\n')
print(ser.readline())
