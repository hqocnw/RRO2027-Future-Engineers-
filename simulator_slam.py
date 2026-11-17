import time

import cv2
import numpy as np

pole = cv2.imread("img/pole_slam.png")
robot = cv2.imread("img/robot.png")
images_array = np.zeros([690,1850,3],dtype=np.uint8)
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

min_green = np.array((53, 128, 0), np.uint8)
max_green = np.array((69, 255, 255), np.uint8)

min_blue = np.array((100, 150, 50), np.uint8)
max_blue = np.array((140, 255, 255), np.uint8)

min_black = np.array((0, 0, 0), np.uint8)
max_black = np.array((180, 255, 50), np.uint8)

min_red1 = np.array((0, 120, 70), np.uint8)
max_red1 = np.array((10, 255, 255), np.uint8)
min_red2 = np.array((170, 120, 70), np.uint8)
max_red2 = np.array((180, 255, 255), np.uint8)

min_yellow = np.array((20, 100, 100), np.uint8)
max_yellow = np.array((35, 255, 255), np.uint8)



# map_draw= [[2,221,2,1,1,1,1,1],
#       [2,61,2,2,2,64,1,63],
#       [1,1,1,1,2,1,1,2],
#       [1,1,1,1,1,1,2,2],
#       [1,1,2,2,1,1,2,2],
#       [1,1,2,2,1,1,61,61],
#       [1,2,121,61,1,1,1,2],
#       [151,2,2,2,1,31,31,31]
#       ]
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
slam_map = [[0 for _ in range(17)] for _ in range(17)]
# края поля в slam_map: номер первой/последней строки и столбца поля, None - еще не знаем
granitsy = {"top": None, "bottom": None, "left": None, "right": None}

camera = 0

PAD  = 25
CELL = 80
GRID = 8

for i in range(GRID):
    for j in range(GRID):
        y0 = i * CELL + PAD
        x0 = j * CELL + PAD
        pole[y0:y0 + CELL, x0:x0 + CELL] = cv2.imread(f"img/{map_draw[i][j]}.png")

pole_draw=pole.copy()

robot_pos = [1,6] # y x
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
      images_array[0:690,0:690] = pole_draw
      # cv2.imshow("pole", images_array)

def show_pole():
    draw_pole()
    cv2.imshow("pole", images_array)


