# Вывод изображения cv2:
# cv2.imread(картинка) – Получить изображение
# cv2.imshow(title, картинка) – Показать изображение
# cv2.waitKey() – Ждать нажатия


# Вывод текста на изображении:
# putText(картинка,текст,(x,y),Тип шрифта,Масштаб шрифта,Цвет)
#
# Рисование на изображении:
# cv2.line(картинка,(x,y), (x1,y1), цвет, толщина)
# cv2.rectangle(картинка,(x,y), (x1,y1), цвет, толщина)
# cv2.circle(картинка,(x,y), радиус, цвет, толщина)

# ROI
# img[y1:y2,x1:x2] – вырезать
# night[y1:y2,x1:x2] = neo – вставить
#
# cv2.flip(Изображение, code)

# Слои
# img[0:210,0:910,0] = 255 - синий
# img[0:210,0:910,1] = 255 - зеленый
# img[0:210,0:910,2] = 255 - красный

# Пиксели
# for x in range(img.shape[1]):
#     for y in range(img.shape[0]):
#         if img[:,:,0][y,x] < img[:,:,2][y,x]:
#             if img[:,:,1][y,x] < img[:,:,2][y,x]:
#                 if img[:,:,2][y,x] > 64:
#                     img[:,:,0][y,x] = 255


# Фильтры, размер, охранение
# img1 = cv2.resize(img1, (100, 100))
# dst = cv2.addWeighted(img1, 0.7, img2, 0.2, 1)
# blur = cv2.GaussianBlur(dst, (5,5), 0)
# cv2.imwrite("img.jpg", blur)

# Камера
# cap = cv2.VideoCapture(0)
# while True:
#     _, frame = cap.read()
#     cv2.imshow('frame', frame)
#     key = cv2.waitKey(1)
#     if key == 27:
#         break


# Время
#     loc_time = time.localtime(time.time())
#     time_date = time.strftime("%m/%d/%Y", loc_time)
#     time_clock = time.strftime("%H:%M:%S", loc_time)
#     cv2.rectangle(frame, (0, 0), (200, 50), (0, 0, 0), 2)
#     cv2.putText(frame, time_date,(0,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),1)
#     cv2.putText(frame, time_clock,(0,40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),1)



# HSV
# imageHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(imageHSV, trackbar_vals['min'], trackbar_vals['max'])
# im2 = cv2.bitwise_or(img, img, mask=mask)
# min_green = np.array((53, 128, 0), np.uint8)
# max_green = np.array((69, 255, 255), np.uint8)

#Контуры
# min_green = np.array((53, 128, 0), np.uint8)
# max_green = np.array((69, 255, 255), np.uint8)
#
# contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours, -1, (0,0,0), 3, cv2.LINE_AA, hierarchy, 1)
#
# count = 0
# for contour in contours:
#     area = cv2.contourArea(contour)
#     if area > 100:
#         count += 1
#
# cv2.putText(img1, str(count),(100,280), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3,(0,255,0),2)


# Регулторы
# for contour in contours:
#     area = cv2.contourArea(contour)
#     x, y, w, h = cv2.boundingRect(contour)
#     if area > 2000:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         # if x+w//2 > 320:
#         #     sim.move(-1, 3)
#         # else:
#         #     sim.move(1, 3)
#         e = 320 - (x + w // 2)
#         u = e * 0.01
#         if u > 3: u = 3
#         if u < -3: u = -3
#         sim.move(u, 3)



# Поиск пошаблону
#     img_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
#     template = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
#     res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
#     threshold = 0.99
#     loc = np.where(res >= threshold)
#     for x, y in zip(*loc[::-1]):
#         cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     cv2.imshow("Image", frame1)




