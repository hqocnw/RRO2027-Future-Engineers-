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



map= [[0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0]
      ]
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
bort_map = [[0 for _ in range(17)] for _ in range(17)]  # для углов: 0 - не знаем, 1 - поле, 2 - бортик

camera = 0

PAD  = 25
CELL = 80
GRID = 8

coords = 0

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


def Wave_pole():
      # wave_pole = pole.copy()
      # for i in range(8):
      #       for g in range(8):
      #             cv2.putText(wave_pole,str(wave[g][i]),(30+i*80,45+g*80),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
      # images_array[0:690,660:1300] = wave_pole
      pass


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

red_color = (36, 28, 237)  # цвет бортика


def camera_view():
      # что видит камера робота: 3 ряда по 3 клетки, нос робота смотрит вверх
      # робот стоит в середине нижнего ряда
      # за полем ничего нет (черное), бортик это красная полоса по краю поля
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


def detect_red():
      # ищем бортики только рядом с роботом: на следующей клетке спереди, слева и справа
      # бортик это красная полоса у края клетки, который ближе к роботу
      view = camera_view()
      left = view[160:240, 70:80]
      front = view[150:160, 80:160]
      right = view[160:240, 160:170]

      names = ["left", "front", "right"]
      strips = [left, front, right]
      red = {}
      for i in range(3):
            hsv = cv2.cvtColor(strips[i], cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(hsv, min_red1, max_red1)
            mask2 = cv2.inRange(hsv, min_red2, max_red2)
            mask = mask1 + mask2
            procent = cv2.countNonZero(mask) / mask.size
            if procent > 0.9:
                  red[names[i]] = True
            else:
                  red[names[i]] = False
      return red


def scan_ahead_4():
      # сканируем 4 клетки буквой Т перед роботом:
      # 0 - слева спереди, 1 - спереди, 2 - справа спереди, 3 - через одну спереди
      global camera
      view = camera_view()
      cells = [view[80:160, 0:80], view[80:160, 80:160], view[80:160, 160:240], view[0:80, 80:160]]

      # какие клетки за бортиком
      red = detect_red()
      out = [False, False, False, False]
      if red["front"] == True:
            out = [True, True, True, True]
      if red["left"] == True:
            out[0] = True
      if red["right"] == True:
            out[2] = True

      # дальняя клетка: если внизу у нее красная полоса, это не клетка поля - пропускаем
      # (бортиком ее не считаем, робот видит бортики только рядом с собой)
      hsv = cv2.cvtColor(view[70:80, 80:160], cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(hsv, min_red1, max_red1) + cv2.inRange(hsv, min_red2, max_red2)
      if cv2.countNonZero(mask) / mask.size > 0.9:
            out[3] = True

      saved = camera
      imgs = []
      for i in range(4):
            if out[i] == True:
                  imgs.append(None)
            else:
                  kletka = cells[i]
                  # поворачиваем клетку обратно, как она лежит на поле
                  if robot_dir == 2:
                        kletka = cv2.rotate(kletka, cv2.ROTATE_90_CLOCKWISE)
                  elif robot_dir == 3:
                        kletka = cv2.rotate(kletka, cv2.ROTATE_180)
                  elif robot_dir == 4:
                        kletka = cv2.rotate(kletka, cv2.ROTATE_90_COUNTERCLOCKWISE)
                  camera = kletka
                  img = cv2.imread("img/" + str(detect_cell()) + ".png")
                  if img is None:
                        img = camera
                  imgs.append(img)

      if imgs[1] is not None:
            camera = imgs[1]
      else:
            camera = saved
      return imgs


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

      # бортики рисуем красными линиями вокруг робота
      red = detect_red()
      if red["front"] == True:
            cv2.line(images_array, (rx, ry), (rx + 40, ry), red_color, 3)
      if red["left"] == True:
            cv2.line(images_array, (rx, ry), (rx, ry + 40), red_color, 3)
      if red["right"] == True:
            cv2.line(images_array, (rx + 40, ry), (rx + 40, ry + 40), red_color, 3)

      # область интереса - клетка прямо перед роботом, внизу панели
      roi = camera_view()[80:160, 80:160]
      images_array[600:680, 710:790] = roi

      cv2.imshow("pole", images_array)


def key_drive(t=1):
      global robot_pos, robot_dir

      K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESC, K_SPACE = 82, 84, 81, 83, 27, 32
      F_UP, F_DOWN, F_LEFT, F_RIGHT, F_SPACE = 0x260000, 0x280000, 0x250000, 0x270000, 0x320000

      show_pole()
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
                  draw_scan_panel(scan_ahead_4())


            elif action == "right":
                  rotate(1)
                  show_pole()
                  draw_scan_panel(scan_ahead_4())


            elif action == "space":
                  draw_scan_panel(scan_ahead_4())

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
                  draw_scan_panel(scan_ahead_4())
                  cv2.waitKey(1)

def scan():
    global camera
    y, x = robot_pos

    ny, nx = y, x
    if robot_dir == 1:   ny = y - 1
    elif robot_dir == 3: ny = y + 1
    elif robot_dir == 2: nx = x + 1
    elif robot_dir == 4: nx = x - 1

    if not (0 <= ny <= 7 and 0 <= nx <= 7):
        return  # смотрим в стену — сканировать нечего

    cell = map_draw[ny][nx]
    path = "img/" + str(cell) + ".png"
    camera = cv2.imread(path)
    if camera is None:
        print(f"WARNING: не удалось загрузить {path!r}")
        return
    # cv2.imshow("camera", camera)
    # cv2.moveWindow("camera", 100, 100)

def scan_cords(y,x):
      global camera
      cell = map_draw[y][x]
      path = "img/" + str(cell) + ".png"
      camera = cv2.imread(path)
      if camera is None:
            print(f"WARNING: не удалось загрузить {path!r}")
            return

def find_green():
    global camera

    if camera is None:
        print("camera пустая — сначала нажмите SPACE для сканирования")
        return None

    # 1. Переводим в HSV и строим маску по заданным границам
    hsv = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, min_green, max_green)

    # 2. Чистим маску от шума (морфология)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)  # убирает мелкие точки
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # закрывает дырки

    # 3. Ищем контуры
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. Рисуем прямоугольники вокруг достаточно крупных контуров
    result = camera.copy()
    found = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:          # отсекаем мелкие артефакты — подберите под масштаб
            continue

        x, y, w, h = cv2.boundingRect(cnt)   # прямоугольник, описывающий контур
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # центр объекта — пригодится для навигации
        cx, cy = x + w // 2, y + h // 2
        cv2.circle(result, (cx, cy), 4, (255, 0, 0), -1)
        found.append({"rect": (x, y, w, h), "center": (cx, cy), "area": area})

    # cv2.imshow("green mask", mask)
    cv2.imshow("green found", result)

    return found

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

def detect_robot():
      global camera, images_array,posu
      posu = 0
      saved_camera = camera
      for y in range(8):
            for x in range(8):
                  camera = pole_draw[y*CELL+PAD:(y+1)*CELL+PAD, x*CELL+PAD:(x+1)*CELL+PAD].copy()
                  cell_id = detect_cell()
                  if cell_id in (1511,152,153,154):
                        posu = cell_id
                        camera = saved_camera
                        return [y, x]
      camera = saved_camera
      return [0, 0]

def sputnik():
    global camera, images_array,new_map
    saved_camera = camera
    new_map = [[0 for _ in range(8)] for _ in range(8)]
    for y in range(8):
        for x in range(8):
            cell_img = pole[y*CELL+PAD:(y+1)*CELL+PAD, x*CELL+PAD:(x+1)*CELL+PAD].copy()
            camera = cell_img
            cell_id = detect_cell()
            new_map[y][x] = cell_id
    camera = saved_camera

    images_array[0:640, 660:1300] = (40, 40, 40)
    for y in range(8):
        for x in range(8):
            cell_id = new_map[y][x]
            path = f"img/{cell_id}.png"
            img = cv2.imread(path)
            ty = y * 80
            tx = 660 + x * 80
            images_array[ty:ty + 80, tx:tx + 80] = img
            cv2.putText(images_array, str(cell_id),(tx + 3, ty + 15),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 3)
    images_array = cv2.rectangle(images_array, (640, 0), (660, 640),(0, 250, 255), -1)
    cv2.imshow("pole", images_array)

    print("sputnik: новая карта")
    for row in new_map:
        print(" ".join(f"{v:>4}" for v in row))

    return new_map

def sputnik_go():
    global robot_dir, robot_pos, map_draw, new_map, pole_draw,posu

    # --- 1. Стартовое состояние ---
    draw_robot()
    draw_pole()
    show_pole()
    cv2.waitKey(1)

    # --- 2. Сканирование карты ---
    new_map = sputnik()

    # --- 3. Робот и его направление ---
    #     detect_cell() возвращает 1511/152/153/154 для маркера робота
    robot_pos = detect_robot()
    marker = posu

    if   marker == 1511: robot_dir = 1
    elif marker == 152:  robot_dir = 2
    elif marker == 153:  robot_dir = 3
    elif marker == 154:  robot_dir = 4
    else:
        print(f"WARN: робот не найден (marker={marker} в {robot_pos})")
        return

    # --- 4. Подмена карты на распознанную ---
    map_draw = [row[:] for row in new_map]
    pole_draw = pole.copy()
    draw_robot()
    draw_pole()
    show_pole()
    cv2.waitKey(1)

    # --- 5. Кратчайший маршрут по всем трубам ---
    tubes = [[y, x] for y in range(8) for x in range(8)
             if map_draw[y][x] in (151, 152, 251, 252, 121, 122, 221, 222)]
    stands = [[y, x] for y in range(8) for x in range(8) if map_draw[y][x] in (31, 32, 33, 34)]
    if len(tubes) != 3 or not stands:  # calc_path перебирает ровно 3 трубы
        print(f"WARN: нужно 3 трубы и подставка, найдено труб={len(tubes)}, подставок={len(stands)}")
        return
    trubi[:] = [robot_pos] + tubes + [stands[len(stands) // 2]]
    calc_path()

    # --- 6. Показать маршрут ---
    pole_draw = pole.copy()
    draw_robot()
    size  = [20, 15, 10, 5]
    color = [(0,0,255), (0,255,255), (255,0,0), (0,255,0)]
    for j, leg in enumerate(fin_path):
        for y, x in leg:
            cv2.circle(pole_draw, (x*CELL+PAD+40, y*CELL+PAD+40), size[j], color[j], -1)
    draw_pole()
    show_pole()
    cv2.waitKey()

    # --- 7. Проехать маршрут ---
    for j, leg in enumerate(fin_path):
        if not leg or leg == [[-1, -1]]:
            print(f"WARN: участок {j} не найден, пропускаю")
            continue
        make_drive(leg)
        drive(1)
        draw_robot()
        draw_pole()
        show_pole()
        cv2.waitKey()

    print(f"sputnik_go: готово, финиш {robot_pos}, dir={robot_dir}")
    cv2.waitKey(0)


def draw_corners():
      # если две красные клетки сходятся углом, рисуем между ними красную клетку - угол поля
      # bort_map: 0 - не знаем, 1 - поле, 2 - бортик (slam_map только для кодов клеток)
      S = 40
      for y in range(17):
            for x in range(17):
                  if bort_map[y][x] != 0:
                        continue
                  for dy in [-1, 1]:
                        for dx in [-1, 1]:
                              if 0 <= y + dy < 17 and 0 <= x + dx < 17:
                                    # бортик сверху/снизу и слева/справа, а по диагонали поле -> это угол
                                    if bort_map[y + dy][x] == 2 and bort_map[y][x + dx] == 2 and bort_map[y + dy][x + dx] == 1:
                                          bort_map[y][x] = 2
                                          images_array[y * S:(y + 1) * S, 810 + x * S:810 + (x + 1) * S] = red_color


def slam_step1():
      global robot_dir

      robot_dir = 1
      draw_robot()
      show_pole()

      images_array[0:690, 810:1500] = (0, 0, 0)

      S = 40
      cx, cy = 8, 8

      # где на карте клетки буквы Т (dx, dy) для каждого направления робота
      # порядок: слева спереди, спереди, справа спереди, через одну спереди
      offsets = {
            1: [(-1, -1), (0, -1), (1, -1), (0, -2)],
            2: [(1, -1), (1, 0), (1, 1), (2, 0)],
            3: [(1, 1), (0, 1), (-1, 1), (0, 2)],
            4: [(-1, 1), (-1, 0), (-1, -1), (-2, 0)]
      }
      # где на карте клетки слева и справа от робота (dx, dy)
      sides = {
            1: [(-1, 0), (1, 0)],
            2: [(0, -1), (0, 1)],
            3: [(1, 0), (-1, 0)],
            4: [(0, 1), (0, -1)]
      }
      cv2.waitKey(0)
      for _ in range(4):
            imgs = scan_ahead_4()
            # рисуем отсканированные клетки на карте
            bort_map[cy][cx] = 1  # клетка робота - это поле
            for i in range(4):
                  if imgs[i] is not None:
                        dx, dy = offsets[robot_dir][i]
                        tx = 810 + (cx + dx) * S
                        ty = (cy + dy) * S
                        images_array[ty:ty + S, tx:tx + S] = cv2.resize(imgs[i], (S, S))
                        bort_map[cy + dy][cx + dx] = 1  # 1 - поле

            # бортики рисуем на карте красными клетками
            red = detect_red()
            krasnye = []
            # клетки Т за бортиком (если бортик прямо спереди, Т не красим)
            # дальнюю клетку (3) не красим - там робот бортик не видит
            if red["front"] == False:
                  for i in range(3):
                        if imgs[i] is None:
                              krasnye.append(offsets[robot_dir][i])
            # клетки слева и справа от робота
            if red["left"] == True:
                  krasnye.append(sides[robot_dir][0])
            if red["right"] == True:
                  krasnye.append(sides[robot_dir][1])
            for dx, dy in krasnye:
                  tx = 810 + (cx + dx) * S
                  ty = (cy + dy) * S
                  images_array[ty:ty + S, tx:tx + S] = red_color
                  bort_map[cy + dy][cx + dx] = 2  # 2 - бортик
            draw_corners()

            # сначала показываем, потом поворачиваем, чтобы панель совпадала с роботом на поле
            show_pole()
            draw_scan_panel(imgs)
            cv2.waitKey(0)
            rotate(1)

      while robot_dir != 1:
            rotate(1)
            show_pole() 
            cv2.waitKey(100)

      cv2.waitKey(0)



robot_pos = [0, 7]   # стартовая клетка (y, x)
# draw_robot()
# draw_pole()
# show_pole()
# cv2.waitKey(1)
#
# key_drive(1)
# cv2.waitKey(0)

slam_step1()



# cords = "1"
# start = pole[2][3]
# print(start)
# print(1 in dict_p.get(str(start))[0])
# robot_pos = [4,4] # y x
# draw_robot()
# draw_pole()
# cv2.imshow("pole", pole_dra)

# sputnik_go()
# robot_pos = [4, 4]
# draw_robot()
# draw_pole()
# show_pole()
# # key_drive(1)
# cv2.waitKey()
# robot_pos = detect_robot()
# print(robot_pos)
# sputnik()
# calc_path()
# draw_robot()
# draw_pole()
# show_pole()
#
# cv2.waitKey()
# for i in range(4):
#       make_drive(fin_path[i])
#       print(fin_path[i])
#       print(move)
#       drive(1)
#       print(robot_pos)
#       cv2.waitKey()

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