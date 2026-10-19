import time

import cv2
import numpy as np
pole = cv2.imread("img/pole.png")
robot = cv2.imread("img/robot.png")
images_array = np.zeros([640,1300,3],dtype=np.uint8)
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
#43 заезд на пандус
#42 сьезд с пандуса
#44 двойной пандус1
#51 взять трубу с 1 этажа
#52 взять трубу с 2 этажа
#53 выгруз трубы
#60 61 62 поворот в стороны

dict_p ={
      "1":[[1,61],[1,62],[1,63],[1,64]],
      "2":[[2,63],[2,64],[2,61],[2,62]],
      "61":[[2,63],[0],[1,63],[0]],
      "62":[[0],[2,64],[0],[1,64]],
      "63":[[1,61],[0],[2,61],[0]],
      "64":[[0],[1,62],[0],[2,62]],
      "151": [[0],[0],[0],[0]],
      "152": [[0],[0],[0],[0]],
      "251": [[0],[0],[0],[0]],
      "252": [[0],[0],[0],[0]],
      "121": [[0],[0],[0],[0]],
      "122": [[0],[0],[0],[0]],
      "221": [[0],[0],[0],[0]],
      "222": [[0],[0],[0],[0]],
      "31": [[0],[0],[0],[0]],
      "32": [[0],[0],[0],[0]],
      "33": [[0],[0],[0],[0]],
      "34": [[0],[0],[0],[0]]


}
dict_tube = {
      "151":[[1],[0],[1],[0]],
      "152":[[0],[1],[0],[1]],
      "251":[[2],[0],[2],[0]],
      "252":[[0],[2],[0],[2]],
      "121":[[1],[0],[1],[0]],
      "122":[[0],[1],[0],[1]],
      "221":[[2],[0],[2],[0]],
      "222":[[0],[2],[0],[2]],
      "31":[[1],[0],[0],[0]],
      "32":[[0],[1],[0],[0]],
      "33":[[0],[0],[1],[0]],
      "34":[[0],[0],[0],[1]]
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
map_draw= [[1,1,1,1,1,1,1,1],
      [2,63,252,2,2,64,1,63],
      [1,61,1,1,2,1,1,2],
      [1,1,1,1,1,1,2,2],
      [1,1,2,2,1,1,2,2],
      [1,1,2,2,1,1,61,61],
      [1,2,121,61,1,1,1,1],
      [151,1,1,1,1,31,31,31]
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
dlina = 0
trubi = [[0,0],[1,2],[6,2],[7,0],[7,6]]
fin_path =[]
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

def rotate_pro(N):
      global robot_dir
      r = -1
      cur_dir = robot_dir
      if N != cur_dir:
            if N == 1:
                  if cur_dir == 2:r = 0
                  elif cur_dir == 3:r = 2
                  elif cur_dir == 4:r = 1
            if N == 2:
                  if cur_dir == 1:r = 1
                  elif cur_dir== 3:r = 0
                  elif cur_dir == 4:r = 2
            if N == 3:
                  if cur_dir == 2:r = 1
                  elif cur_dir == 1:r = 2
                  elif cur_dir == 4:r = 0
            if N == 4:
                  if cur_dir == 2:r = 2
                  elif cur_dir == 3:r = 1
                  elif cur_dir == 1:r = 0
            # rotate(r)
            cur_dir = N
            return r + 60
      else: return 59

def draw_pole():
      # cv2.imshow("pole", pole_draw)
      images_array[0:640,0:640] = pole_draw

def Wave_pole():
      wave_pole = pole.copy()
      for i in range(8):
            for g in range(8):
                  cv2.putText(wave_pole,str(wave[g][i]),(30+i*80,45+g*80),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
      images_array[0:640,660:1300] = wave_pole

def show_pole():
      global images_array
      draw_pole()
      Wave_pole()
      images_array = cv2.rectangle(images_array,(640,0),(660,640),(0,250,255),-1)
      cv2.imshow("pole", images_array)
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


def Wave(y,x):
      cordsN = [[y,x]]
      flag_stop = True

      for i in range(8):
            for g in range(8):
                  wave[i][g] = 100
      wave[y][x] = 0
      while flag_stop:
            cords = []

            for y1,x1 in cordsN:
                  start = map_draw[y1][x1]
                  # print(start,y1,x1)
                  ynew = y1
                  xnew = x1
                  if ynew-1 >=0:
                       cord = int(map_draw[ynew-1][xnew])
                       # print(1,cord)
                       # print(start, cord)
                       # print(cord,dict_p.get(str(start))[0])
                       if cord in dict_p.get(str(start))[0] and wave[ynew - 1][xnew] > wave[ynew][xnew]:
                              wave[ynew - 1][xnew] = wave[ynew][xnew] + 1
                              if cord == 61 or cord == 63: wave[ynew - 1][xnew] += 2
                              cords.append([ynew-1,xnew])



                  if ynew +1 <= 7:
                        cord = int(map_draw[ynew + 1][ xnew])
                        # print(3,cord)
                        # print(start, cord)
                        # print(cord,dict_p.get(str(start))[0])

                        if cord in dict_p.get(str(start))[2] and wave[ynew + 1][xnew] > wave[ynew][xnew]:
                              wave[ynew + 1][xnew] = wave[ynew][xnew] + 1
                              if cord == 63 or cord == 61: wave[ynew + 1][xnew] += 2
                              cords.append([ynew+1,xnew])

                  if xnew - 1 >= 0:
                        cord = int(map_draw[ynew][xnew-1])
                        # print(start,cord)
                        # print(4,cord)
                        # print(cord, dict_p.get(str(start))[0])

                        if cord in dict_p.get(str(start))[3] and wave[ynew][xnew-1] > wave[ynew][xnew]:
                              wave[ynew][xnew-1] = wave[ynew][xnew] + 1
                              if cord == 64 or cord == 62: wave[ynew][xnew-1] += 2
                              cords.append([ynew,xnew-1])

                  if xnew + 1 <= 7:
                        cord = int(map_draw[ynew][ xnew + 1])
                        # print(2,cord)
                        # print(start, cord)
                        # print(cord, dict_p.get(str(start))[0])

                        if cord in dict_p.get(str(start))[1] and wave[ynew][xnew+1] > wave[ynew][xnew]:
                              wave[ynew][xnew + 1] = wave[ynew][xnew] + 1
                              if cord == 62 or cord == 64:wave[ynew][xnew + 1] += 2
                              cords.append([ynew,xnew+1])
            # print(cords)
            if len(cords) > 0:
                  cordsN = cords
            else: flag_stop = False
            # print(cordsN)
      # print(wave)

def FindPath(y,x):
      flag_s = True
      start = [2,3]
      path = []
      goal = [y,x]
      min = 100
      cv2.circle(pole_draw,((x*80)+40,(y*80)+40),20,(0,0,255),-1)


      if map_draw[y][x] in [151,152,121,122,251,252,221,222, 31, 32, 33, 34]:
            if y - 1 >= 0:
                  if map_draw[y - 1][x] in dict_tube.get(str(map_draw[y][x]))[0]:
                        # path.append([y, x])
                        goal = [y-1, x]
                        min = wave[y-1][x]
                        # print(goal,min)
            if y + 1<= 7:
                  if map_draw[y + 1][x] in dict_tube.get(str(map_draw[y][x]))[2]:
                        # path.append([y, x])
                        if min > wave[y+1][x]:
                              min = wave[y+1][x]
                              goal = [y + 1, x]
            if x - 1 >= 0:
                  if map_draw[y][x-1] in dict_tube.get(str(map_draw[y][x]))[3]:
                        # path.append([y, x])
                        if min > wave[y][x-1]:
                              min = wave[y][x-1]
                              goal = [y, x-1]

            if x + 1 <=7:
                  if map_draw[y][x+1] in dict_tube.get(str(map_draw[y][x]))[1]:
                        # path.append([y, x])
                        if min > wave[y][x+1]:
                              min = wave[y][x+1]
                              goal = [y, x+1]

      else: min = wave[y][x]
      path.append(goal)
      tube = goal

      # print(min,goal)


      while flag_s:
            y = goal[0]
            x = goal[1]
            flag_r =False
            if y - 1 >= 0:
                  if map_draw[y - 1][x] in dict_p.get(str(map_draw[y][x]))[0] and wave[y][x] > wave[y-1][x]:
                        # min = wave[y - 1][x]
                        path.append([y-1, x])
                        goal = [y - 1, x]
                        flag_r = True
                        # print(goal)
                        # min = wave[y - 1][x]
            if y + 1 <= 7 and flag_r == False:
                  if map_draw[y + 1][x] in dict_p.get(str(map_draw[y][x]))[2] and wave[y][x] > wave[y+1][x]:
                        path.append([y+1, x])
                        goal = [y + 1, x]
                        flag_r = True
                        # print(goal)

                        # min = wave[y + 1][x]
            if x - 1 >= 0 and flag_r == False:
                  if map_draw[y][x - 1] in dict_p.get(str(map_draw[y][x]))[3] and wave[y][x] > wave[y][x-1]:
                        path.append([y, x-1])
                        goal = [y, x - 1]
                        flag_r = True
                        # print(goal)

                        # min = wave[y][x - 1]
            if x + 1 <= 7 and flag_r == False:
                  if map_draw[y][x + 1] in dict_p.get(str(map_draw[y][x]))[1] and wave[y][x] > wave[y][x+1]:
                        path.append([y, x+1])
                        goal = [y, x + 1]
                        flag_r = True
                        # print(goal)
            if flag_r == False:
                  flag_s = False



                        # min = wave[y][x + 1]
            # y = goal[0]
            # x = goal[1]
            if wave[goal[0]][goal[1]] == 0 :
                  flag_s = False
                  # path.append([goal[0], goal[1]])
            # flag_s = False
      # print(path)
      if wave[goal[0]][goal[1]] == 0:
            return path[::-1],tube
      else:
            return [[-1,-1]],tube



def robot_move(y,x,t):

      global pole_draw, robot_dir, robot_pos
      # print(y, x, t, robot_pos[0], robot_pos[1])
      y = max(0, min(7, y))
      x = max(0, min(7, x))
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

                  show_pole()
                  cv2.waitKey(t)
      elif gt == 4:
            for i in range(x1, x - 1, -1):
                  crop = pole[y:y + 80, i:i + 80].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[y:y + 80, i:i + 80] = img + img1
                  # print(y, y + 80, i, i + 80)

                  # cv2.imshow("test", crop)

                  show_pole()
                  cv2.waitKey(t)
      elif gt == 1:
            for i in range(y1, y - 1, -1):
                  crop = pole[i:i + 80, x:x + 80].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[i:i + 80, x:x + 80] = img + img1
                  # print(y, y + 80, i, i + 80)

                  # cv2.imshow("test", crop)

                  show_pole()
                  cv2.waitKey(t)
      elif gt == 3:
                  for i in range(y1, y+1, 1):
                        crop = pole[i:i + 80, x:x + 80].copy()
                        img1 = cv2.bitwise_and(crop, crop, mask=mask)
                        pole_draw[i:i + 80, x:x + 80] = img + img1
                        # print(y,  + 80, i, i + 80)
                        #
                        # cv2.imshow("test", crop)

                        show_pole()
                        cv2.waitKey(t)
                  # time.sleep(t)
      robot_pos[0] = y//80
      robot_pos[1] = x//80
      # print(y,x)

def drive(t):
      for i in move:
            # print(i)
            if  i == 60 or i==61 or i ==62:
                  rotate(i-60)
                  show_pole()
                  # print(robot_pos[0], robot_pos[1])
            if  i > 10 and i < 20:
                  if robot_dir == 1:robot_move(robot_pos[0]-(i-10),robot_pos[1],t)
                  if robot_dir == 3:robot_move(robot_pos[0] + (i - 10), robot_pos[1],t)
                  if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]+(i-10),t)
                  if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-(i-10),t)
            if  i >20 and i < 30:
                  if robot_dir == 1:robot_move(robot_pos[0]-(i-20),robot_pos[1],t)
                  if robot_dir == 3:robot_move(robot_pos[0] + (i - 20), robot_pos[1],t)
                  if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]+(i-20),t)
                  if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-(i-20),t)
            if  i == 43 or i ==42:
                  # print(robot_pos[0],robot_pos[1])
                  if robot_dir == 1:robot_move(robot_pos[0]-1,robot_pos[1],t+10)
                  if robot_dir == 3:robot_move(robot_pos[0] + 1, robot_pos[1],t+10)
                  if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]+1,t+10)
                  if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-1,t+10)
            # if i == 44:
            #       if robot_dir == 1:robot_move(robot_pos[0]-3,robot_pos[1],t+10)
            #       if robot_dir == 3:robot_move(robot_pos[0] + 3, robot_pos[1],t+10)
            #       if robot_dir == 2:robot_move(robot_pos[0], robot_pos[1]+3,t+10)
            #       if robot_dir == 4:robot_move(robot_pos[0], robot_pos[1]-3,t+10)
