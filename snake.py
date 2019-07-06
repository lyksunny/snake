import random, sys, pygame
from pygame.locals import *

#定义颜色变量
redcolor = pygame.Color(255, 0, 0)
whitecolor = pygame.Color(255, 255, 255)
blackcolor = pygame.Color(0, 0, 0)
azureblue = pygame.Color(0,255,255)

pygame.init() #初始化pygame
fpsClock = pygame.time.Clock() #定义变量控制游戏速度
playSurface = pygame.display.set_mode((640,480)) #创建pygame的显示层
pygame.display.set_caption("辣鸡贪吃蛇")

#初始化
snakePosition = [40, 100] #初始化贪吃蛇位置
snakebody = [[40,100], [20,100], [0,100]] #初始化贪吃蛇长度
targetPosition = [300, 300]  #初始化目标方块的位置
targetFlag = 1  #初始化目标方块的标记
direction = 'right' #初始化方向
changeDirection = direction #定义一个方向变量
score = 0
p = 1
pause = False
die = False

#处理pygame当中的事件，游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if die == False:
                if pause == False:
                    if event.key == K_RIGHT:
                        changeDirection = 'right'
                    if event.key == K_LEFT:
                        changeDirection = 'left'
                    if event.key == K_UP:
                        changeDirection = 'up'
                    if event.key == K_DOWN:
                        changeDirection = 'down'
                if event.key == K_SPACE:
                    p += 1
            if die == True:
                if event.key == GL_MULTISAMPLEBUFFERS:
                    snakePosition = [40, 100]
                    snakebody = [[40, 100], [20, 100], [0, 100]]
                    targetPosition = [300, 300]
                    targetFlag = 1
                    direction = 'right'
                    changeDirection = direction
                    score = 0
                    p = 1
                    pause = False
                    die = False
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    #确定方向
    if changeDirection == 'left' and direction != 'right':
        direction = changeDirection
    if changeDirection == 'right' and direction != 'left':
        direction = changeDirection
    if changeDirection == 'up' and direction != 'down':
        direction = changeDirection
    if changeDirection == 'down' and direction != 'up':
        direction = changeDirection

    if pause == False and die == False:
        #根据方向移动蛇头坐标
        if direction == 'right':
            snakePosition[0] += 20
        if direction == 'left':
            snakePosition[0] -= 20
        if direction == 'up':
            snakePosition[1] -= 20
        if direction == 'down':
            snakePosition[1] += 20

        #增加蛇的长度
        snakebody.insert(0,list(snakePosition))

        #吃掉目标方块，target==0
        if snakePosition == targetPosition:
            targetFlag = 0
            score += 10
        else:
            snakebody.pop()

        while targetFlag == 0:
            x = random.randrange(1,32)
            y = random.randrange(6,24)
            targetPosition = [x*20, y*20]
            if targetPosition in snakebody: targetFlag = 0
            else: targetFlag = 1

    if p % 2 == 0: pause = True
    else: pause = False

    #绘制pygame显示层
    playSurface.fill(blackcolor)
    for position in snakebody:
        pygame.draw.rect(playSurface, whitecolor, Rect(position[0], position[1], 20, 20))
    pygame.draw.rect(playSurface, redcolor, Rect(targetPosition[0], targetPosition[1], 20, 20))

    surf = pygame.Surface((640, 100))
    surf.fill(azureblue)
    playSurface.blit(surf, (0, 0))

    #文字
    if pause == False:
        text = '得分：' + str(score)
    else:
        text = '  暂停 '
    font = pygame.font.SysFont('SimHei', 50)
    textScreen = font.render(text, True, redcolor)
    playSurface.blit(textScreen, (240, 30))

    if die == True:
        retext = '按回车键重新开始'
        refont = pygame.font.SysFont('SimHei', 30)
        rescreen = refont.render(retext, True, redcolor)
        playSurface.blit(rescreen, (200, 400))
        if score < 1500:
            overfont = pygame.font.SysFont('SimHei', 100)
            overtext = overfont.render("你个辣鸡", False, redcolor)
            playSurface.blit(overtext, (120, 200))

    #更新显示屏幕表面
    pygame.display.update()

    #判断死亡
    if snakePosition[0] > 620 or snakePosition[0] < 0 or snakePosition[1] >460 or snakePosition[1] < 100:
        die = True
    for position in snakebody[1::]:
        if position == snakePosition:
            die = True

    fpsClock.tick(len(snakebody) / 10 + 5)