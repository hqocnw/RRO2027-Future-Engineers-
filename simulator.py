import time

import cv2
import numpy as np
pole = cv2.imread("img/pole.png")
robot = cv2.imread("img/robot.png")
#1 первый этаж
#2 второй этаж
#61 62 63 64 пандус
#151 152 кр труба на 1 этаже
#251 252 кр труба на 2 этаже
#121 122 син труба на 1 этаже
#221 222 син труба на 2 этаже
#31 32 33 34 зеленая подставка

#10 езда 1 этаж 0 = n клеток
#20 езда 2 этаж 0 = n клеток
#24 заезд на пандус
#42 сьезд с пандуса
#44 двойной пандус
#51 взять трубу с 1 этажа
#52 взять трубу с 2 этажа
#53 выгруз трубы
#60 61 62 поворот в стороны

dict_p ={
 "s11": (1, 61), "s12": (1, 62), "s13": (1, 63),"s14":(1,64),
 "s21": (2,63), "s22": (2,64), "s23": (2,61),"s24": (2,62)
}




move = [62,44,61,11,60]


min_white = np.array((0, 0, 200), np.uint8)
max_white = np.array((180, 100, 255), np.uint8)

map= [[0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0]
      ]
map_draw= [[152,1,1,1,1,1,1,1],
      [2,63,2,2,2,64,1,63],
      [1,61,1,1,2,1,1,2],
      [1,1,1,1,1,1,2,221],
      [151,1,2,2,1,1,2,2],
      [1,1,2,2,1,1,61,61],
      [1,2,1,61,1,1,1,1],
      [1,1,1,1,1,31,31,31]
      ]
wave=[[100,100,100,100,100,100,100,100],
      [100,100,100,100,100,100,100,100],
      [100,100,100,100,100,100,100,100],
      [100,100,100,100,100,100,100,100],
      [100,100,100,100,100,100,100,100],
      [100,100,100,100,100,100,100,100],
      [100,100,100,100,100,100,100,100],
      [100,100,100,100,100,100,100,100]
      ]



for i in range(8):
    for j in range(8):
        pole[i*80:(i*80)+80,j*80:(j*80)+80] = cv2.imread("img/"+str(map_draw[i][j])+".png")

pole_draw=pole.copy()

robot_pos = [0,1] # y x
robot_dir = 1
def rotate(n):
      global robot, robot_dir, robot_pos
      if n == 1:
            robot = cv2.rotate(robot, cv2.ROTATE_90_CLOCKWISE)
            robot_dir+=1
            if robot_dir > 4:
                  robot_dir = 1
      elif n == 0:
            robot = cv2.rotate(robot, cv2.ROTATE_90_COUNTERCLOCKWISE)
            robot_dir -= 1
            if robot_dir < 1:
                  robot_dir = 4
      else:
            robot = cv2.rotate(robot, cv2.ROTATE_180)
            if robot_dir == 1: robot_dir = 3
            elif robot_dir == 2: robot_dir = 4
            elif robot_dir == 3: robot_dir = 1
            elif robot_dir == 4: robot_dir = 2



      draw_robot()
def draw_pole():
      cv2.imshow("pole", pole_draw)


