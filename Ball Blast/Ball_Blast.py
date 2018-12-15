import pygame
import random
import sys
import threading
import time
import math
import csv

pygame.init()

# Screen Dimesions
screenW = 500
screenH = 900

# Setting up the display
win = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Ball Blast')

# Text Variables
hfont = pygame.font.SysFont('comicsans', 30)
gofont = pygame.font.SysFont('comicsans', 50)
levelupfont = pygame.font.SysFont('comicsans', 50)
infofont = pygame.font.SysFont('comicsans', 30)
shopbtnfont = pygame.font.SysFont('comicsans', 25)
btnfont = pygame.font.SysFont('comicsans', 50)

# Colours
white = (255, 255, 255)
cannon = (82, 55, 150)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
shopColour = (255, 0, 102)
coincolor = (230, 230, 0)
goshopcolor = (0, 131, 219)
yellow = (206, 202, 2)
restartbtncolor = (68, 252, 114)

# Upgradables
damageLevel = 1
fireRate = 20
cashmult = 1
offlineearn = 0

# Level Variables
level = 1
killed = 0
score = 0
cash = 1000

# Shop variables
powerbtncost = 100
bulletincscost = 250
coininccost = 200
offlinecost = 200

powerinc = 1.1
bulletinc = 1.2
coininc = 1.1
offlineinc = 1.2

powerOwned = 0
bulletincOwned = 0
coinincOwned = 0
offlineOwned = 0

powercostinc = 1.2
bulletconstinc = 1.3
coincostinc = 1.2
offlinecoininc = 1.4

clock = pygame.time.Clock()


class Tower(object):
    def __init__(self):
        self.y = screenH - 100
        self.w = 50
        self.h = 70
        self.x = (screenW - self.w) // 2
        self.damage = damageLevel
        self.firerate = fireRate
        self.vel = 10

    def draw(self, win):
        # Frame, Color, (positionX, positionY, widthX, widthY), Filled
        pygame.draw.rect(win, (82, 55, 150), (self.x, self.y, self.w, self.h), 0)


class Projectile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 15
        self.radius = 5
        self.hitbox = (self.x, self.y)
        self.power = damageLevel

    def draw(self, win):
        # circle(Surface, color, pos, radius, width=0)
        pygame.draw.circle(win, black, (self.x, self.y), self.radius, 0)


class Ball(object):
    def __init__(self, x, y, h, r):
        self.x = x
        self.y = y
        self.vel = 5
        self.velUp = 10
        self.health = h
        self.starthealth = h
        self.radius = r
        self.floor = screenH - 30
        self.ceiling = 30
        self.wallL = 25
        self.wallR = screenW - 25
        # self.hitBox = (self.x + 17, self.y + 2, 31, 57)
        self.hitBox = (self.x, self.y)

    def draw(self, win):
        # text = scorefont.render('Score: ' + str(score), 1, white)
        pygame.draw.circle(win, green, (self.x, self.y), self.radius, 0)
        for ball in balls:
            htext = hfont.render(str(ball.health), 1, white)
            win.blit(htext, (ball.x, ball.y))
        self.move()

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.wallR - self.radius:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.wallL + self.radius:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

        if self.velUp > 0:
            if self.y + self.vel < self.floor - self.radius:
                self.y += self.velUp
            else:
                self.velUp = self.velUp * -1
        else:
            if self.y - self.velUp > self.ceiling + self.radius:
                self.y += self.velUp
            else:
                self.velUp = self.velUp * -1