def make_drive(path):
      global move,robot_dir, dlina
      dlina = 0
      move = []
      save_dir = robot_dir
      for i in range(len(path)-1):
            if path[i][0] > path[i+1][0]:
                  r = rotate_pro(1)
                  robot_dir = 1
                  if r != 59: move.append(r)
                  if map_draw[path[i+1][0]][path[i+1][1]] == 1:
                        move.append(11)
                        dlina +=1
                  if map_draw[path[i+1][0]][path[i+1][1]] == 2:
                        move.append(21)
                        dlina += 1
                  if map_draw[path[i+1][0]][path[i+1][1]] == 61:
                        move.append(43)
                        dlina += 3
                  if map_draw[path[i+1][0]][path[i+1][1]] == 63:
                        move.append(42)
                        dlina += 3
                  # if map_draw[path[i+1][0]][path[i+1][1]] == 61 and map_draw[path[i][0]][path[i][1]] == 63:
                  #       move.append(44)
                  # if map_draw[path[i + 1][0]][path[i + 1][1]] == 63 and map_draw[path[i][0]][path[i][1]] == 61:
                  #       move.append(44)
            if path[i][0] < path[i+1][0]:
                  r = rotate_pro(3)
                  robot_dir = 3
                  if r != 59: move.append(r)
                  if map_draw[path[i+1][0]][path[i+1][1]] == 1:
                        move.append(11)
                        dlina += 1

                  if map_draw[path[i+1][0]][path[i+1][1]] == 2:
                        move.append(21)
                        dlina += 1

                  if map_draw[path[i+1][0]][path[i+1][1]] == 61:
                        move.append(43)
                        dlina += 3

                  if map_draw[path[i+1][0]][path[i+1][1]] == 63 :
                        move.append(42)
                        dlina += 3

                  # if map_draw[path[i+1][0]][path[i+1][1]] == 61 and map_draw[path[i][0]][path[i][1]] == 63:
                  #       move.append(44)
                  # if map_draw[path[i + 1][0]][path[i + 1][1]] == 63 and map_draw[path[i][0]][path[i][1]] == 61:
                  #       move.append(44)
            if path[i][1] > path[i+1][1]:
                  r = rotate_pro(4)
                  robot_dir = 4
                  if r != 59: move.append(r)
                  if map_draw[path[i+1][0]][path[i+1][1]] == 1:
                        move.append(11)
                        dlina += 1

                  if map_draw[path[i+1][0]][path[i+1][1]] == 2:
                        move.append(21)
                        dlina += 1

                  if map_draw[path[i+1][0]][path[i+1][1]] == 64:
                        move.append(43)
                        dlina += 3

                  if map_draw[path[i+1][0]][path[i+1][1]] == 62:
                        move.append(42)
                        dlina += 3

                  # if map_draw[path[i+1][0]][path[i+1][1]] == 61 and map_draw[path[i][0]][path[i][1]] == 63:
                  #       move.append(44)
                  # if map_draw[path[i + 1][0]][path[i + 1][1]] == 63 and map_draw[path[i][0]][path[i][1]] == 61:
                  #       move.append(44)
            if path[i][1] < path[i+1][1]:
                  r = rotate_pro(2)
                  robot_dir = 2
                  if r != 59: move.append(r)
                  if map_draw[path[i+1][0]][path[i+1][1]] == 1:
                        move.append(11)
                        dlina += 1

                  if map_draw[path[i+1][0]][path[i+1][1]] == 2:
                        move.append(21)
                        dlina += 1

                  if map_draw[path[i+1][0]][path[i+1][1]] == 62:
                        move.append(43)
                        dlina += 3

                  if map_draw[path[i+1][0]][path[i+1][1]] == 64:
                        move.append(42)
                        dlina += 3

                  # if map_draw[path[i+1][0]][path[i+1][1]] == 61 and map_draw[path[i][0]][path[i][1]] == 63:
                  #       move.append(44)
                  # if map_draw[path[i + 1][0]][path[i + 1][1]] == 63 and map_draw[path[i][0]][path[i][1]] == 61:
                  #       move.append(44)
      robot_dir = save_dir


