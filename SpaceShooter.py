import pygame, sys, random, time
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Space Shooter")
screen = pygame.display.set_mode((800,600))
bg = pygame.image.load("SpaceBg.jfif")

score = 0

missileCount = 4

myfont = pygame.font.SysFont("comicsansms", 20)

class GameObject:
    def __init__(self, x, y, filename):
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename).convert_alpha()
    def draw(self):
        screen.blit(self.image, (self.x, self.y) )

class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self, 320, 500, "shuttle2.png")
        self.miss_list = []
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.x> 0:
            self.x -= 7
        if pressed_keys[K_RIGHT] and self.x < 800 - 52:
            self.x += 7
    def fire(self):
        self.miss_list.append( Missile(self.x + 26) )
    def remove(self, a):
        self.miss_list.pop(a)

class Missile(GameObject):
    def __init__(self, x):
        GameObject.__init__(self, x, 500, "cloud.png")
    def move(self):
        self.y -= 5
    def draw_missile(x, y):
        pygame.draw.line(screen, (0,255,0), (x,y), (x,y+8), 1)
    def offScreen(self):
        if self.y < 0:
            return True
          

class BadGuy(GameObject):
    def __init__(self):
        GameObject.__init__(self, random.randint(0, 600), -45, "badguy.png")
        self.dx = random.randint(-5,5)
        self.dy = random.randint(1,5)
    def move(self):
        self.x += self.dx
        self.y += self.dy
    def bounce(self):
        if self.x <0 or self.x > 700:
            self.dx *= -1
    def off_screen(self):
        if self.y > 700:
            return True
        else:
            return False
    def collision_with_missile(self, missile):
        if pygame.Rect(self.x, self.y, 100, 100).collidepoint((missile.x, missile.y)) == True:
            return True

badguy = BadGuy()

enemy_list = []

player = Player()

prev_time = 0

while True:
    clock.tick(60)
    screen.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        if event.type == KEYDOWN and event.key == K_SPACE and len(player.miss_list) < 4:
            player.fire()

    m = 0
    while m < len(player.miss_list):
        player.miss_list[m].move()
        Missile.draw_missile( player.miss_list[m].x, player.miss_list[m].y)
        if player.miss_list[m].offScreen() == True:
            player.remove(m)
            m -= 1
        m += 1

    i = 0
    while i < len(enemy_list):
        j = 0
        while j < len(player.miss_list):
            if enemy_list[i].collision_with_missile(player.miss_list[j]):
                del enemy_list[i]
                del player.miss_list[j]
                score += 100
                i -= 1
                break
            j += 1
        i += 1

    if time.time() - prev_time > 2:
        enemy_list.append(BadGuy())
        prev_time = time.time()

    x = 0
    while x < len(enemy_list):
        enemy_list[x].move()
        enemy_list[x].bounce()
        enemy_list[x].draw()
        if enemy_list[x].off_screen():
            del enemy_list[x]
            x -= 1
            print("Defeated!")
            sys.exit()
        x += 1

    player.move()
    player.draw()
    screen.blit(myfont.render ("Missile Count: " + str(missileCount - len(player.miss_list)), True, (255,255,255)), (650, 5))
    screen.blit(myfont.render ("Score: " + str(score), True, (255,255,255)), (5,5))
    pygame.display.update()

