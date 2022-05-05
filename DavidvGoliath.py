import pygame, sys
from pygame.locals import *
from time import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()

BLACK = (0,0,0)
white = (255, 255, 255)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen_rect = screen.get_rect()
pygame.display.set_caption('David vs Goliath')

###    Loads the images    ####

samuel = pygame.image.load('DVG/PICS/samuel.png').convert_alpha() #loads the sheet
jesseicon = [pygame.image.load('DVG/PICS/jesse1.png'),pygame.image.load('DVG/PICS/jesse2.png'),pygame.image.load('DVG/PICS/jesse3.png')]
eliabicon = [pygame.image.load('DVG/PICS/eliab1.png'),pygame.image.load('DVG/PICS/eliab2.png'),pygame.image.load('DVG/PICS/eliab3.png')]
brothersicon = [pygame.image.load('DVG/PICS/bros1.png'),pygame.image.load('DVG/PICS/bros2.png'),pygame.image.load('DVG/PICS/bros3.png')]
davidwalkRight = [pygame.image.load('DVG/PICS/Walk1.png'), pygame.image.load('DVG/PICS/Walk2.png'), pygame.image.load('DVG/PICS/Walk3.png'), pygame.image.load('DVG/PICS/Walk4.png'), pygame.image.load('DVG/PICS/Walk5.png')]
davidwalkLeft = [pygame.image.load('DVG/PICS/Walk6.png'), pygame.image.load('DVG/PICS/Walk7.png'), pygame.image.load('DVG/PICS/Walk8.png'), pygame.image.load('DVG/PICS/Walk9.png'), pygame.image.load('DVG/PICS/Walk10.png')]
giant = [pygame.image.load('DVG/PICS/standing.png'),pygame.image.load('DVG/PICS/standing1.png'),pygame.image.load('DVG/PICS/standing2.png')]
saul = [pygame.image.load('DVG/PICS/saul1.png'),pygame.image.load('DVG/PICS/saul2.png'),pygame.image.load('DVG/PICS/saul3.png')]
farm = pygame.image.load('DVG/PICS/farm.png')
coronation = pygame.image.load('DVG/PICS/coronation.png')
desert = pygame.image.load('DVG/PICS/battlefield.png')
war = pygame.image.load('DVG/PICS/war.png')
warzone = pygame.image.load('DVG/PICS/warzone.png')
davididle = [pygame.image.load('DVG/PICS/Idle1.png'), pygame.image.load('DVG/PICS/Idle2.png'), pygame.image.load('DVG/PICS/Idle3.png'), pygame.image.load('DVG/PICS/Idle4.png'), pygame.image.load('DVG/PICS/Idle5.png')]
scene3 = pygame.image.load('DVG/PICS/anoint.png')
question_1 = pygame.image.load('DVG/test/1.png')
question_2 = pygame.image.load('DVG/test/2.png')
question_3 = pygame.image.load('DVG/test/3.png')
question_4 = pygame.image.load('DVG/test/4.png')
question_5 = pygame.image.load('DVG/test/5.png')
question_6 = pygame.image.load('DVG/test/6.png')
question_7 = pygame.image.load('DVG/test/7.png')
question_8 = pygame.image.load('DVG/test/8.png')
question_9 = pygame.image.load('DVG/test/9.png')
question_10 = pygame.image.load('DVG/test/10.png')
fail = pygame.image.load('DVG/test/fail.png')
passing = pygame.image.load('DVG/test/pass.png')
#######################

health = 100
clock = pygame.time.Clock()

hitsfx = pygame.mixer.Sound('DVG/sounds/grunt.wav') 
music = pygame.mixer.music.load('DVG/sounds/soundeffect.mp3')
pygame.mixer.music.set_volume(0.05)

class Sprite:
    image, box = None, None

    def __init__(self):
        self.image = pygame.Surface((0, 0))
        self.box = self.image.get_rect()

    def setImage(self, pygameImage):
        self.image = pygameImage
        self.box = self.image.get_rect()

    def motion(self):
        raise NotImplementedError

    def animate(self):
        self.display = self.image

    def update(self):
        self.motion()
        self.animate()
        scr.blit(self.display, self.box)
    
    def collidedWith(self, other):
        return self.box.colliderect(other.box)
    
    def getX(self):
        return self.box.centerx

    def getY(self):
        return self.box.centery
    
    def getCenter(self):
        return self.box.center

    def strip_from_sheet(self, sheet, start, size, columns, rows): #separates the spritesheet
        self.frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0]+size[0]*i, start[1]+size[1]*j)
                self.frames.append(sheet.subsurface(pygame.Rect(location, size)))
        return self.frames
    