def calc_path():
      global pole_draw,fin_path
      trubi[0] = robot_pos
      dlini = []

      marsh = [[trubi[0],trubi[1],trubi[2],trubi[3],trubi[4]],
               [trubi[0],trubi[1],trubi[3],trubi[2],trubi[4]],
               [trubi[0],trubi[2],trubi[1],trubi[3],trubi[4]],
               [trubi[0], trubi[2], trubi[3], trubi[1], trubi[4]],
               [trubi[0], trubi[3], trubi[1], trubi[2], trubi[4]],
               [trubi[0], trubi[3], trubi[2], trubi[1], trubi[4]]
               ]
      super_path =[]

      for x in range(6):
            joh = 0
            start = marsh[x][0][0], marsh[x][0][1]
            for y in range(4):

                  # print(start[0],start[1],marsh[x][y+1][0],marsh[x][y+1][1])
                  Wave(start[0],start[1])

                  der,tube = FindPath(marsh[x][y+1][0],marsh[x][y+1][1])
                  start=tube
                  der.append([marsh[x][y+1][0],marsh[x][y+1][1]])
                  super_path.append(der)
                  make_drive(der)
                  # print(dlina,der)
                  # Wave_pole()
                  # show_pole()
                  # cv2.waitKey()
                  joh += dlina
            # print(" ")
            dlini.append(joh)


      print(dlini)
      # for i in super_path:
      #       print(i)
      size = [20, 15, 10, 5]
      color = [(0, 0, 255), (0, 255, 255), (255, 0, 0), (0, 255, 0)]

      for r in range(6):
            j = 0
            pole_draw = pole.copy()
            for i in range(4):
                  for y, x in super_path[r*4+i]:
                        cv2.circle(pole_draw, (x * 80 + 40, y * 80 + 40), size[j], color[j], -1)
                  j += 1

            # show_pole()
            # cv2.waitKey()
      minV = min(dlini)
      num = dlini.index(minV)
      print(num)
      for i in range(4):
            fin_path.append(super_path[num*4+i])
      print(fin_path)

      j = 0
      pole_draw = pole.copy()
      for i in fin_path:
            for y, x in i:
                  cv2.circle(pole_draw, (x * 80 + 40, y * 80 + 40), size[j], color[j], -1)
            j += 1


















# cords = "1"
# start = pole[2][3]
# print(start)
# print(1 in dict_p.get(str(start))[0])
robot_pos = [4,4] # y x

calc_path()
draw_robot()
draw_pole()
show_pole()

cv2.waitKey()
for i in range(4):
      make_drive(fin_path[i])
      print(fin_path[i])
      print(move)
      drive(1)
      print(robot_pos)
      cv2.waitKey()

# show_pole()
# draw_pole()
# wave_pole()
# Wave(robot_pos[0],robot_pos[1])
# doroga = FindPath(4,3)
# show_pole()
# print(doroga)
# make_drive(doroga)
# cv2.imshow("pole",pole_draw)
# cv2.waitKey()
# print(move,dlina)
# rotate(2)
# draw_pole()
# cv2.waitKey()
# robot_move(7,4,1)
# move = [62,44,61,11,60]

# robot_dir = 1
# drive(1)

# cv2.imshow("pole",pole_draw)

# robot_move(0,4)

cv2.waitKey()