import cv2 as cv
import numpy as np
import razmetka_library as razmetka_library
import logging

video = cv.VideoCapture(0)
if not video.isOpened():
    logging.warning( u'Камера не работает, проверьте подключение' )
# выставление задержки между кадрами
cv.waitKey(1)

while video.isOpened():
    _, frame = video.read()
    # настройка разрешения изображения
    #cv.resizeWindow("razmetka", 1280, 720)
    #cv.namedWindow("razmetka", cv.WINDOW_NORMAL)
    # первый слой изображения
    copy_img = np.copy(frame)

    try:
        # второй слой изображения
        frame = razmetka_library.canny(frame)
        frame = razmetka_library.mask(frame)
        # поиск линий на изображении при помощи numpy
        lines = cv.HoughLinesP(frame, 2, np.pi/180, 100, np.array([()]), minLineLength=20, maxLineGap=5)
        # усредняем линии
        avaraged_lines = razmetka_library.average_slope_intercept(frame, lines)

        # отображаем эти самые линии на изображении №1
        line_image = razmetka_library.display_lines(copy_img, avaraged_lines)

        #комбинируем изображения 1 и 2
        combo = cv.addWeighted(copy_img, 0.8, line_image, 0.5, 1)

        # вывод изображеия
        cv.imshow("razmetka", frame)
    except:
        pass
    # выход при помощи кнопуи q
    if cv.waitKey(1) & 0xFF == ord('q'):
        video.release()
        cv.destroyAllWindows()