def draw_robot():
      global pole_draw
      y0 = robot_pos[0] * CELL + PAD
      x0 = robot_pos[1] * CELL + PAD
      crop = pole[y0:y0 + CELL, x0:x0 + CELL].copy()
      imageHSV = cv2.cvtColor(robot, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(imageHSV, min_white, max_white)
      mask1 = cv2.bitwise_not(mask)
      img = cv2.bitwise_and(robot, robot, mask=mask1)
      img1 = cv2.bitwise_and(crop, crop, mask=mask)
      pole_draw[y0:y0 + CELL, x0:x0 + CELL] = img + img1

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
      cv2.circle(pole_draw,(x*CELL+PAD+40,y*CELL+PAD+40),20,(0,0,255),-1)


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
                  gt = 1
      if x != x1:
            if x1 > x:
                  gt = 4
            elif x1 < x:
                  gt = 2

      y1 = robot_pos[0] * CELL + PAD
      x1 = robot_pos[1] * CELL + PAD
      y = y * CELL + PAD
      x = x * CELL + PAD

      imageHSV = cv2.cvtColor(robot, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(imageHSV, min_white, max_white)
      mask1 = cv2.bitwise_not(mask)
      img = cv2.bitwise_and(robot, robot, mask=mask1)

      if gt == 2:
            for i in range(x1, x + 1, 1):
                  crop = pole[y:y + CELL, i:i + CELL].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[y:y + CELL, i:i + CELL] = img + img1
                  show_pole()
                  cv2.waitKey(t)
      elif gt == 4:
            for i in range(x1, x - 1, -1):
                  crop = pole[y:y + CELL, i:i + CELL].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[y:y + CELL, i:i + CELL] = img + img1
                  show_pole()
                  cv2.waitKey(t)
      elif gt == 1:
            for i in range(y1, y - 1, -1):
                  crop = pole[i:i + CELL, x:x + CELL].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[i:i + CELL, x:x + CELL] = img + img1
                  show_pole()
                  cv2.waitKey(t)
      elif gt == 3:
            for i in range(y1, y + 1, 1):
                  crop = pole[i:i + CELL, x:x + CELL].copy()
                  img1 = cv2.bitwise_and(crop, crop, mask=mask)
                  pole_draw[i:i + CELL, x:x + CELL] = img + img1
                  show_pole()
                  cv2.waitKey(t)

      robot_pos[0] = (y - PAD) // CELL
      robot_pos[1] = (x - PAD) // CELL

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
                        cv2.circle(pole_draw, (x * CELL + PAD + 40, y * CELL + PAD + 40), size[j], color[j], -1)
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
                  cv2.circle(pole_draw, (x * CELL + PAD + 40, y * CELL + PAD + 40), size[j], color[j], -1)
            j += 1

def camera_view():
      # что видит камера робота: 3 ряда по 3 клетки, нос робота смотрит вверх
      # робот стоит в середине нижнего ряда
      # за полем ничего нет (черное)
      big = cv2.copyMakeBorder(pole, 160, 160, 160, 160, cv2.BORDER_CONSTANT, value=(0, 0, 0))
      y0 = robot_pos[0] * 80 + PAD
      x0 = robot_pos[1] * 80 + PAD
      kvadrat = big[y0:y0 + 400, x0:x0 + 400]  # 5x5 клеток, робот в центре

      # поворачиваем так, чтобы робот смотрел вверх
      if robot_dir == 2:
            kvadrat = cv2.rotate(kvadrat, cv2.ROTATE_90_COUNTERCLOCKWISE)
      elif robot_dir == 3:
            kvadrat = cv2.rotate(kvadrat, cv2.ROTATE_180)
      elif robot_dir == 4:
            kvadrat = cv2.rotate(kvadrat, cv2.ROTATE_90_CLOCKWISE)

      return kvadrat[0:240, 80:320].copy()


def raspoznat_kletku(kletka):
      # распознаем клетку из кадра камеры: сначала поворачиваем ее, как она лежит на поле
      global camera
      if robot_dir == 2:
            kletka = cv2.rotate(kletka, cv2.ROTATE_90_CLOCKWISE)
      elif robot_dir == 3:
            kletka = cv2.rotate(kletka, cv2.ROTATE_180)
      elif robot_dir == 4:
            kletka = cv2.rotate(kletka, cv2.ROTATE_90_COUNTERCLOCKWISE)
      camera = kletka  # detect_cell смотрит в camera
      return detect_cell()


def scan_ahead_4():
      # сканируем 4 клетки буквой Т перед роботом:
      # 0 - слева спереди, 1 - спереди, 2 - справа спереди, 3 - через одну спереди
      view = camera_view()
      cells = [view[80:160, 0:80], view[80:160, 80:160], view[80:160, 160:240], view[0:80, 80:160]]

      # если датчики видят бортик, клетки за ним не считываем, чтобы не распознать их неправильно
      left, front, right = red_sensors()
      skip = [False, False, False, False]
      if front == True:
            skip = [True, True, True, True]  # бортик спереди - вся Т за полем
      if left == True:
            skip[0] = True
      if right == True:
            skip[2] = True

      # дальнюю клетку датчики не видят: если у ее ближнего к роботу края красная полоса,
      # значит она за краем поля - тоже не считываем
      if dolya_krasnogo(view[70:80, 80:160]) > 0.9:  # у бортика 1.0, у клеток поля не больше 0.17
            skip[3] = True

      imgs = []
      codes = []  # коды клеток для slam_map, 0 - клетку не считывали
      for i in range(4):
            if skip[i] == True:
                  imgs.append(None)
                  codes.append(0)
                  continue
            code = raspoznat_kletku(cells[i])
            img = cv2.imread("img/" + str(code) + ".png")
            if img is None:
                  img = camera  # картинки для такого кода нет - показываем саму клетку
            imgs.append(img)
            codes.append(code)
      return imgs, codes


def draw_scan_panel(imgs):
      SCAN_CELL = 40
      panel_x0 = 690
      panel_w = 120
      panel_y0 = 0
      panel_h = 690

      base_x = panel_x0 + (panel_w - SCAN_CELL * 3) // 2
      base_y = panel_y0 + (panel_h - SCAN_CELL * 3) // 2  # 3 ряда: через одну, спереди, робот

      slots = [
            (base_x, base_y + SCAN_CELL),
            (base_x + SCAN_CELL, base_y + SCAN_CELL),
            (base_x + 2 * SCAN_CELL, base_y + SCAN_CELL),
            (base_x + SCAN_CELL, base_y),
      ]

      if robot_dir == 1:
            rot = None
      elif robot_dir == 2:
            rot = cv2.ROTATE_90_COUNTERCLOCKWISE
      elif robot_dir == 3:
            rot = cv2.ROTATE_180
      else:
            rot = cv2.ROTATE_90_CLOCKWISE

      images_array[0:690, 690:810] = (0, 0, 0)

      for i, img in enumerate(imgs):
            if img is not None and i < len(slots):
                  tx, ty = slots[i]
                  resized = cv2.resize(img, (SCAN_CELL, SCAN_CELL))
                  if rot is not None:
                        resized = cv2.rotate(resized, rot)
                  images_array[ty:ty + SCAN_CELL, tx:tx + SCAN_CELL] = resized

      # рисуем робота под буквой Т, нос (желтый) смотрит вверх
      rx = base_x + 40
      ry = base_y + 80
      robot_img = cv2.imread("img/robot.png")
      images_array[ry:ry + 40, rx:rx + 40] = cv2.resize(robot_img, (40, 40))

      # область интереса - клетка прямо перед роботом, внизу панели
      roi = camera_view()[80:160, 80:160]
      images_array[600:680, 710:790] = roi

      draw_metrika()  # панель очищена - рисуем метрику заново (там же imshow)


def dolya_krasnogo(kusok):
      # какая часть картинки красная: от 0 до 1
      hsv = cv2.cvtColor(kusok, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(hsv, min_red1, max_red1) + cv2.inRange(hsv, min_red2, max_red2)
      return cv2.countNonZero(mask) / mask.size


def red_sensors():
      # 3 маленьких датчика 8x8 пикселей: ровно слева, ровно спереди и ровно справа от робота
      # каждый датчик наполовину на клетке робота, наполовину на соседней клетке
      # возвращает [слева, спереди, справа]: True - датчик видит красный бортик
      view = camera_view()  # робот в середине нижнего ряда, клетка робота view[160:240, 80:160]
      centers = [(200, 80), (160, 120), (200, 160)]  # центры датчиков (y, x): слева, спереди, справа
      result = []
      for cy, cx in centers:
            kusok = view[cy - 4:cy + 4, cx - 4:cx + 4]
            result.append(dolya_krasnogo(kusok) > 0.4)  # у бортика 0.5-0.73, у клеток поля не больше 0.23
      return result


def sensor_napravleniya(d):
      # куда смотрят датчики [слева, спереди, справа] при направлении робота d, как (dx, dy)
      if d == 1:
            fx, fy = 0, -1
      elif d == 2:
            fx, fy = 1, 0
      elif d == 3:
            fx, fy = 0, 1
      else:
            fx, fy = -1, 0
      return [(fy, -fx), (fx, fy), (-fy, fx)]


def obnovit_granitsy(sy, sx, sdir, sensors):
      # датчик видит бортик -> знаем край поля в slam_map
      # поле всегда 8x8, поэтому сразу знаем и противоположный край
      napravleniya = sensor_napravleniya(sdir)
      for i in range(3):
            if sensors[i] == True:
                  vx, vy = napravleniya[i]
                  if vy == -1:  # бортик сверху: строка робота - верхняя строка поля
                        granitsy["top"] = sy
                        granitsy["bottom"] = sy + 7
                  elif vy == 1:  # бортик снизу
                        granitsy["bottom"] = sy
                        granitsy["top"] = sy - 7
                  elif vx == -1:  # бортик слева
                        granitsy["left"] = sx
                        granitsy["right"] = sx + 7
                  else:  # бортик справа
                        granitsy["right"] = sx
                        granitsy["left"] = sx - 7


def v_pole_slam(y, x):
      # клетка (y, x) slam_map может быть клеткой поля: внутри карты 17x17 и внутри известных краев
      if y < 0 or y > 16 or x < 0 or x > 16:
            return False
      if granitsy["top"] is not None and (y < granitsy["top"] or y > granitsy["bottom"]):
            return False
      if granitsy["left"] is not None and (x < granitsy["left"] or x > granitsy["right"]):
            return False
      return True


def mozhno_ehat(y, x, ny, nx, sy, sx):
      # можно ли по slam_map проехать из клетки (y, x) в соседнюю (ny, nx) по правилам dict_p
      # (sy, sx) - где стоит робот: если клетку под ним не распознали, считаем ее полом 1 этажа
      if not v_pole_slam(ny, nx):
            return False
      kod = slam_map[y][x]
      if y == sy and x == sx and kod == 0:
            kod = 1
      razresheno = dict_p.get(str(kod))
      if razresheno is None:
            return False  # труба, подставка или непонятная клетка - через нее не едем
      if ny < y:
            k = 0
      elif nx > x:
            k = 1
      elif ny > y:
            k = 2
      else:
            k = 3
      return slam_map[ny][nx] in razresheno[k]


def na_panduse(y, x):
      # клетка (y, x) slam_map - пандус: на нем робот не останавливается, не поворачивает и не сканирует
      return slam_map[y][x] in (61, 62, 63, 64)


def vidit_neizvestnoe(y, x, d):
      # увидит ли камера (буква Т) из клетки (y, x) при направлении d хоть одну неизвестную клетку поля
      if na_panduse(y, x):
            return False  # с пандуса не сканируем
      for dx, dy in offsets_T[d]:
            ny = y + dy
            nx = x + dx
            if v_pole_slam(ny, nx) and slam_map[ny][nx] == 0 and (ny, nx) not in plohie:
                  return True
      return False


def plan_issledovaniya(sy, sx, sdir):
      # поиск в ширину по состояниям (клетка, направление). Каждое действие стоит 1:
      # шаг вперед или поворот на 90 градусов. Так робот не делает лишних поворотов.
      # Цель - состояние, из которого камера увидит неизвестную клетку поля.
      # возвращает план [(y, x, d), ...] от робота до цели, или None, если смотреть больше нечего
      shagi = {1: (-1, 0), 2: (0, 1), 3: (1, 0), 4: (0, -1)}
      otkuda = {(sy, sx, sdir): None}
      ochered = [(sy, sx, sdir)]
      i = 0
      while i < len(ochered):
            y, x, d = ochered[i]
            i += 1
            if vidit_neizvestnoe(y, x, d):
                  plan = [(y, x, d)]
                  while otkuda[(y, x, d)] is not None:
                        y, x, d = otkuda[(y, x, d)]
                        plan.append((y, x, d))
                  plan.reverse()
                  return plan

            sosedi = []
            ny = y + shagi[d][0]
            nx = x + shagi[d][1]
            if mozhno_ehat(y, x, ny, nx, sy, sx):
                  sosedi.append((ny, nx, d))      # вперед
            if not na_panduse(y, x):              # на пандусе только вперед, без поворотов
                  sosedi.append((y, x, d % 4 + 1))       # поворот направо
                  sosedi.append((y, x, (d + 2) % 4 + 1)) # поворот налево
            for s in sosedi:
                  if s not in otkuda:
                        otkuda[s] = (y, x, d)
                        ochered.append(s)
      return None


def kletki_plana(plan):
      # клетки, через которые проходит план (без повторов) - чтобы нарисовать путь на карте
      if plan is None:
            return None
      put = []
      for y, x, d in plan:
            if (y, x) not in put:
                  put.append((y, x))
      return put


def vse_naideno(sy, sx):
      # можно заканчивать исследование: известны края поля, найдены 3 трубы и подставка,
      # и до каждой трубы и до подставки можно доехать по уже известным клеткам
      if granitsy["top"] is None or granitsy["left"] is None:
            return False
      tubes = []
      stands = []
      for y in range(17):
            for x in range(17):
                  if slam_map[y][x] in (151, 152, 251, 252, 121, 122, 221, 222):
                        tubes.append((y, x))
                  if slam_map[y][x] in (31, 32, 33, 34):
                        stands.append((y, x))
      if len(tubes) != 3 or len(stands) < len(tubes):  # на подставке нужно место под каждую трубу
            return False

      # куда можно доехать от робота по известным клеткам
      byl = [[False for _ in range(17)] for _ in range(17)]
      byl[sy][sx] = True
      ochered = [(sy, sx)]
      i = 0
      while i < len(ochered):
            y, x = ochered[i]
            i += 1
            for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                  ny = y + dy
                  nx = x + dx
                  if mozhno_ehat(y, x, ny, nx, sy, sx) and not byl[ny][nx]:
                        byl[ny][nx] = True
                        ochered.append((ny, nx))

      # к трубе и подставке подъезжаем сбоку, с разрешенной стороны (dict_tube, как в FindPath)
      celi = tubes + [stands[len(stands) // 2]]  # calc_path берет среднюю клетку подставки
      for ty, tx in celi:
            pod = dict_tube.get(str(slam_map[ty][tx]))
            mozhno = False
            for k, (dy, dx) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
                  ny = ty + dy
                  nx = tx + dx
                  if v_pole_slam(ny, nx) and byl[ny][nx] and slam_map[ny][nx] in pod[k]:
                        mozhno = True
            if not mozhno:
                  return False
      return True


def draw_sensors():
      # рамки датчиков вокруг робота на поле и телеметрия между картами
      sensors = red_sensors()

      # рамки датчиков на поле (зеленые)
      px = robot_pos[1] * 80 + PAD + 40  # центр клетки робота
      py = robot_pos[0] * 80 + PAD + 40
      napravleniya = sensor_napravleniya(robot_dir)  # слева, спереди, справа
      for vx, vy in napravleniya:
            sx = px + vx * 40
            sy = py + vy * 40
            cv2.rectangle(images_array, (sx - 4, sy - 4), (sx + 4, sy + 4), (0, 255, 0), 1)

      # телеметрия: 3 прямоугольника между картами, красный - датчик видит бортик
      names = ["L", "F", "R"]
      images_array[10:100, 690:810] = (0, 0, 0)
      for i in range(3):
            x = 698 + i * 38
            if sensors[i] == True:
                  color = (0, 0, 255)
            else:
                  color = (60, 60, 60)
            cv2.rectangle(images_array, (x, 30), (x + 28, 58), color, -1)
            cv2.rectangle(images_array, (x, 30), (x + 28, 58), (255, 255, 255), 1)
            cv2.putText(images_array, names[i], (x + 9, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

      cv2.imshow("pole", images_array)
      return sensors


def key_drive(t=1):
      global robot_pos, robot_dir

      K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESC, K_SPACE = 82, 84, 81, 83, 27, 32
      F_UP, F_DOWN, F_LEFT, F_RIGHT, F_SPACE = 0x260000, 0x280000, 0x250000, 0x270000, 0x320000

      show_pole()
      draw_sensors()
      cv2.waitKey(1)

      while True:
            try:
                  raw = cv2.waitKeyEx(50)
            except AttributeError:
                  raw = cv2.waitKey(50)

            if raw == -1:
                  continue

            short = raw & 0xFF

            action = None
            if raw == F_UP or short == K_UP:
                  action = "up"
            elif raw == F_DOWN or short == K_DOWN:
                  action = "down"
            elif raw == F_LEFT or short == K_LEFT:
                  action = "left"
            elif raw == F_RIGHT or short == K_RIGHT:
                  action = "right"
            elif short == K_ESC or raw == K_ESC:
                  action = "esc"
            elif raw == F_SPACE or short == K_SPACE:
                  action = "space"

            if action is None:
                  continue

            if action == "esc":
                  break

            elif action == "left":
                  rotate(0)
                  show_pole()
                  draw_scan_panel(scan_ahead_4()[0])
                  draw_sensors()  # после каждого движения проверяем бортики датчиками

            elif action == "right":
                  rotate(1)
                  show_pole()
                  draw_scan_panel(scan_ahead_4()[0])
                  draw_sensors()

            elif action == "space":
                  draw_scan_panel(scan_ahead_4()[0])
                  draw_sensors()

            elif action in ("up", "down"):
                  sign = +1 if action == "up" else -1

                  dy = dx = 0
                  if robot_dir == 1:
                        dy = -1
                  elif robot_dir == 3:
                        dy = +1
                  elif robot_dir == 2:
                        dx = +1
                  elif robot_dir == 4:
                        dx = -1
                  dy *= sign
                  dx *= sign

                  new_y = robot_pos[0] + dy
                  new_x = robot_pos[1] + dx

                  if not (0 <= new_y < GRID and 0 <= new_x < GRID):
                        continue

                  start_cell = str(map_draw[robot_pos[0]][robot_pos[1]])
                  target_cell = int(map_draw[new_y][new_x])

                  if dy == -1:
                        idx = 0
                  elif dx == +1:
                        idx = 1
                  elif dy == +1:
                        idx = 2
                  else:
                        idx = 3

                  allowed = dict_p.get(start_cell)
                  if allowed is None or target_cell not in allowed[idx]:
                        continue

                  delay = t + 10 if target_cell in (61, 62, 63, 64) else t
                  robot_move(new_y, new_x, delay)
                  show_pole()
                  draw_scan_panel(scan_ahead_4()[0])
                  draw_sensors()
                  cv2.waitKey(1)

def find_col(col):
      global camera

      if camera is None:
            print("camera пустая — сначала нажмите SPACE для сканирования")
            return None

      if col == 2:
            hsv = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, min_blue, max_blue)
      elif col == 3:
            hsv = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, min_green, max_green)
      elif col == 5:
            hsv = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(hsv, min_red1, max_red1)
            mask2 = cv2.inRange(hsv, min_red2, max_red2)
            mask = mask1 + mask2
      elif col == 6:
            hsv = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, min_white, max_white)
      elif col == 1:
            hsv = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, min_black, max_black)
      elif col == 4:
            hsv = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, min_yellow, max_yellow)

      kernel = np.ones((5, 5), np.uint8)
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # убирает мелкие точки
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # закрывает дырки

      # 3. Ищем контуры
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # 4. Рисуем прямоугольники вокруг достаточно крупных контуров
      result = camera.copy()
      found = []
      xm,ym,wm,hm,aream = 0,0,0,0,0
      for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # отсекаем мелкие артефакты — подберите под масштаб
                  x, y, w, h = cv2.boundingRect(cnt)  # прямоугольник, описывающий контур
                  if col != 6 and col !=1:
                        if w*h > wm*hm:
                              xm,ym,wm,hm = x, y, w, h
                              aream = area
                  else:
                        if w * h > wm * hm:
                              xm, ym, wm, hm = x, y, w, h
                        aream += area

      cv2.rectangle(result, (xm, ym), (xm + wm, ym + hm), (0, 255, 255), 2)

      # центр объекта — пригодится для навигации
      cx, cy = xm + wm // 2, ym + hm // 2
      cv2.circle(result, (cx, cy), 4, (255, 0, 0), -1)
      # found = ({"rect": (xm, ym, wm, hm), "center": (cx, cy), "area": area})

      # cv2.imshow("green mask", mask)
      # cv2.imshow("green found", result)

      return [xm,ym,wm,hm,aream]

def detect_cell():
      global kletka
      kletka = 0
      green = find_col(3)
      black = find_col(1)
      white = find_col(6)
      blue = find_col(2)
      red = find_col(5)
      yellow = find_col(4)
      if green[4] > 0:#находим зеленые подставки
            if green[3] > green[2]:
                  if green[0]<40: kletka = 32
                  else: kletka = 34
            else:
                  if green[1]<40: kletka = 33
                  else: kletka = 31
      elif red[4] > 0 and blue[4]> 0:#пандусы
            if red[1]+20 < blue[1]: kletka = 62
            elif red[1]> blue[1]+20: kletka = 64
            elif red[0]+20 < blue[0]: kletka = 61
            elif red[0] >blue[0]+20: kletka = 63

      elif red[4]>0:#красные трубы
            if red[3]>red[2]:
                  if white[4] > black[4]: kletka = 152
                  elif white[4] < black[4]: kletka = 252
            elif red[2] > red[3]:
                  if white[4] > black[4]: kletka = 151
                  elif white[4] < black[4]: kletka = 251

      elif blue[4]>0:#синие трубы
            if blue[3]>blue[2]:
                  if white[4] > black[4]: kletka = 122
                  elif white[4] < black[4]: kletka = 222
            elif blue[2] > blue[3]:
                  if white[4] > black[4]: kletka = 121
                  elif white[4] < black[4]: kletka = 221
      elif black[4]>white[4]: kletka = 2#2 этаж
      else: kletka = 1#1 этаж

      if yellow[4]>0:
            if yellow[3]>yellow[2]:
                  if red[0]<40:
                        kletka = 1511
                  else: kletka = 153
            else:
                  if red[1]<40: kletka = 152
                  else: kletka = 154

      return kletka

# где на карте клетки буквы Т (dx, dy) для каждого направления робота
# порядок: слева спереди, спереди, справа спереди, через одну спереди
offsets_T = {
      1: [(-1, -1), (0, -1), (1, -1), (0, -2)],
      2: [(1, -1), (1, 0), (1, 1), (2, 0)],
      3: [(1, 1), (0, 1), (-1, 1), (0, 2)],
      4: [(-1, 1), (-1, 0), (-1, -1), (-2, 0)]
}
polosy = []   # бортики с датчиков: (y, x, vx, vy) - у клетки (y, x) в сторону (vx, vy)
plohie = []   # клетки, на которые робот смотрел, но так и не распознал - больше к ним не едем


def slam_skan(sy, sx):
      # робот в клетке (sy, sx) slam_map смотрит по robot_dir:
      # сканирует Т, записывает коды в slam_map, датчиками ищет бортики
      imgs, codes = scan_ahead_4()
      for i in range(4):
            if imgs[i] is None:  # клетка за бортиком, не считывали
                  continue
            dx, dy = offsets_T[robot_dir][i]
            slam_map[sy + dy][sx + dx] = codes[i]

      sensors = red_sensors()  # [слева, спереди, справа]
      obnovit_granitsy(sy, sx, robot_dir, sensors)
      napravleniya = sensor_napravleniya(robot_dir)
      for i in range(3):
            if sensors[i] == True:
                  vx, vy = napravleniya[i]
                  if (sy, sx, vx, vy) not in polosy:
                        polosy.append((sy, sx, vx, vy))
      return imgs


def draw_slam_map(sy, sx, put):
      # рисуем вторую карту заново: известные клетки, бортики, края поля, путь и робота
      S = 40
      images_array[0:690, 810:1500] = (0, 0, 0)
      for y in range(17):
            for x in range(17):
                  if slam_map[y][x] != 0:
                        img = cv2.imread("img/" + str(slam_map[y][x]) + ".png")
                        if img is not None:
                              images_array[y * S:y * S + S, 810 + x * S:810 + x * S + S] = cv2.resize(img, (S, S))

      # бортики красной полосой у края клетки, как на настоящем поле
      T = 12  # толщина полосы: бортик 25 px на клетку 80 px, у нас клетка 40 px
      for y, x, vx, vy in polosy:
            x0 = 810 + x * S
            y0 = y * S
            if vx == 1:
                  images_array[y0:y0 + S, x0 + S:x0 + S + T] = (0, 0, 255)
            elif vx == -1:
                  images_array[y0:y0 + S, x0 - T:x0] = (0, 0, 255)
            elif vy == 1:
                  images_array[y0 + S:y0 + S + T, x0:x0 + S] = (0, 0, 255)
            else:
                  images_array[y0 - T:y0, x0:x0 + S] = (0, 0, 255)

      # известные края поля тонкими красными линиями через всю карту
      if granitsy["top"] is not None:
            y1 = granitsy["top"] * S
            y2 = (granitsy["bottom"] + 1) * S
            cv2.line(images_array, (810, y1), (810 + 17 * S, y1), (0, 0, 255), 2)
            cv2.line(images_array, (810, y2), (810 + 17 * S, y2), (0, 0, 255), 2)
      if granitsy["left"] is not None:
            x1 = 810 + granitsy["left"] * S
            x2 = 810 + (granitsy["right"] + 1) * S
            cv2.line(images_array, (x1, 0), (x1, 17 * S), (0, 0, 255), 2)
            cv2.line(images_array, (x2, 0), (x2, 17 * S), (0, 0, 255), 2)

      # путь до неизвестного: зеленые точки, цель - синяя рамка
      if put is not None:
            for y, x in put:
                  cv2.circle(images_array, (810 + x * S + S // 2, y * S + S // 2), 5, (0, 255, 0), -1)
            ty, tx = put[-1]
            cv2.rectangle(images_array, (810 + tx * S, ty * S), (810 + tx * S + S - 1, ty * S + S - 1), (255, 0, 0), 2)

      # робот, повернут как сейчас
      images_array[sy * S:sy * S + S, 810 + sx * S:810 + sx * S + S] = cv2.resize(robot, (S, S))


def pokazat_vse(sy, sx, put, imgs):
      # обновляем окно: поле, вторую карту, панель скана и датчики
      draw_slam_map(sy, sx, put)
      show_pole()
      draw_scan_panel(imgs)
      draw_sensors()


def print_slam_map(sy, sx):
      # печатаем, что робот узнал (0 - не знаем, R - сам робот)
      print("границы поля в slam_map:", granitsy)
      if granitsy["top"] is not None and granitsy["left"] is not None:
            print("робот на поле в клетке (y, x):", sy - granitsy["top"], sx - granitsy["left"])
      for y in range(17):
            stroka = ""
            for x in range(17):
                  if y == sy and x == sx:
                        stroka += "   R"
                  else:
                        stroka += "%4d" % slam_map[y][x]
            print(stroka)


def skan_pod_soboi():
      # сканируем клетку, на которой стоит робот (в camera_view это середина нижнего ряда)
      return raspoznat_kletku(camera_view()[160:240, 80:160])


def slam_step1():
      # робот крутится на месте и осматривается; он стоит в центре slam_map (8, 8)
      global robot_dir
      robot_dir = 1
      draw_robot()
      show_pole()
      cv2.waitKey(0)  # ждём любую клавишу, потом робот сам крутится и считывает

      slam_map[8][8] = skan_pod_soboi()  # сначала клетка под собой
      print("робот стоит на клетке:", slam_map[8][8])

      for _ in range(4):
            imgs = slam_skan(8, 8)
            pokazat_vse(8, 8, None, imgs)
            cv2.waitKey(500)  # пауза, чтобы было видно скан
            rotate(1)
      # после 4 поворотов робот снова смотрит вверх

      plan = plan_issledovaniya(8, 8, robot_dir)
      print("план до неизвестного:", plan)
      draw_slam_map(8, 8, kletki_plana(plan))
      show_pole()
      cv2.waitKey(1)
      print("slam_map после осмотра:")
      print_slam_map(8, 8)


def povernut_v(nado):
      # поворачиваем робота в направление nado (1 - вверх, 2 - вправо, 3 - вниз, 4 - влево)
      r = rotate_pro(nado)
      if r != 59:  # 59 - уже смотрим куда надо
            rotate(r - 60)


def slam_explore(t=300):
      # главный цикл SLAM: по плану делаем одно действие (шаг или поворот), сканируем, планируем снова
      # робот знает только себя в slam_map (sy, sx) и свое направление robot_dir
      sy, sx = 8, 8
      imgs = [None, None, None, None]
      shagov = 0
      while shagov < 300:  # защита от вечного цикла
            if not na_panduse(sy, sx) and vse_naideno(sy, sx):  # на пандусе не останавливаемся
                  print("slam_explore: трубы и подставка найдены, до них можно доехать, шагов:", shagov)
                  break
            plan = plan_issledovaniya(sy, sx, robot_dir)
            if plan is None:
                  print("slam_explore: всё, что можно, осмотрено, шагов:", shagov)
                  break

            if len(plan) > 1:
                  ny, nx, nd = plan[1]
                  if nd != robot_dir:
                        povernut_v(nd)
                  else:
                        # на пандус и с пандуса едем медленно
                        if na_panduse(sy, sx) or na_panduse(ny, nx):
                              skorost = 15
                        else:
                              skorost = 1
                        # это "мир": настоящий робот на поле едет туда же, куда робот думает
                        robot_move(robot_pos[0] + ny - sy, robot_pos[1] + nx - sx, skorost)
                        sy, sx = ny, nx
                  shagov += 1
            if na_panduse(sy, sx):
                  continue  # на пандусе не сканируем и не останавливаемся - сразу едем дальше
            imgs = slam_skan(sy, sx)

            # клетки Т, которые после скана остались неизвестными, больше не ждем (не распознали)
            for dx, dy in offsets_T[robot_dir]:
                  ny = sy + dy
                  nx = sx + dx
                  if v_pole_slam(ny, nx) and slam_map[ny][nx] == 0 and (ny, nx) not in plohie:
                        plohie.append((ny, nx))

            pokazat_vse(sy, sx, kletki_plana(plan_issledovaniya(sy, sx, robot_dir)), imgs)
            cv2.waitKey(t)

      print("slam_map после исследования:")
      print_slam_map(sy, sx)
      return sy, sx


def vyrezat_8x8():
      # вырезаем поле 8x8 из slam_map по найденным краям поля
      karta = []
      for y in range(8):
            stroka = []
            for x in range(8):
                  kod = slam_map[granitsy["top"] + y][granitsy["left"] + x]
                  if kod == 0:
                        # неизвестную клетку пишем -1: в dict_p и dict_tube [0] значит "нельзя",
                        # и 0 там совпал бы с этим "нельзя" - Wave и FindPath поехали бы в неизвестное
                        kod = -1
                  stroka.append(kod)
            karta.append(stroka)
      return karta


def slam_zadanie(sy, sx):
      # этап 5: по карте, которую робот собрал сам, едем по трубам к подставке (как sputnik_go в simulator_sputnik.py)
      global map_draw, pole_draw
      if granitsy["top"] is None or granitsy["left"] is None:
            print("slam_zadanie: края поля не найдены - не знаю, где я на поле")
            return

      map_draw = vyrezat_8x8()
      ry = sy - granitsy["top"]  # где робот на поле по SLAM
      rx = sx - granitsy["left"]
      print("slam_zadanie: карта поля, которую собрал робот:")
      for stroka in map_draw:
            print(" ".join("%4d" % v for v in stroka))
      print("робот по SLAM в клетке", [ry, rx], ", на самом деле", robot_pos)

      # трубы и подставка из собранной карты
      tubes = []
      stands = []
      for y in range(8):
            for x in range(8):
                  if map_draw[y][x] in (151, 152, 251, 252, 121, 122, 221, 222):
                        tubes.append([y, x])
                  if map_draw[y][x] in (31, 32, 33, 34):
                        stands.append([y, x])
      if len(tubes) != 3 or len(stands) == 0:  # calc_path перебирает ровно 3 трубы
            print("slam_zadanie: нужно 3 трубы и подставка, найдено труб", len(tubes), ", подставок", len(stands))
            return
      trubi[:] = [[ry, rx]] + tubes + [stands[len(stands) // 2]]
      fin_path.clear()
      v_robote.clear()
      sobrannye.clear()
      calc_path()

      # показываем маршрут на поле
      pole_draw = pole.copy()
      draw_robot()
      size = [20, 15, 10, 5]
      color = [(0, 0, 255), (0, 255, 255), (255, 0, 0), (0, 255, 0)]
      for j in range(len(fin_path)):
            for y, x in fin_path[j]:
                  cv2.circle(pole_draw, (x * CELL + PAD + 40, y * CELL + PAD + 40), size[j], color[j], -1)
      show_pole()
      cv2.waitKey(1000)

      # едем по маршруту: к каждой трубе, потом к подставке
      for j in range(len(fin_path)):
            if fin_path[j][0] == [-1, -1]:  # FindPath не нашел путь (calc_path дописывает цель в конец)
                  print("slam_zadanie: участок", j, "не найден, пропускаю")
                  continue
            make_drive(fin_path[j])
            drive(1)
            if j < 3:  # первые 3 участка ведут к трубам - забираем трубу
                  ty, tx = fin_path[j][-1]  # последняя клетка участка - сама труба
                  zabrat_trubu(ty, tx)
            else:  # последний участок ведет к зеленой подставке - выгружаем трубы
                  vygruzit_truby()
            # вторая карта: робот на новом месте, забранные трубы уже пустые подставки
            draw_slam_map(granitsy["top"] + robot_pos[0], granitsy["left"] + robot_pos[1], None)
            draw_robot()
            show_pole()
            cv2.waitKey(500)
      print("slam_zadanie: готово, робот в", robot_pos)


def zamenit_kletku(ty, tx, novyi):
      # клетка (ty, tx) поля стала другой (новый код novyi): меняем ее на поле, в map_draw и в slam_map
      img = cv2.imread("img/" + str(novyi) + ".png")
      if img is None:
            print("нет картинки img/" + str(novyi) + ".png")
            return False
      y0 = ty * CELL + PAD
      x0 = tx * CELL + PAD
      pole[y0:y0 + CELL, x0:x0 + CELL] = img       # самое поле - его видит камера
      pole_draw[y0:y0 + CELL, x0:x0 + CELL] = img  # то, что нарисовано в окне
      map_draw[ty][tx] = novyi
      slam_map[granitsy["top"] + ty][granitsy["left"] + tx] = novyi  # карта робота (вторая карта)
      return True


v_robote = []    # коды труб, которые робот сейчас везет
sobrannye = []   # коды труб в том порядке, в каком робот их собрал (не меняется при выгрузке)


def cvet_truby(kod):
      # цвет трубы для рисования: 2 - синяя, 5 - красная (труба 151 -> 5, подставка с трубой 315 -> 5)
      if kod >= 300:
            c = kod % 10
      else:
            c = (kod // 10) % 10
      if c == 2:
            return (204, 72, 63)
      return (36, 28, 237)


def zabrat_trubu(ty, tx):
      # робот забрал трубу из клетки (ty, tx) поля: на ее месте остается пустая подставка
      # код пустой подставки = код трубы с 0 на конце (121 -> 1210)
      kod = map_draw[ty][tx]
      if kod not in (151, 152, 251, 252, 121, 122, 221, 222):
            return
      if zamenit_kletku(ty, tx, kod * 10):
            v_robote.append(kod)
            sobrannye.append(kod)
            print("забрали трубу", kod, "из клетки", [ty, tx], "- везем", v_robote)
            draw_metrika()


def poryadok_vygruzki(truby):
      # по регламенту: две трубы одного цвета по бокам, труба другого цвета посередине
      # возвращает трубы в порядке клеток подставки: [бок, середина, бок]
      if len(truby) != 3:
            return truby[:]
      cveta = [(k // 10) % 10 for k in truby]
      for i in range(3):
            if cveta.count(cveta[i]) == 1:  # эта труба одна такого цвета - ее в середину
                  boka = [truby[j] for j in range(3) if j != i]
                  return [boka[0], truby[i], boka[1]]
      return truby[:]  # все три одного цвета - кладем как есть


def vygruzit_truby():
      # трубы лежат в роботе друг на друге: снять можно только верхнюю - последнюю собранную.
      # Регламент говорит, какого цвета труба должна лежать в каждой клетке подставки,
      # поэтому берем верхнюю трубу и везем ее на свободную клетку подставки ее цвета.
      # код подставки с трубой = код подставки + цвет трубы (31 + синяя -> 312, 31 + красная -> 315)
      stands = []
      for y in range(8):
            for x in range(8):
                  if map_draw[y][x] in (31, 32, 33, 34):
                        stands.append([y, x])  # по порядку: слева направо (или сверху вниз)
      plan = poryadok_vygruzki(v_robote)
      print("по регламенту на подставке будет:", plan)
      cveta_mest = [(k // 10) % 10 for k in plan]          # какой цвет нужен в каждой клетке подставки
      svobodno = list(range(min(len(stands), len(plan))))  # номера свободных клеток подставки

      while len(v_robote) > 0:
            kod = v_robote[-1]       # верхняя труба
            cvet = (kod // 10) % 10  # средняя цифра кода трубы: 2 - синяя, 5 - красная
            # свободная клетка нужного цвета, ближайшая к роботу
            mesto = None
            for i in svobodno:
                  if cveta_mest[i] == cvet:
                        d = abs(stands[i][0] - robot_pos[0]) + abs(stands[i][1] - robot_pos[1])
                        if mesto is None or d < luchshee:
                              mesto = i
                              luchshee = d
            if mesto is None:
                  print("vygruzit_truby: на подставке нет места для трубы", kod, ", в роботе остались", v_robote)
                  break
            y, x = stands[mesto]

            # подъезжаем к этой клетке подставки так же, как calc_path подъезжает к трубам
            Wave(robot_pos[0], robot_pos[1])
            der, _ = FindPath(y, x)
            if der[0] == [-1, -1]:
                  print("vygruzit_truby: не доехать до клетки подставки", [y, x], ", в роботе остались", v_robote)
                  break
            der.append([y, x])
            make_drive(der)  # последний поворот - лицом к подставке
            drive(1)

            if not zamenit_kletku(y, x, map_draw[y][x] * 10 + cvet):
                  break
            svobodno.remove(mesto)
            v_robote.pop()
            print("сняли сверху трубу", kod, "и положили на подставку", [y, x])
            draw_slam_map(granitsy["top"] + robot_pos[0], granitsy["left"] + robot_pos[1], None)
            draw_robot()
            show_pole()
            draw_metrika()
            cv2.waitKey(500)
      print("порядок сбора труб:", sobrannye)


def draw_metrika():
      # метрика посередине экрана (между картами): трубы в порядке сбора и что лежит на подставке
      white = (255, 255, 255)
      images_array[100:280, 690:810] = (0, 0, 0)
      cv2.putText(images_array, "Sobrano " + str(len(sobrannye)) + "/3", (695, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.45, white, 1)
      for i in range(len(sobrannye)):
            x = 698 + i * 38
            cv2.rectangle(images_array, (x, 130), (x + 28, 158), cvet_truby(sobrannye[i]), -1)
            cv2.putText(images_array, str(i + 1), (x + 9, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, white, 1)

      # подставка по карте робота: серый - пусто, цвет - лежит труба
      cv2.putText(images_array, "Podstavka", (695, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.45, white, 1)
      kletki = []
      for y in range(17):
            for x in range(17):
                  if slam_map[y][x] in (31, 32, 33, 34) or 300 <= slam_map[y][x] < 400:
                        kletki.append(slam_map[y][x])
      for i in range(min(3, len(kletki))):
            x = 698 + i * 38
            if kletki[i] >= 300:
                  color = cvet_truby(kletki[i])
            else:
                  color = (60, 60, 60)
            cv2.rectangle(images_array, (x, 200), (x + 28, 228), color, -1)
            cv2.rectangle(images_array, (x, 200), (x + 28, 228), (34, 177, 76), 2)  # зеленая рамка - подставка

      # что лежит в роботе: слева нижняя труба, справа верхняя (ее снимают первой)
      cv2.putText(images_array, "V robote", (695, 248), cv2.FONT_HERSHEY_SIMPLEX, 0.45, white, 1)
      for i in range(len(v_robote)):
            x = 698 + i * 38
            cv2.rectangle(images_array, (x, 256), (x + 28, 272), cvet_truby(v_robote[i]), -1)
      cv2.imshow("pole", images_array)


robot_pos = [5, 0]   # стартовая клетка (y, x)
draw_robot()
draw_pole()
show_pole()
cv2.waitKey(1)

slam_step1()     # робот осматривается вокруг себя
sy, sx = slam_explore()   # робот сам ездит и исследует поле
slam_zadanie(sy, sx)      # по собранной карте едет по трубам к подставке
key_drive(1)              # потом можно ездить с клавиатуры
cv2.waitKey(0)
