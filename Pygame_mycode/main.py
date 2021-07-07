import pygame
#from playsound import playsound
#pygame.init()
pygame.font.init()
pygame.mixer.init()
import os

from pygame import key
from pygame.constants import K_RCTRL
from pygame.version import PygameVersion #help finding the path of images

#setting the game window size
WIDTH, HEIGTH = 1000, 700
WIN =pygame.display.set_mode((WIDTH,HEIGTH))
#setting the game window caption
pygame.display.set_caption("warning:this is a dumb game")


WHITE = (255,255,255) #define White Color tuple
BLACK = (0,0,0)#define black color tuple
RED = (255,0,0)#define red color tuple
YELLOW = (255,255,0)#define yellow color tuple
GREEN = (0,255,0)
BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGTH)
FPS = 120 #frames per second(updating rate)
VEL = 5 #for moving speed (if key is pressed)
MAX_BULLETS =5
BULLETS_VEL =7
IMAGE_WIDTH, IMAGE_HEIGHT = 55, 40
BACK = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets','back.png')),(WIDTH,HEIGTH))
HEALTH_FONT = pygame.font.SysFont('comicscans',40) #define the font and size
WINNER_FONT = pygame.font.SysFont('comicscans',100)

#load MP3 file
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','fire.mp3'))


#os.path.join('Assets','spaceship_yellow.png')-->(folder_name,file_name)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))
#scaling&rotating the image->rotating angle as parameter is needed
YELLOW_SPACESHIP =pygame.transform.rotate(
     pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)) ,90)
 

#os.path.join('Assets','spaceship_yellow.png')-->(folder_name,file_name)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))
#scaling&rotating the image->rotating angle as parameter is needed
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)) ,270)


def yellow_moving(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x +yellow.width - VEL < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y -VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y +yellow.height+ VEL < HEIGTH -15:  # DOWN
        yellow.y += VEL

def red_moving(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x+BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x +red.width - VEL < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y -VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y +red.height+ VEL < HEIGTH -18:  # DOWN
        red.y += VEL
        

def win_drawing(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    #setting color of background
    #WIN.fill(WHITE)#fill()內部放RGB tuple->range from 0-255
    #pygame doesn't remove something is drawn
    #therefor should draw something cover every single FPS
    WIN.blit(BACK,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    #add7/7
    RED_HEALTH_BORDER = pygame.Rect(580,15, red_health*25, 10)
    YELLOW_HEALTH_BORDER = pygame.Rect(175, 15,yellow_health*25,10)
    pygame.draw.rect(WIN,GREEN,RED_HEALTH_BORDER)
    pygame.draw.rect(WIN,GREEN,YELLOW_HEALTH_BORDER)

    red_health_text = HEALTH_FONT.render("Health("+str(int(red_health))+")",1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health("+str(int(yellow_health))+")",1,WHITE)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width(),10))
    WIN.blit(yellow_health_text,(10,10))
    #use blit whenever wanna draw some surface on window
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y)) 

    
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW, bullet)
    
    pygame.display.update()#should be manually updated


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()/2 , HEIGTH/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#creating userdefine_event  
#the event status checking part is in the main_game loop
YELLOW_HIT =pygame.USEREVENT +1 #plus different number for unique ID(RED_HIT is just an ID)
RED_HIT =pygame.USEREVENT +2 #plus different number for unique ID(YELLOW_JIT is just an ID)

#checking colliding or not
def bullets_judge(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        #use the inbuild function colliderect()->only for two rectangle object
        if red.colliderect(bullet):#for red be hitten by yellow bullets 
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x >WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        #use the inbuild function colliderect()->only for two rectangle object
        if yellow.colliderect(bullet):#for red be hitten by yellow bullets 
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0 :
            red_bullets.remove(bullet)

    

#put every main game loop inside main
def main():
    #define the corresponding rectangle for each image
    #as moving the rectangle x,y ,we can consequently moving the image
    red =pygame.Rect(750,300,IMAGE_WIDTH,IMAGE_HEIGHT)
    yellow =pygame.Rect(250,300,IMAGE_WIDTH,IMAGE_HEIGHT)

    red_bullets =[]
    yellow_bullets =[]
    red_health =10
    yellow_health =10
    red_text_num=10
    yellow_text_num=10
    

    clock = pygame.time.Clock()#define clock variable
    running =True
    while running:
        clock.tick(FPS)#ensuring frame rate never exceed 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #the if statement is making the (while loop break out)
            #whenever any quit requirement is catered
        #another keydetecting means(just count the key pressed)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(yellow_bullets)<=MAX_BULLETS:
                #create a bullet whenever the LCTRL is pressed
                #Rect(x,y,width,heigth)
                bullet = pygame.Rect( yellow.x+yellow.width, yellow.y+yellow.height//2 -2,10, 5)#two slashes for integer division
                yellow_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()

            if event.key == pygame.K_RCTRL and len(red_bullets)<=MAX_BULLETS:
                bullet = pygame.Rect( red.x, red.y+red.height//2 -2,10, 5)
                red_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()


        if event.type == RED_HIT:
            red_health *=0.995
            BULLET_HIT_SOUND.play()

        if event.type == YELLOW_HIT:
            yellow_health *=0.995
            BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0.2:
            winner_text = "Left Wins!"
        if yellow_health <= 0.2:
            winner_text = "Right wins!"
        if winner_text !="":
            draw_winner(winner_text)
            break

        #pygame.key.get_pressed(): powerful enough to detecting wether the key is being pressed
        global keyspressed 
        keyspressed= pygame.key.get_pressed()
        yellow_moving(keyspressed,yellow)
        red_moving(keyspressed,red)

        bullets_judge(yellow_bullets,red_bullets,yellow,red)

        win_drawing(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)

    pygame.quit()

#若沒有此行 if __name__ == "__main__": 
#此main在其他file中被import遊戲會直接跳出
if __name__ == "__main__":
    main()