def draw_robot():
      global pole_draw
      crop = pole[robot_pos[0] * 80:robot_pos[0] * 80 + 80, robot_pos[1] * 80:robot_pos[1] * 80 + 80].copy()
      imageHSV = cv2.cvtColor(robot, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(imageHSV, min_white, max_white)
      mask1=cv2.bitwise_not(mask)
      # cv2.imshow("mask", mask1)
      img = cv2.bitwise_and(robot, robot, mask=mask1)
      img1 = cv2.bitwise_and(crop,crop, mask=mask)
      pole_draw[robot_pos[0] * 80:robot_pos[0] * 80 + 80, robot_pos[1] * 80:robot_pos[1] * 80 + 80]=img+img1



def robot_move(y,x,t):
      global pole_draw, robot_dir, robot_pos
      y1 = robot_pos[0]
      x1 = robot_pos[1]
      gt = 0
      if y != y1:
            if y1 < y:
                  gt = 3
            elif y1 > y:
                  gt= 1
      if x != x1:
            if x1 > x:
                  gt = 4
            elif x1 < x:
                  gt = 2
      y1 = robot_pos[0]*80
      x1 = robot_pos[1]*80
      y =y*80
      x =x*80
      imageHSV = cv2.cvtColor(robot, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(imageHSV, min_white, max_white)
      mask1 = cv2.bitwise_not(mask)
      img = cv2.bitwise_and(robot, robot, mask=mask1)

      if gt == 2:
           for i in range(x1,x+1,1):
                  crop = pole[y:y+80,i:i+80].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[y:y+80,i:i+80] = img + img1
                  # print(y,y+80,i,i+80)

                  # cv2.imshow("test",crop)

                  draw_pole()
                  cv2.waitKey(t)
      elif gt == 4:
            for i in range(x1, x - 1, -1):
                  crop = pole[y:y + 80, i:i + 80].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[y:y + 80, i:i + 80] = img + img1
                  # print(y, y + 80, i, i + 80)

                  # cv2.imshow("test", crop)

                  draw_pole()
                  cv2.waitKey(t)
      elif gt == 1:
            for i in range(y1, y - 1, -1):
                  crop = pole[i:i + 80, x:x + 80].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[i:i + 80, x:x + 80] = img + img1
                  # print(y, y + 80, i, i + 80)

                  # cv2.imshow("test", crop)

                  draw_pole()
                  cv2.waitKey(t)
      elif gt == 3:
                  for i in range(y1, y+1, 1):
                        crop = pole[i:i + 80, x:x + 80].copy()
                        img1 = cv2.bitwise_and(crop, crop, mask=mask)
                        pole_draw[i:i + 80, x:x + 80] = img + img1
                        # print(y,  + 80, i, i + 80)
                        #
                        # cv2.imshow("test", crop)

                        draw_pole()
                        cv2.waitKey(t)
                  # time.sleep(t)
      robot_pos[0] = y//80
      robot_pos[1] = x//80

def drive(t):
      for i in move:
            if  i == 60 or i==61 or i ==62:
                  rotate(i-60)
                  draw_pole()

            if  i >10 and i < 20:
                  if robot_dir == 1:robot_move(robot_pos[0]-(i-10),robot_pos[1],t)
                  if robot_dir == 3:robot_move(robot_pos[0] + (i - 10), robot_pos[1],t)
                  if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]+(i-10),t)
                  if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-(i-10),t)
            if  i >20 and i < 30:
                  if robot_dir == 1:robot_move(robot_pos[0]-(i-20),robot_pos[1],t)
                  if robot_dir == 3:robot_move(robot_pos[0] - (i - 20), robot_pos[1],t)
                  if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]-(i-20),t)
                  if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-(i-20),t)
            if  i == 24 or i ==42:
                  if robot_dir == 1:robot_move(robot_pos[0]-2,robot_pos[1],t+10)
                  if robot_dir == 3:robot_move(robot_pos[0] + 2, robot_pos[1],t+10)
                  if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]+2,t+10)
                  if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-2,t+10)
            if i == 44:
                  if robot_dir == 1:robot_move(robot_pos[0]-3,robot_pos[1],t+10)
                  if robot_dir == 3:robot_move(robot_pos[0] + 3, robot_pos[1],t+10)
                  if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]+3,t+10)
                  if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-3,t+10)







draw_robot()
draw_pole()
# cv2.imshow("pole",pole_draw)
cv2.waitKey()
# rotate(2)
# draw_pole()
# cv2.waitKey()
# robot_move(7,4,1)
drive(1)

# cv2.imshow("pole",pole_draw)

# robot_move(0,4)

cv2.waitKey()