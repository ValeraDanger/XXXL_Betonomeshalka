import recognition_module

import cv2
import time
import logging, coloredlogs
import numpy as np
import betonomeshalka.resheniya as resheniya
import betonomeshalka.protocol as protocol
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
    if (equal_num == 10 and card != None):
        logging.info('Карта принята')
        logging.info(card)
        comands = resheniya.desision(card, 'START1')
        logging.info(comands)
        protocol.send_command("C0\n")
        time.sleep(1)
        protocol.send_command("C-15\n")
        time.sleep(0.5)
        protocol.send_command("C0\n")
        time.sleep(2)
        protocol.send_command("C15\n")
        time.sleep(1.5)
        protocol.send_command("C0\n")
        time.sleep(7)
        protocol.send_command("C-15\n")
        time.sleep(0.8)
        protocol.send_command("C0\n")
        time.sleep(2.5)
        protocol.send_command("C-15\n")
        time.sleep(0.6)
        protocol.send_command("C0\n")
        time.sleep(2.5)
        protocol.send_command("C-15\n")
        time.sleep(0.6)
        protocol.send_command("C0\n")
        time.sleep(2)
        protocol.send_command("C15\n")
        time.sleep(2)
        protocol.send_command("C0\n")
        time.sleep(3)
        protocol.send_command("#\n")
        logging.info("Stopped")





 #       for i in range(0, len(comands), 2):
  #          while (exit_code != 'OK'):


    if (last_card != card):
        equal_num = 0
        logging.info('Недостаточно времени для распознавания карточки')
    last_card = card


# Clean up
threaded_camera.stream_stop()
