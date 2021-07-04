import pygame
import os #help finding the path of images

#setting the game window size
WIDTH, HEIGTH = 1000, 700
WIN =pygame.display.set_mode((WIDTH,HEIGTH))
#setting the game window caption
pygame.display.set_caption("warning:this is a dumb game")


WHITE = (255,255,255) #define White Color tuple
BLACK = (0,0,0)#define black color tuple
BORDER = pygame.Rect(WIDTH/2 -5, 0, 10, HEIGTH)
FPS = 120 #frames per second(updating rate)
VEL = 5 #for moving speed (if key is pressed)
IMAGE_WIDTH, IMAGE_HEIGHT = 55, 40


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
        


def win_drawing():
    #setting color of background
    WIN.fill(WHITE)#fill()內部放RGB tuple->range from 0-255
    pygame.draw.rect(WIN,BLACK,BORDER)
    #use blit whenever wanna draw some surface on window
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    pygame.display.update()#should be manually updated



#put every main game loop inside main
def main():
    #define the corresponding rectangle for each image
    #as moving the rectangle x,y ,we can consequently moving the image
    global red
    red =pygame.Rect(750,300,IMAGE_WIDTH,IMAGE_HEIGHT)
    global yellow
    yellow =pygame.Rect(250,300,IMAGE_WIDTH,IMAGE_HEIGHT)


    clock = pygame.time.Clock()#define clock variable
    running =True
    while running:
        clock.tick(FPS)#ensuring frame rate never exceed 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #the if statement is making the (while loop break out)
            #whenever any quit requirement is catered
        
        #pygame.key.get_pressed(): powerful enough to detecting wether the key is being pressed
        global keys_pressed 
        keyspressed= pygame.key.get_pressed()
        yellow_moving(keyspressed,yellow)
        red_moving(keyspressed,red)

        win_drawing()

    pygame.quit()

#若沒有此行 if __name__ == "__main__": 
#此main在其他file中被import遊戲會直接跳出
if __name__ == "__main__":
    main()
