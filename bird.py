import pygame ,sys
import time
import random
#CLASS
class Explosion(pygame.sprite.Sprite):
        def __init__(self,pos_x,pos_y):
            super().__init__()
            self.sprites = []
            for i in range(1,6):
                surface = pygame.image.load("assets/exp{}.png".format(i)).convert_alpha()
                self.sprites.append(surface)
            self.index = 0
            self.image = self.sprites[self.index]
            self.rect = self.image.get_rect(center=(pos_x,pos_y))

        def update(self):
            if self.index <= len(self.sprites):
                self.index +=1
            else:
                self.index =0            
#Functions
def floor_draw():
    screen.blit(floor,(flr_x_pos,580))
    screen.blit(floor,(flr_x_pos + 336,580))
    screen.blit(floor,(flr_x_pos + 576,580))
def create_pipe():
    x = random.randint(300,550)
    top_pipe = pipe.get_rect(midbottom=(600,random.randint(80,240)))
    bot_pipe = pipe.get_rect(midtop=(600,x))
    return bot_pipe,top_pipe

def draw_pipes(pipes):
    for p in pipes:
        if p.top <= 0:
            flip_pipe = pygame.transform.flip(pipe,False,True)
            screen.blit(flip_pipe,p)
        else:    
            screen.blit(pipe,p)    
def move_pipes(pipes):
    for p in pipes:
        if p.left <= -576:
           pipes.remove(p)
        p.centerx -= 4
def collision(pipes):
    if bird_rect.bottom >=650 or bird_rect.top <= -1:
        die.play()
        return False 
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit.play()
            return False
    return True 
def rotate_bird():
    rbird = pygame.transform.rotozoom(bird,-bird_movement*2,1)
    return rbird
def flapanima():
    new_bird = bird_frame[index]
    new_rect = new_bird.get_rect(center=(bird_rect.centerx,bird_rect.centery))
    return new_bird,new_rect    

pygame.init()
screen = pygame.display.set_mode((576,650))
clock = pygame.time.Clock()
#USEREVENTS
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1000)

FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(FLAP,100)

#Game variables
grv = 0.25
bird_movement =0
grv_x = 0.04
bird_x_move = 0
game_active = True

bg = pygame.image.load('assets/bgnight.png').convert()
bg = pygame.transform.scale2x(bg)

pipe = pygame.image.load('assets/pipe-red.png').convert()
pipes = []

floor = pygame.image.load("assets/base.png").convert()
flr_x_pos = 0

upbird = pygame.image.load('assets/uflap.png').convert_alpha()
midbird = pygame.image.load("assets/redbird.png").convert_alpha()
dbird = pygame.image.load('assets/dflap.png').convert_alpha()
bird_frame = [dbird,midbird,upbird]
index =0
bird = bird_frame[index]
bird_rect = bird.get_rect(center=(100,324))
#SPRITES

#spr_grp = pygame.sprite.Group()
#exp = Explosion(100,300)
#spr_grp.add(exp)
#SOUNDS
wing = pygame.mixer.Sound('assets/sfx_wing.wav')
boost = pygame.mixer.Sound('assets/fart.wav')
hit = pygame.mixer.Sound('assets/sfx_hit.wav')
die = pygame.mixer.Sound('assets/die.wav')
#TEXTS
font = pygame.font.Font('assets/Oswald-Bold.ttf',60)
text = font.render('PRESS SPACE',True,(255,0,0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                wing.play()
                bird_movement = 0
                bird_movement  -= 8  
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center =(100,324)
                pipes.clear()
                bird_movement =0
                bird_x_move =0
                game_active = True
            if event.key == pygame.K_b:
                boost.play()
                bird_x_move =4
                bird_rect.centerx += 12        
        if event.type == SPAWNPIPE:
            pipes.extend(create_pipe())  
        if event.type == FLAP:
            if index <2:
                index +=1
            else:
                index=0
            bird,bird_rect = flapanima()                       
    
    screen.blit(bg,(0,0))
    if game_active:
        #BIRD
        bird_movement += grv
        bird_rect.centery += bird_movement
        #draw bird
        Rbird = rotate_bird()
        screen.blit(Rbird,bird_rect)
        game_active = collision(pipes)
        bird_x_move -= grv_x
        bird_rect.centerx += bird_x_move
        if bird_rect.centerx <= 100:
            bird_rect.centerx =100
        #PIPES
        move_pipes(pipes)
        draw_pipes(pipes)
        #Explosion
    else:    
        screen.blit(text,(130,200))    
    #FLOOR
    flr_x_pos -=1
    floor_draw()
    if flr_x_pos < -335:
        flr_x_pos = 0
    
    pygame.display.update()        
    clock.tick(60)