# События мышки
# def callback(event, x, y, flags, param):
#     global x_mouse, y_mouse, crop_image, frame, w, h
#     frame_copy = frame.copy()
#     if event == cv2.EVENT_LBUTTONDOWN:
#         if x_mouse == -1:
#             x_mouse, y_mouse = x, y
#
#     if event == cv2.EVENT_LBUTTONUP:
#         if y > y_mouse: y, y_mouse = y_mouse, y
#         if x > x_mouse: x, x_mouse = x_mouse, x
#         crop_image = frame_copy[y:y_mouse, x:x_mouse]
#         cv2.destroyWindow('crop_image')
#         cv2.imshow('crop_image', crop_image)
#         x_mouse, y_mouse = -1, -1
#
#
#     if x_mouse != -1:
#         cv2.rectangle(frame_copy, (x, y), (x_mouse, y_mouse), (0, 255, 0), 2)
#
#     cv2.imshow('test', frame_copy)


# Опорные точки
# orb = cv2.ORB_create(1000)
#
# frame_image = frame.copy()
#
#     kp1, des1 = orb.detectAndCompute(frame, None)
#     kp2, des2 = orb.detectAndCompute(crop_image, None)
#
#     frame = cv2.drawKeypoints(frame, kp1, None, color=(0, 0, 255))
#     img2 = cv2.drawKeypoints(crop_image, kp2, None, color=(255, 0, 0))
#
#     bf = cv2.BFMatcher()
#     matches = bf.knnMatch(des1, des2, k=2)
#     good = []
#     goodxy = []
#     for mat in matches:
#         if mat[0].distance < 0.6 * mat[1].distance:
#             good.append([mat[0]])
#             xy = mat[0].queryIdx
#             (xm, ym) = kp1[xy].pt
#             goodxy.append((int(xm), int(ym)))
#
#     if len(good)>0:
#         frame = cv2.drawMatchesKnn(frame, kp1, img2, kp2, good, frame, flags=2)
#         Draw_rect(frame, goodxy)


# Каскады Хаара
# face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
#
# while True:
#     _, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 3)


#Запись видео и определение движения
# filename = "output.avi"
# out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640, 480))
# if out.isOpened():
#     print("Save video to:", filename, )
# else:
#     print("FAIL open file to save video")
#     exit(0)
#
# cap = cv2.VideoCapture(0)
# fgbg = cv2.createBackgroundSubtractorMOG2()
#
# while 1:
#     ret, frame = cap.read()
#     mask = fgbg.apply(frame)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
#     contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     for contour in contours:
#         if (cv2.contourArea(contour) > 4000):
#             x, y, w, h = cv2.boundingRect(contour)
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#             out.write(frame)
#     cv2.imshow('mask', mask)
#     cv2.imshow('frame', frame)
#     k = cv2.waitKey(1)
#     if k == 27:
#         break


# Определение угла наклона линии
# r, image = cap.read()
#
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# canny = cv2.Canny(gray, 50, 150)
# lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 15, np.array([]), 50, 20)
#
# angles = []
# if lines is not None:
#     for line in lines:
#         for x1, y1, x2, y2 in line:
#             cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 5)
#             angles.append(LineAngle(x1, y1, x2, y2))
# if len(angles) > 0:
#     a = 90 - np.median(np.array(angles))
#
# def LineAngle(x1, y1, x2, y2):
#     dx = x1 - x2
#     dy = y1 - y2
#     rads = math.atan2(-dy, dx)
#     rads %= math.pi
#     degs = math.degrees(rads)
#     return degs






#Движение по линии

# imageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(imageHSV, min, max)
# contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# sr = 0
# n = 0
# w_max = 0
# for contour in contours:
#     if (cv2.contourArea(contour) > 10):
#         x, y, w, h = cv2.boundingRect(contour)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#         sr += x + w // 2
#         n += 1
#         if w > w_max:
#             w_max = w
#
# if n > 0:
#     e = 100 - sr // n
#     u = e * 1
#     if w_max > 100:
#         sim.move(0, 5)
#     else:
#         sim.move(u, 5)
#     eold = e
# else:
#     if eold > 0:
#         sim.move(10, 1)
#     else:
#         sim.move(-10, 1)