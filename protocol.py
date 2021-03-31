import serial
import time
import pprint
import logging, coloredlogs

coloredlogs.install(level='DEBUG')
logging.basicConfig(level=logging.DEBUG)
try:
    ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
    logging.info('Сериал инициализирован')
    print(ser.readline())
except:
    logging.info('Ошибка инициализации сериала')

'''
    A - скорость первого мотора #
    B - скорость второго мотора #
    C - угол направляющего колеса
    D - время работы моторов
'''

def check_sost():
    answer = ser.readline().decode()
    answer = answer[:-2]
    enc = 0
    sost = "waitingAnswer"
    if (answer == "OK"):
        sost = "waitingCommand"
    elif (answer[0:3] == 'ENC'):
        sost = "readingEnc"
        enc = answer[3:-1]+answer[-1]
    elif (answer == 'Stoped'):
        sost = "waitingCommand"
        logging.info('Stoped')
    elif (answer == "isStart"):
        sost = "waitingCommand"

    return answer, -int(enc), sost

def send_command(command):
    try:
        ser.write(command.encode())
        logging.info(command.encode())
    except:
        logging.info('Ошибка отправки команды')