class TestThreading(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

        global killed

        spawn = 0

        spawning = True
        while spawning:

            if spawn != level:
                types = random.randint(0, 4)
                health = random.randint(10, maxhealth[level // 10])
                radius = radii[types]
                y = random.randint(0 + radius, screenH // 2)
                balls.append(Ball(0 + radius, y, health, radius))
                spawn += 1

            else:
                spawning = False

            interval = random.randint(3, 5)
            time.sleep(interval)


def save():

    global level
    global cash
    global cash
    global powerbtncost
    global bulletincscost
    global coininccost
    global offlinecost
    global powerinc
    global bulletinc
    global coininc
    global offlineinc
    global powerOwned
    global bulletincOwned
    global coinincOwned
    global offlineOwned
    global damageLevel
    global fireRate
    global cashmult
    global offlineearn

    f = open('level.txt', 'w')
    f.write(str(level) + "," + str(cash) + ',' + str(math.ceil(time.time())))
    f.close()

    f = open('upgradesLevel.txt', 'w')
    f.write(str(damageLevel) + ',' + str(fireRate) + ',' + str(cashmult) + ',' + str(offlineearn))
    f.close()

    f = open('upgradesCosts.txt', 'w')
    f.write(str(powerbtncost) + ',' + str(bulletincscost) + ',' + str(coininccost) + ',' + str(offlinecost))
    f.close()

    f = open('upgradesOwned.txt', 'w')
    f.write(str(powerOwned) + ',' + str(bulletincOwned) + ',' + str(coinincOwned) + ',' + str(offlineOwned))
    f.close()


def drawshop():

    global cash
    global powerbtncost
    global bulletincscost
    global coininccost
    global offlinecost
    global powerinc
    global bulletinc
    global coininc
    global offlineinc
    global powerOwned
    global bulletincOwned
    global coinincOwned
    global offlineOwned
    global damageLevel
    global fireRate
    global cashmult
    global offlineearn

    win.fill(shopColour)
    cashtext = infofont.render('Coins: ' + str(cash), 1, black)

    # Button Drawing
    powerbtn = pygame.draw.rect(win, red, (0, 100, screenW, 100))
    bulletsbtn = pygame.draw.rect(win, blue, (0, 200, screenW, 100))
    cashbtn = pygame.draw.rect(win, yellow, (0, 300, screenW, 100))
    offlinebtn = pygame.draw.rect(win, green, (0, 400, screenW, 100))
    exitbtn = pygame.draw.rect(win, restartbtncolor, (0, 500, screenW, 100))

    # Label Drawing
    powertextlbl = shopbtnfont.render('Power Increase', 1, white)
    powertextcost = shopbtnfont.render('Cost: ' + str(powerbtncost), 1, white)
    powerowned = shopbtnfont.render('Owned: ' + str(powerOwned), 1, white)
    bulletlbl = shopbtnfont.render('Bullets Increase', 1, white)
    bulletcosttext = shopbtnfont.render('Cost: ' + str(bulletincscost), 1, white)
    bulletsowned = shopbtnfont.render('Owned: ' + str(bulletincOwned), 1, white)
    cashlbl = shopbtnfont.render('Cash Increase', 1, white)
    cashcosttext = shopbtnfont.render('Cost: ' + str(coininccost), 1, white)
    cashincowned = shopbtnfont.render('Owned: ' + str(coinincOwned), 1, white)
    offlinelbl = shopbtnfont.render('Offline Earnings', 1, white)
    offlinecosttext = shopbtnfont.render('Cost: ' + str(offlinecost), 1, white)
    offlineowned = shopbtnfont.render('Owned: ' + str(offlineOwned), 1, white)
    restartbtntext = shopbtnfont.render('Restart ', 1, white)

    # Adding it to the screen
    win.blit(cashtext, (screenW // 2 - (cashtext.get_width() / 2), 20))
    win.blit(powertextlbl, (5, 105))
    win.blit(powertextcost, (5, 140))
    win.blit(powerowned, (5, 175))
    win.blit(bulletlbl, (5, 205))
    win.blit(bulletcosttext, (5, 240))
    win.blit(bulletsowned, (5, 275))
    win.blit(cashlbl, (5, 305))
    win.blit(cashcosttext, (5, 340))
    win.blit(cashincowned, (5, 375))
    win.blit(offlinelbl, (5, 405))
    win.blit(offlinecosttext, (5, 440))
    win.blit(offlineowned, (5, 475))
    win.blit(restartbtntext, (screenW / 2 - (restartbtntext.get_width() / 2), 545))
    pygame.display.update()

    shopping = True
    while shopping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and powerbtn.collidepoint(pygame.mouse.get_pos()):
                if cash >= powerbtncost:
                    cash -= powerbtncost
                    damageLevel += 2
                    powerOwned += 1
                    powerbtncost = math.ceil(powerbtncost * powercostinc)
                    drawshop()
            if event.type == pygame.MOUSEBUTTONDOWN and bulletsbtn.collidepoint(pygame.mouse.get_pos()):
                if cash >= bulletincscost:
                    cash -= bulletincscost
                    fireRate = math.ceil(fireRate * bulletinc)
                    bulletincscost = math.ceil(bulletconstinc * bulletincscost)
                    bulletincOwned += 1
                    drawshop()
            if event.type == pygame.MOUSEBUTTONDOWN and cashbtn.collidepoint(pygame.mouse.get_pos()):
                if cash >= coininccost:
                    cash -= coininccost
                    coininccost = math.ceil(coininccost * coincostinc)
                    coinincOwned += 1
                    cashmult = cashmult * coininc
                    drawshop()
            if event.type == pygame.MOUSEBUTTONDOWN and offlinebtn.collidepoint(pygame.mouse.get_pos()):
                if cash >= offlinecost:
                    if offlineOwned == 0:
                        cash -= offlinecost
                        offlinecost = math.ceil(offlinecost * offlinecoininc)
                        offlineOwned += 1
                        offlineearn = 5
                    else:
                        cash -= offlinecost
                        offlinecost = math.ceil(offlinecost * offlinecoininc)
                        offlineOwned += 1
                        offlineearn = math.ceil(offlineearn * offlineinc)
                    drawshop()
            if event.type == pygame.MOUSEBUTTONDOWN and exitbtn.collidepoint(pygame.mouse.get_pos()):
                main()


def nextLevelDraw():
    win.fill(white)
    # Frame, Color, (positionX, positionY, widthX, widthY), Filled
    restartbtn = pygame.draw.rect(win, green, (0, 300, screenW, 100))
    shopbtn = pygame.draw.rect(win, blue, (0, 400, screenW, 100))
    quitbtn = pygame.draw.rect(win, red, (0, 500, screenW, 100))
    lvltext = levelupfont.render('Level Up', 1, black)
    restarttext = btnfont.render('Restart', 1, white)
    shoptext = btnfont.render('Shop', 1, white)
    quittext = btnfont.render('Quit', 1, white)
    win.blit(lvltext, (screenW // 2 - (lvltext.get_width() / 2), 20))
    win.blit(restarttext, (screenW // 2 - (restarttext.get_width() / 2), 335))
    win.blit(shoptext, (screenW // 2 - (shoptext.get_width() / 2), 435))
    win.blit(quittext, (screenW // 2 - (quittext.get_width() / 2), 535))
    pygame.display.update()

    next = True
    while next:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and restartbtn.collidepoint(pygame.mouse.get_pos()):
                main()
            if event.type == pygame.MOUSEBUTTONDOWN and shopbtn.collidepoint(pygame.mouse.get_pos()):
                drawshop()
            if event.type == pygame.MOUSEBUTTONDOWN and quitbtn.collidepoint(pygame.mouse.get_pos()):
                save()
                pygame.quit()
                sys.exit()


def redraw():
    win.fill(white)
    cannon.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for ball in balls:
        ball.draw(win)
    lvltext = infofont.render('Level: ' + str(level), 1, black)
    win.blit(lvltext, (20, 20))
    scoretext = infofont.render('Score: ' + str(score), 1, black)
    win.blit(scoretext, (screenW // 2 - (scoretext.get_width() / 2), 20))
    cashtext = infofont.render('Coins: ' + str(cash), 1, black)
    win.blit(cashtext, (screenW - (cashtext.get_width()) - 10, 20))
    pygame.display.update()


def gameOver():
    win.fill(black)
    gotext = gofont.render('Game Over', 1, white)
    win.blit(gotext, (screenW // 2 - (gotext.get_width() / 2), 20))
    # Frame, Color, (positionX, positionY, widthX, widthY), Filled
    restartbtn = pygame.draw.rect(win, green, (screenW // 2 - 50, screenH // 2 - 150, 100, 50))
    shopbtn = pygame.draw.rect(win, goshopcolor, (screenW // 2 - 50, screenH // 2 - 50, 100, 50))
    quitbtn = pygame.draw.rect(win, red, (screenW // 2 - 50, screenH // 2 + 50, 100, 50))
    pygame.display.update()

    go = True

    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and restartbtn.collidepoint(pygame.mouse.get_pos()):
                main()
            if event.type == pygame.MOUSEBUTTONDOWN and shopbtn.collidepoint(pygame.mouse.get_pos()):
                drawshop()
            if event.type == pygame.MOUSEBUTTONDOWN and quitbtn.collidepoint(pygame.mouse.get_pos()):
                save()
                pygame.quit()
                sys.exit()


cannon = Tower()

bullets = []
balls = []

maxhealth = [25, 100, 500, 1000, 5000]
radii = [25, 40, 55, 70, 85]


def main():

    global killed
    global score
    global level
    global cash

    killed = 0
    tr = TestThreading()

    run = True
    while run:

        clock.tick(30)

        if killed == level:
            h = 0
            while len(balls) != 0:
                balls.pop()
                h += 1
            i = 0
            while len(bullets) != 0:
                bullets.pop()
                i += 1
            level += 1
            nextLevelDraw()
            run = False

        for bullet in bullets:
            for ball in balls:
                if bullet.y - bullet.radius < ball.y + ball.radius and bullet.y + bullet.radius > ball.y:
                    if bullet.x + bullet.radius > ball.x and bullet.x - bullet.radius < ball.x + ball.radius:
                        if ball.health > bullet.power:
                            ball.health -= bullet.power
                            score += bullet.power
                        else:
                            cash += math.ceil((ball.starthealth // 2) * cashmult)
                            balls.pop(balls.index(ball))
                            killed += 1
                        bullets.pop(bullets.index(bullet))

        for ball in balls:
            if ball.y - ball.radius < cannon.y + cannon.h and ball.y + ball.radius > cannon.y:
                if ball.x + ball.radius > cannon.x and ball.x - ball.radius < cannon.x + cannon.w:
                    h = 0
                    while len(balls) != 0:
                        balls.pop()
                        h += 1
                    i = 0
                    while len(bullets) != 0:
                        bullets.pop()
                        i += 1
                    del tr
                    gameOver()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()

        for bullet in bullets:
            if 0 < bullet.y < screenH:
                bullet.y -= bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and cannon.x > cannon.vel:
            cannon.x -= cannon.vel
        if keys[pygame.K_RIGHT] and cannon.x < screenW - cannon.w - cannon.vel:
            cannon.x += cannon.vel
        if keys[pygame.K_SPACE]:
            if len(bullets) < fireRate:
                bullets.append(Projectile(cannon.x + (cannon.w // 2), cannon.y - 5))

        redraw()


def openfile():
    global cash
    global powerbtncost
    global bulletincscost
    global coininccost
    global offlinecost
    global powerinc
    global bulletinc
    global coininc
    global offlineinc
    global powerOwned
    global bulletincOwned
    global coinincOwned
    global offlineOwned
    global damageLevel
    global fireRate
    global cashmult
    global offlineearn
    global level

    with open('level.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            level = int(row[0])
            cash = int(row[1])
            timediff = math.ceil(time.time()) - int(row[2])
            timeaway = math.floor(timediff / 60)
            cashearned = math.ceil(timeaway * offlineearn)
            cash += cashearned

    with open('upgradesCosts.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            powerbtncost = int(row[0])
            bulletincscost = int(row[1])
            coininccost = int(row[2])
            offlinecost = int(row[3])

    with open('upgradesLevel.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            damageLevel = int(row[0])
            fireRate = int(row[1])
            cashmult = float(row[2])
            offlineearn = int(row[3])

    with open('upgradesOwned.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            powerOwned = int(row[0])
            bulletincOwned = int(row[1])
            coinincOwned = int(row[2])
            offlineOwned = int(row[3])

    if cashearned == 0:
        opening()
    else:
        offlineearning(timeaway, cashearned)


def offlineearning(t, c):

    win.fill(white)
    minutes = infofont.render('You have been away for: ' + str(t) + ' minutes', 1, black)
    cashearn = infofont.render('You earned: ' + str(c) + ' coins', 1, black)
    cashnow = infofont.render('Coins: ' + str(cash), 1, black)
    okbtn = pygame.draw.rect(win, black, (0, 600, screenW, 100))
    oktext = btnfont.render('OK', 1, white)
    win.blit(minutes, (screenW // 2 - (minutes.get_width() / 2), 400))
    win.blit(cashearn, (screenW // 2 - (cashearn.get_width() / 2), 450))
    win.blit(cashnow, (screenW // 2 - (cashnow.get_width() / 2), 500))
    win.blit(oktext, (screenW // 2 - (oktext.get_width() / 2), 635))
    pygame.display.update()

    open = True

    while open:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and okbtn.collidepoint(pygame.mouse.get_pos()):
                opening()


def opening():
    win.fill(white)
    maintext = infofont.render('Start Menu', 1, black)
    playbtn = pygame.draw.rect(win, green, (0, 300, screenW, 100))
    shopbtn = pygame.draw.rect(win, blue, (0, 400, screenW, 100))
    quitbtn = pygame.draw.rect(win, red, (0, 500, screenW, 100))
    restarttext = btnfont.render('Restart', 1, white)
    shoptext = btnfont.render('Shop', 1, white)
    quittext = btnfont.render('Quit', 1, white)
    win.blit(restarttext, (screenW // 2 - (restarttext.get_width() / 2), 335))
    win.blit(shoptext, (screenW // 2 - (shoptext.get_width() / 2), 435))
    win.blit(quittext, (screenW // 2 - (quittext.get_width() / 2), 535))
    win.blit(maintext, (screenW // 2 - (maintext.get_width() / 2), 30))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and playbtn.collidepoint(pygame.mouse.get_pos()):
                main()
            if event.type == pygame.MOUSEBUTTONDOWN and shopbtn.collidepoint(pygame.mouse.get_pos()):
                drawshop()
            if event.type == pygame.MOUSEBUTTONDOWN and quitbtn.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()


openfile()
