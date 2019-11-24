import pygame
import random

pygame.init()
clock = pygame.time.Clock()
screenWidth = 800
screenHeight = 450
window = pygame.display.set_mode(size=(screenWidth, screenHeight))
pygame.display.set_caption("My Game")
bg = pygame.image.load('pics/bg.jpg')
char = pygame.image.load('pics/standing.png')
walkRight = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'), pygame.image.load('pics/R3.png'),
             pygame.image.load('pics/R4.png'), pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png'),
             pygame.image.load('pics/R7.png'), pygame.image.load('pics/R8.png'), pygame.image.load('pics/R9.png')]
walkLeft = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'), pygame.image.load('pics/L3.png'),
            pygame.image.load('pics/L4.png'), pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png'),
            pygame.image.load('pics/L7.png'), pygame.image.load('pics/L8.png'), pygame.image.load('pics/L9.png')]

bulletSound = pygame.mixer.Sound('sounds/bullet.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')
bulletSound.set_volume(0.2)
hitSound.set_volume(0.2)
music = pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

score = 0


class enemy(object):
    walkRight = [pygame.image.load('pics/R1E.png'), pygame.image.load('pics/R2E.png'), pygame.image.load('pics/R3E.png'),
                 pygame.image.load('pics/R4E.png'), pygame.image.load('pics/R5E.png'), pygame.image.load('pics/R6E.png'),
                 pygame.image.load('pics/R7E.png'), pygame.image.load('pics/R8E.png'), pygame.image.load('pics/R9E.png'),
                 pygame.image.load('pics/R10E.png'), pygame.image.load('pics/R11E.png')]
    walkLeft = [pygame.image.load('pics/L1E.png'), pygame.image.load('pics/L2E.png'), pygame.image.load('pics/L3E.png'),
                pygame.image.load('pics/L4E.png'), pygame.image.load('pics/L5E.png'), pygame.image.load('pics/L6E.png'),
                pygame.image.load('pics/L7E.png'), pygame.image.load('pics/L8E.png'), pygame.image.load('pics/L9E.png'),
                pygame.image.load('pics/L10E.png'), pygame.image.load('pics/L11E.png')]

    def __init__(self, x, y, width, height, end, name, hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.hitCount = 0
        self.name = name
        self.maxHealth = hp
        self.health = hp
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20,  (50*self.health)/self.maxHealth, 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)

    def move(self):
        if self.vel < 0:
            if self.x + self.vel > self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel < self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self, dmg):
        if self.health > dmg:
            self.health -= dmg
        else:
            self.visible = False

        self.hitCount += 1
        print("hit ", self.name, self.hitCount)


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 16
        self.isJump = False
        self.left = True
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 29, 60)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 13, 29, 50)
        # pygame.draw.rect(window, (255,0,0), self.hitbox, 1)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 90
        self.y = 350
        self.walkCount = 0
        font3 = pygame.font.SysFont('comicsans', 100)
        text = font3.render('-5p', 1, (255, 0, 0))
        window.blit(text, (screenWidth/2 - text.get_width()/2, screenHeight/2))
        pygame.display.update()
        i = 0
        while i < 100:  # this type of delay allows the user to exit the game during the delay
            pygame.time.delay(10)  # this delay makes the game unresponsive for the time
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class marker(object):
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('comicsans', 24)
        self.text = text
        self.time = pygame.time.get_ticks()

    def draw(self, win):
        mark = self.font.render(self.text, 1, (255, 0, 0))
        win.blit(mark, (self.x, self.y))


class projectile(object):
    def __init__(self,x,y,radius,color,facing,dmg):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 12 * facing
        self.dmg = dmg

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    window.blit(bg, (0,0))
    text = font1.render('Score: ' + str(score), 1, (0, 0, 0))
    window.blit(text, (screenWidth - 200, 10))
    player1.draw(window)

    for enem in enemies:
        enem.draw(window)

    for bullet in bullets:
        bullet.draw(window)

    for hitMark in hitMarks:
        hitMark.draw(window)
        if hitMark.time < pygame.time.get_ticks() - 800:
            hitMarks.pop(hitMarks.index(hitMark))

    fps = font1.render('FPS: ' + str(round(clock.get_fps())), 1, (0, 0, 0))
    window.blit(fps, (10, 10))

    pygame.display.update()

# main
player1 = player(90, 350, 64, 64)
# goblin = enemy(550, 350, 64, 64, 150, "goblin")
enemies = []
bullets = []
hitMarks = []
shootLoop = 0
font1 = pygame.font.SysFont('comicsans', 30, bold=True)
font2 = pygame.font.SysFont('comicsans', 14)
i = 0
# mainloop
run = True
while run:
    # max 27 FPS
    clock.tick(27)

    randInt_0_1000 = random.randint(0, 1000)
    if randInt_0_1000 < 10:  # standard goblin 1%
        enemies.append(enemy(screenWidth - 100, 350, 64, 64, 150, "goblin" + str(i), 20))
        i += 1
    elif randInt_0_1000 < 12:  # BIG goblin 0.2%
        enemies.append(enemy(screenWidth - 100, 350, 64, 64, 150, "BIG-goblin" + str(i), 40))
        i += 1
    elif randInt_0_1000 < 14:  # tiny goblin 0.2%
        enemies.append(enemy(screenWidth - 100, 350, 64, 64, 150, "tiny-goblin" + str(i), 10))
        i += 1

    # shoot cooldown
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for ene in enemies:
        if player1.hitbox[1] < ene.hitbox[1] + ene.hitbox[3] and player1.hitbox[1] + player1.hitbox[3] > ene.hitbox[1]:
            if player1.hitbox[0] + player1.hitbox[2] > ene.hitbox[0] and player1.hitbox[0] < ene.hitbox[0] + ene.hitbox[2]:
                player1.hit()
                score -= 5

    for bullet in bullets:
        if screenWidth > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

        for ene in enemies:
            if bullet in bullets:  # bullet still exists
                if bullet.y - bullet.radius < ene.hitbox[1] + ene.hitbox[3] and bullet.y + bullet.radius > ene.hitbox[1]:
                    if bullet.x + bullet.radius > ene.hitbox[0] and bullet.x - bullet.radius < ene.hitbox[0] + ene.hitbox[2]:
                        ene.hit(bullet.dmg)
                        hitSound.play()
                        hitMarks.append(marker(bullet.x, bullet.y, str(bullet.dmg)))
                        score += 1
                        bullets.pop(bullets.index(bullet))
                        if not ene.visible:
                            enemies.pop(enemies.index(ene))



    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if player1.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(player1.x + player1.width//2), round(player1.y + player1.height//2), 6, (0,0,0), facing, random.randint(1,5)))
            bulletSound.play()

        shootLoop = 1

    if keys[pygame.K_LEFT] and player1.x > player1.velocity:
        player1.x -= player1.velocity
        player1.left = True
        player1.right = False
        player1.standing = False
    elif keys[pygame.K_RIGHT] and player1.x < screenWidth - player1.width - player1.velocity:
        player1.x += player1.velocity
        player1.right = True
        player1.left = False
        player1.standing = False
    else:
        player1.standing = True
        player1.walkCount = 0

    if not(player1.isJump):
        if keys[pygame.K_UP]:
            player1.isJump = True

    else:
        if player1.jumpCount >= -10:
            neg = 1
            if player1.jumpCount < 0:
                neg = -1
            player1.y -= (player1.jumpCount ** 2) * 0.5 * neg
            player1.jumpCount -= 1
        else:
            player1.isJump = False
            player1.jumpCount = 10

    redrawGameWindow()

pygame.quit()

