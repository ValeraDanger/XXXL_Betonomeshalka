import recognition_module
import cv2
import time
import logging, coloredlogs
import numpy as np
import classes as classes
import protocol as protocol
import math

#import betonomeshalka.color_recognition.dominator_color_webcam
import pprint

coloredlogs.install(level='DEBUG')
logging.basicConfig(level=logging.DEBUG)

threaded_camera = recognition_module.ThreadedCamera(0)
detection_result = np.zeros(4)


while (cv2.getWindowProperty('frame', 0) == -1):
    try:
        detection_result = threaded_camera.show_frame()
    except AttributeError:
        pass

recognition_module.cv2.destroyAllWindows()
logging.info('Нейросеть Инициализированна')
time.sleep(5)

logging.info('Запуск распознавания')
def stream():
    j = 0
    recognized_percents = []
    recognized_classes = []
    try:
        detection_result = threaded_camera.show_frame()
        #print(detection_result[2][0][0])
        while True:
            if detection_result[1][0][j] < 0.8:
                break
            recognized_percents.append(detection_result[1][0][j])
            j += 1
        for i in range(len(recognized_percents)):
            recognized_classes.append(detection_result[2][0][i])

        if (len(recognized_classes) > 0 and recognized_classes[0] > 0 and recognized_classes[0] < 10):
            color = threaded_camera.detect_colour(detection_result[0][0][0])
            if (color != None):
                card = str(color) + str(int(recognized_classes[0]))
                last_card = card
                return card


    except AttributeError:
        pass

last_card = ''
equal_num = 0
while True:

    card = 0
    card = stream()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if (last_card == card and card != None):
        equal_num += 1
        logging.info('{0} из 15'.format(equal_num))
    if (equal_num == 5 and card != None):
        logging.info('Карта принята')
        logging.info(card)
        comands = classes.my_programm("START1", card)
        if comands == None:
            break
        logging.info(comands)
        if (comands != None):
            for i in range(0, len(comands), 2):
                circle_lenth = 122
                wheel_lenth = 28
                corner = int(comands[i])
                if (corner != 0):

                    answer, enc, sost = protocol.check_sost()

                    protocol.send_command("#\n")
                    while (sost != "waitingCommand"):
                        answer, enc, sost = protocol.check_sost()
                    if corner < 0:
                        protocol.send_command('C45\n')
                    else:
                        protocol.send_command('C-45\n')

                    while (abs(corner) > math.degrees(abs((enc)/4/360*wheel_lenth/25))):
                        answer, enc, sost = protocol.check_sost()
                        logging.info(enc)
                        logging.info("bred")
                protocol.send_command('#\n')
                while (sost != "waitingCommand"):
                    answer, enc, sost = protocol.check_sost()
                enc = 0
                logging.info(str(i) + ' команда')
                protocol.send_command('C0\n')
                answer, last_enc, sost = protocol.check_sost()
                while (int(comands[i+1])*2 > (enc-last_enc)/4/360*wheel_lenth):
                    logging.info("ENC: {0}".format(enc-last_enc))
                    answer, enc, sost = protocol.check_sost()
                    # logging.info('Ответ {0}'.format(answer))
                    # logging.info('Состояние {0}'.format(sost))
                    # logging.info('Энкодер {0}'.format(enc))
                protocol.send_command('#\n')
                while (sost != "waitingCommand"):
                    answer, enc, sost = protocol.check_sost()

 #       for i in range(0, len(comands), 2):
  #          while (exit_code != 'OK'):


    if (last_card != card):
        equal_num = 0
        logging.info('Недостаточно времени для распознавания карточки')
    last_card = card


# Clean up
threaded_camera.stream_stop()