class David:
    def __init__(self, x, y, width, length):
        self.x = x #x coordinate of the sprite
        self.y = y #y coordinate of the sprite
        self.width = width #width of the sprite
        self.length = length #length of the sprite
        self.vel = 5 #walking speed
        self.jump = False 
        self.left = False #facing left or not
        self.right = False #facing right or not
        self.walkcount = 0 #indexes the images for animation
        self.jumpcount = 10
        self.hitbox = (self.x, self.y, 50, 70)

    def draw(self, screen): #blits the character

        if self.walkcount + 1 >= 12:
            self.walkcount = 0

        if self.left:
            screen.blit(davidwalkLeft[self.walkcount//7], (self.x,self.y))
            self.walkcount += 1           
        elif self.right:
            screen.blit(davidwalkRight[self.walkcount//7], (self.x,self.y))
            self.walkcount += 1
        else:
            screen.blit(davididle[self.walkcount//7], (self.x,self.y))
            self.walkcount += 1
    
    def drawinfarm(self, screen): #for the idle david in scene 2
        if self.walkcount + 1 >= 12:
            self.walkcount = 0
        else:
            self.walkcount += 1
        screen.blit(davidwalkLeft[self.walkcount//7], (self.x,self.y))


class Jesse:
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.idle = True
        self.walkcount = 0
        self.hitbox = (self.x, self.y, 400, 100)

    def draw(self, screen):

        if self.walkcount + 1 >= 12:
            self.walkcount = 0
        else:
            self.walkcount += 1
        if self.idle:
            screen.blit(jesseicon[self.walkcount//9], (self.x,self.y))

class Eliab:
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.idle = True
        self.walkcount = 0
        self.hitbox = (self.x, self.y, 60, 100)

    def draw(self, screen):

        if self.walkcount + 1 >= 12:
            self.walkcount = 0
        else:
            self.walkcount += 1
        if self.idle:
            screen.blit(eliabicon[self.walkcount//9], (self.x,self.y))

class Bros:
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.idle = True
        self.walkcount = 0
        self.hitbox = (self.x, self.y, 60, 100)

    def draw(self, screen):

        if self.walkcount + 1 >= 12:
            self.walkcount = 0
        else:
            self.walkcount += 1
        if self.idle:
            screen.blit(brothersicon[self.walkcount//9], (self.x,self.y))

class Projectile: #will serve as the stones that david will sling
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius #size
        self.color = color
        self.facing = facing #where is the projectile released, right or left
        self.vel = 15 * facing #projectile speed
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)  

class Goliath:
    goliaths = [pygame.image.load('DVG/PICS/Gol1.png'), pygame.image.load('DVG/PICS/Gol2.png'), pygame.image.load('DVG/PICS/Gol3.png'), pygame.image.load('DVG/PICS/Gol4.png'), pygame.image.load('DVG/PICS/Gol5.png')]    
    def __init__(self, x, y, width, length, end):
        self.x = x #initial position
        self.y = y # initial position
        self.width = width # size of the image
        self.length = length #size of the image
        self.path = [self.y, end] #not let the sprite off the screen
        self.walkcount = 0 #indexing of the sprite
        self.vel = 4 #walking speed
        self.hitbox = (self.x+50, self.y+35, 50, 50) #a hitbox in the head
        self.health = 100
        self.alive = True

    def draw(self, screen):
        self.move()
        if self.alive:
            if self.walkcount + 1 >= 30:
                self.walkcount = 0
            
            screen.blit(self.goliaths[self.walkcount//9], (self.x, self.y))
            self.walkcount += 1
            self.hitbox = (self.x+50, self.y+35, 50, 50)
            pygame.draw.rect(screen,(255,0,0), (self.hitbox[0] - 20, self.hitbox[1]-30, 100, 10)) # Damage
            pygame.draw.rect(screen,(0,255,0), (self.hitbox[0] - 20, self.hitbox[1]-30, 100 - ((1) * (100 - self.health)), 10)) #hp bar
    def move(self): 
        if self.vel > 0:
            if self.y + self.vel < self.path[1]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.y - self.vel > self.path[0]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self):
        if self.health>0:
            hitsfx.play()
            self.health -= 10
        else:
            self.alive = False

class Saul:
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.idle = True
        self.walkcount = 0
        self.hitbox = (self.x, self.y, 60, 100)

    def draw(self, screen):

        if self.walkcount + 1 >= 12:
            self.walkcount = 0
        else:
            self.walkcount += 1
        if self.idle:
            screen.blit(saul[self.walkcount//9], (self.x,self.y))

class Giant:
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.idle = True
        self.walkcount = 0
        self.hitbox = (self.x, self.y, 150, 150)

    def draw(self, screen):

        if self.walkcount + 1 >= 12:
            self.walkcount = 0
        else:
            self.walkcount += 1
        if self.idle:
            screen.blit(giant[self.walkcount//9], (self.x,self.y))

class Samuel(Sprite):
    
    def __init__(self, sheet, screen_rect):
        self.screen_rect = screen_rect
        self.all_frames = Sprite.strip_from_sheet(self, sheet, (0,0), (75,125), 12, 4)
        self.setup_frames()
        self.direction = 'down'
        self.ani_delay = 100
        self.ani_timer = 0.0
        self.ani_index = 0
        self.image = self.frames[self.direction][self.ani_index]
         
        self.speed = 2
        self.rect = self.image.get_rect(center=(40,370))
        self.update()
         
    def setup_frames(self): #how many sprites per row
        # organize the frames on the spritesheet to possible directions
        self.frames = {
            'down':self.all_frames[:12],
            'left':self.all_frames[12:24],
            'right':self.all_frames[24:36],
            'up':self.all_frames[36:48]
        }
         
    def animate(self):
        # animates the current direction
        if pygame.time.get_ticks()-self.ani_timer > self.ani_delay:
            self.ani_timer = pygame.time.get_ticks()
            self.image = self.frames[self.direction][self.ani_index]
            if self.ani_index == len(self.frames[self.direction])-1:
                self.ani_index = 0
            else:
                self.ani_index += 1
           
    def update(self): # movement of the character
        global gametime
        self.animate()
        self.rect.clamp_ip(self.screen_rect)
        keys = pygame.key.get_pressed()
        if gametime ==2:

            if keys[pygame.K_DOWN]:
                self.direction = 'down'
                if self.rect.y != jesse.hitbox[1]:#to prevent running into the other sprites
                    self.rect.y += self.speed
                self.rect.y += self.speed
            if keys[pygame.K_RIGHT]:
                self.direction = 'right'
                if self.rect.x != jesse.hitbox[0]:
                    self.rect.x += self.speed
            if keys[pygame.K_LEFT]:
                self.direction = 'left'
                if self.rect.x != jesse.hitbox[0]:
                    self.rect.x -= self.speed
            if keys[pygame.K_UP]:
                self.direction = 'up'
                if self.rect.y != jesse.hitbox[1]:
                    self.rect.y -= self.speed

        else:
            if keys[pygame.K_DOWN]:
                self.direction = 'down'
                self.rect.y += self.speed
            if keys[pygame.K_RIGHT]:
                self.direction = 'right'
                self.rect.x += self.speed
            if keys[pygame.K_LEFT]:
                self.direction = 'left'
                self.rect.x -= self.speed
            if keys[pygame.K_UP]:
                self.direction = 'up'
                self.rect.y -= self.speed        
            
    def get_event(self, event):
        pass
           
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
def dvg(): # David vs Goliath scene
    screen.blit(desert, (0,0))
    if health > 0:
        text = hp.render("Health: " +  str(health), 1,(0, 0, 0))
    else:
        text = hp.render("One last hit", 1,(0, 0, 0))
    screen.blit(text, (650,20))
    david.draw(screen)
    goli.draw(screen)
    for stone in stones:
        stone.draw(screen)
    pygame.display.update()

def text_objects(text, font): 
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def message_to_screen(text): 
    largeText = pygame.font.Font('freesansbold.ttf', 18)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (400, 560)
    screen.blit(TextSurf, TextRect)

def test(): #test after gameplay
    global i
    global score
    global hp #formatting
    if i == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_1, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            score += 1
            i += 1
            pygame.time.wait(1000)
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            i += 1
    if i == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_2, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            score += 1
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            i += 1
    if i == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_3, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            score += 1
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            i += 1
    if i == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_4, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            score += 1
            i += 1
    if i == 4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_5, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            score += 1
            i += 1
    if i == 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_6, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            score += 1
            i += 1
    if i == 6:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_7, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            score += 1
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            i += 1
    if i == 7:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_8, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            score += 1
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            i += 1
    if i == 8:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_9, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            score += 1
            i += 1
    if i == 9:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        screen.blit(question_10, (0,0))
        pygame.display.update()
        if keys[pygame.K_a]:
            pygame.time.wait(1000)
            i += 1
        elif keys[pygame.K_b]:
            pygame.time.wait(1000)
            score += 1
            i += 1
    if i == 10:
        text = hp.render("Score: " +  str(score) + "/10", 1,(0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        keys = pygame.key.get_pressed()
        if score < 7:
            screen.blit(fail, (0,0))
            screen.blit(text, (500, 200))
        else:
            screen.blit(passing, (0,0))
            screen.blit(text, (200, 400))
        pygame.display.update()
        pygame.time.wait(2000)
        i += 1

    if i == 11:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.quit

#### characters present #####
hp = pygame.font.SysFont('comicsans', 30, True)
david = David(50, 350, 50, 70) #blits David for the dvg scene
davidfarm = David(400, 450, 50, 70) #blits David in the first farm scene
davidfarm2 = David(350, 200, 50, 70) #blits David in the second farm scene
goli = Goliath(600, 50, 150, 150, 450) #blits Goliath in the dvg scene
goliath = Giant(370, 50, 150, 150) 
jesse = Jesse(400, 130, 50, 80)
eliab = Eliab(450, 130, 40, 80)
eliabwar = Eliab(370, 450, 40, 80)
davidwar = David(50, 450, 50, 70)
saulwar = Saul(360, 500, 40, 90)
bro = Bros(500, 130, 40, 80)
bro1 = Bros(550, 130, 40, 80)
bro2 = Bros(350, 130, 40, 80)
bro3 = Bros(300, 130, 40, 80)
bro4 = Bros(250, 130, 40, 80)
bro5 = Bros(200, 130, 40, 80)
bro6 = Bros(600, 130, 40, 80)
stones = []
score = 0
#################################
shoot = 0
i = 0
gametime = 1 #trial variable to use for proceeding with the game
orange = (255, 216, 137)
#### game loop ####
def gameloop():
    global gametime
    global shoot
    global stones
    global hp
    global david
    global goli
    global health
    global i
    done = False
    game = True
    clock = pygame.time.Clock()
    sam = Samuel(samuel, screen_rect)
    while game:
        while gametime ==1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            sam.get_event(event)
            sam.update()
            screen.fill((0,0,0))
            sam.draw(screen)
            pygame.display.update()
            clock.tick(60)
            pygame.draw.rect(screen, white, [95, 535, 620, 50])
            scene_1 = (
                'Israel’s first king was named Saul. King Saul did not obey God.', 
                'So God said to Samuel, the prophet', 
                '“Find a man named Jesse, one of his sons will be the new king.”') 
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            #DIALOGUE
            if i >= 0 and i < 3:
                words = scene_1[i]
                message_to_screen(words)
                
                pygame.display.update()
                i += 1
                pygame.time.wait(5000) 
            if i == 3: 
                gametime += 1
                i = 0

        while gametime == 2:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            scene_2 = (
                'Samuel found Jesse in Bethlehem. He looked at seven of Jesse’s sons.',
                'They looked handsome and strong.', 
                '“Not them,” God said. “I do not care about looks. ',
                'I care about what’s in a person s heart.”', 
                'Jesse sent for his youngest son, David, who was tending sheep in the fields.',
                'Samuel saw him and God said, “He is the one!”',
                '(approach David)')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            sam.get_event(event)
            sam.update()
            screen.blit(farm, (0,0))
            jesse.draw(screen)
            eliab.draw(screen)
            bro.draw(screen)
            bro1.draw(screen)
            bro2.draw(screen)
            bro3.draw(screen)
            bro4.draw(screen)
            bro5.draw(screen)
            bro6.draw(screen)
            davidfarm.drawinfarm(screen)
            sam.draw(screen)
            pygame.display.update()
            clock.tick(60)
            #DIALOGUE
            if i >= 0 and i < 7:
                pygame.draw.rect(screen, orange, [60, 535, 685, 50])
                words = scene_2[i]
                message_to_screen(words)
                
                pygame.display.update()
                i += 1
                pygame.time.wait(5000)

            elif i == 7:
                if sam.rect.y - 125 < davidfarm.hitbox[1] + davidfarm.hitbox[3] and sam.rect.y + 125 > davidfarm.hitbox[1]: # collision with david to proceed
                        if sam.rect.x + 70 > davidfarm.hitbox[0] and sam.rect.x - 75 < davidfarm.hitbox[2] + davidfarm.hitbox[0]:
                            pygame.time.wait(2000)
                            gametime += 1
                            i = 0
        pygame.mixer.music.play(-1)

        while gametime == 3: #cutscene
            scene_3 = ('Samuel anointed David with oil.','So David was anointed the new king.')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            
            screen.blit(scene3, (0,0))
            pygame.display.update()
            clock.tick(60)
            #DIALOGUE
            pygame.draw.rect(screen, orange, [95, 535, 620, 50])
            words = scene_3[i]
            message_to_screen(words)
            
            pygame.display.update()
            pygame.time.wait(5000) 
            i += 1
            if i == 2:
                i = 0
                gametime += 1

        while gametime == 4: #cutscene
            scene_4 = (
                'Some time later, Israel fought the Philistines.', 
                'A giant Philistine soldier named Goliath challenged', 
                'the Israelites to send a champion to fight him.', 
                'But the Israelites were all too afraid.')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            screen.blit(war, (0,0))
            pygame.display.update()
            clock.tick(60)
            #DIALOGUE

            pygame.draw.rect(screen, orange, [95, 535, 620, 50])
            words = scene_4[i]
            message_to_screen(words)
            
            pygame.display.update()
            pygame.time.wait(5000)
            i += 1

            if i ==  4:
                pygame.time.wait(3000)
                i = 0
                gametime += 1

        while gametime == 5: #second farm scene
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            scene_5 = (
                'Jesse got worried for his sons fighting in the war.',
                'So, he asked David to go to the battlefield and bring food to his brothers.',
                '(go to the left side of the screen)')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            screen.blit(farm, (0,0))
            jesse.draw(screen)
            davidfarm2.draw(screen)
            pygame.display.update()
            clock.tick(60)
            #DIALOGUE
            if i >= 0 and i < 3:
                pygame.draw.rect(screen, orange, [62, 535, 680, 50])
                words = scene_5[i]
                message_to_screen(words)
                
                pygame.display.update()
                pygame.time.wait(5000)
                i += 1

            elif i == 3:

                if keys[pygame.K_LEFT] and davidfarm2.x > david.vel: 
                    davidfarm2.x -= davidfarm2.vel
                    davidfarm2.left = True
                    davidfarm2.right = False
                elif keys[pygame.K_RIGHT] and davidfarm2.x < 800 - davidfarm2.vel - davidfarm2.width:
                    davidfarm2.x += davidfarm2.vel
                    davidfarm2.left = False
                    davidfarm2.right = True
                    
                elif not(david.jump): 
                    if keys[pygame.K_UP] and davidfarm2.y > davidfarm2.vel+150: 
                        davidfarm2.y -= david.vel
                        davidfarm2.up = True
                        davidfarm2.down = False
                    elif keys[pygame.K_DOWN] and davidfarm2.y < 600 - davidfarm2.vel - davidfarm2.length:  
                        davidfarm2.y += david.vel
                        davidfarm2.up = False
                        davidfarm2.down = True
                if (davidfarm2.x > 0 and davidfarm2.x < 30) or (davidfarm2.x > 780 and davidfarm2.x < 800): #when david leaves the farm through the road
                    if (davidfarm2.y > 350 and davidfarm2.y < 400):
                        gametime +=1
                        i = 0
        while gametime == 6:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            scene_6 = (
                'David brought food to his brothers in the army.', 
                'He heard Goliath’s challenge and was not afraid.',
                '“How dare he defy God’s army?” asked David. “I will fight him!”',
                'Surprised, King Saul offered David his armor. “No,” said David.', 
                '“God helped me kill wild beasts.',
                'He will help me against Goliath, too!”,',
                'David took five stones and a sling.',
                '“Am I a dog?” Goliath roared.',
                '“You send me this stick of a boy to fight me!” ',
                '“You have a spear,” said David, “but I have the help of Israel’s God!”',
                '(go towards Goliath)')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            screen.blit(warzone, (0,0))
            eliabwar.draw(screen)
            goliath.draw(screen)
            davidwar.draw(screen)
            saulwar.draw(screen)
            pygame.display.update()
            clock.tick(60)

            #DIALOGUE
            if i >= 0 and i < 11:
                pygame.draw.rect(screen, orange, [62, 535, 680, 50])
                words = scene_6[i]
                message_to_screen(words)
                
                pygame.display.update()
                pygame.time.wait(5000)
                i += 1
            elif i == 11:
                if keys[pygame.K_LEFT] and davidwar.x > david.vel: 
                    davidwar.x -= davidwar.vel
                    davidwar.left = True
                    davidwar.right = False
                elif keys[pygame.K_RIGHT] and davidwar.x < 800 - davidwar.vel - davidwar.width:  
                    if davidwar.x >= 300 and davidwar.y >= 350: 
                        davidwar.x = davidwar.x
                    else:
                        davidwar.x += davidfarm2.vel
                        davidwar.left = False
                        davidwar.right = True
                    
                elif not(davidwar.jump): 
                    if keys[pygame.K_UP] and davidwar.y > davidwar.vel: 
                        davidwar.y -= davidwar.vel
                        davidwar.up = True
                        davidwar.down = False
                    elif keys[pygame.K_DOWN] and davidwar.y < 600 - davidwar.vel - davidwar.length:  
                        if davidwar.x >= 300 and davidwar.y >= 350: 
                            davidwar.x = davidwar.x
                        else:
                            davidwar.y += davidwar.vel
                            davidwar.up = False
                            davidwar.down = True
                if davidwar.y + 80 < goliath.hitbox[1] + goliath.hitbox[3] and davidwar.y > goliath.hitbox[1]: #when David approached Goliath, the battle will proceed
                        if davidwar.x + 70 > goliath.hitbox[0] and davidwar.x < goliath.hitbox[2] + goliath.hitbox[0]:
                            gametime += 1

        while gametime==7: #David vs Goliath scene
            scene_7 = (
                'David put a stone into the sling and threw it.', '(press spacebar to hit Goliath)', 
                'It struck Goliath’s forehead and knocked him down. ')
            clock.tick(30)
            if shoot > 0:
                shoot += 1
            if shoot > 3:
                shoot = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            if i == 0 or i == 1:
                pygame.draw.rect(screen, orange, [95, 535, 620, 50])
                words = scene_7[i]
                message_to_screen(words)
                pygame.display.update()
                pygame.time.wait(5000)
                i += 1
            for stone in stones:
                
                if stone.y - stone.radius < goli.hitbox[1] + goli.hitbox[3] and stone.y + stone.radius > goli.hitbox[1]:
                    if stone.x + stone.radius > goli.hitbox[0] and stone.x - stone.radius < goli.hitbox[2] + goli.hitbox[0]: #collision
                        goli.hit()
                        if health > 0:
                            health -= 10
                        stones.pop(stones.index(stone))
                        if health == 0:
                            pygame.draw.rect(screen, orange, [95, 535, 620, 50])
                            words = scene_7[2]
                            message_to_screen(words)
                            
                            pygame.display.update()
                            pygame.time.wait(5000)
                            i = 0
                            gametime += 1

                if stone.x < 800 and stone.x > 0:
                    stone.x += stone.vel
                else:
                    stones.pop(stones.index(stone)) #erases the stones when leaving the screen

            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE] and shoot == 0:
                if david.left:
                    facing = -1
                else:
                    facing = 1
                if len(stones) < 5:
                    stones.append(Projectile(round(david.x + david.width//2), round(david.y + david.length//2), 6, (160,160,160), facing))

                shoot = 1
            if keys[pygame.K_LEFT] and david.x > david.vel: 
                david.x -= david.vel
                david.left = True
                david.right = False
            elif keys[pygame.K_RIGHT] and david.x < 800 - david.vel - david.width:  
                david.x += david.vel
                david.left = False
                david.right = True
                
            elif not(david.jump): 
                if keys[pygame.K_UP] and david.y > david.vel: 
                    david.y -= david.vel
                    david.up = True
                    david.down = False
                elif keys[pygame.K_DOWN] and david.y < 600 - david.vel - david.length:  
                    david.y += david.vel
                    david.up = False
                    david.down = True

            else:
                    exit
            dvg()

        while gametime == 8: #final scene
            keys = pygame.key.get_pressed()
            scene_8 = ('The Israelites defeated the Philistines.', 'With God’s help, David was a hero!')
            mouse = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                    pygame.display.quit()
                    pygame.quit
            screen.blit(coronation, (0,0))
            pygame.display.update()
            clock.tick(60)
            pygame.draw.rect(screen, orange, [95, 535, 620, 50])
            words = scene_8[i]
            message_to_screen(words)
            
            pygame.display.update()
            pygame.time.wait(5000)
            i += 1
            if i == 1:
                gametime += 1
                i = 0
        while gametime == 9:
            test()

#### program starts here ########         
 
gameloop()