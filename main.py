#!/usr/bin/python3
import pygame
import random
import Classes

direction = 0

#how many pixels should an object move on each tick?
ANIM_SPEED = 1
#limit frame rate to FPS with clock.tick(FPS) in your main loop.
FPS = 20
#go fullscreen on 'f' keypress. TODO: have pygame determine fullscreen size.
FULLSCREEN_DIM = (1366,768)
#prepend log statements with 'if VERBOSE == True:' and quickly toggle it on/off for debugging.
VERBOSE = True

clock = pygame.time.Clock()
pygame.init()

def init_display(WIDTH,HEIGHT):
    global screen,background
    SIZE = WIDTH, HEIGHT
    if WIDTH <= 800:
        screen = pygame.display.set_mode(SIZE)
    if WIDTH > 800:
        screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
    background = screen.copy()
    background.fill((0, 0, 0, 0))
    screen.blit(background, (0, 0))

init_display(800,600)

#########################################main. some setup, then enter draw/update/check for input endless loop.
def main():
    global direction,FPS
    direction_length = 0
    #myword = create_word_blurb('hello world')

    """Creating our objects"""
    cloudimage = pygame.image.load('png/clouds2.png')
    cloudimage = pygame.transform.smoothscale(cloudimage,(screen.get_width(),300))
    cloud2 = pygame.image.load('png/clouds2.png')
    cloud2 = pygame.transform.smoothscale(cloud2,(screen.get_width(),300))
    clouds = Classes.BackgroundImage('clouds',cloudimage,(0,0),(0,0),cloud2)

    """ Classes.Player: 'title',image,target,position,offset,speed=1 """
    boy1 = pygame.image.load('png/boy.png')
    boy = Classes.Player('boy',boy1,position=[0,500],target=[400,420],offset=[52,85])

    girl1 = pygame.image.load('png/girl5.png')
    girl = Classes.Player('girl',girl1,position=[00,1],target=[400,450],offset=[53,95])

    boy2_image = pygame.image.load('png/char10.png')
    boy2 = Classes.Player('boy2',boy2_image,position=[800,1],target=[500,450],offset=[57,100])

    #girl2_image = pygame.image.load('png/char13.png')
    #girl2 = Classes.Player('girl2',girl2_image,position=[300,600],target=[200,450],offset=[57,100])

    selected_player = random.choice(Classes.Player.register)


    """Other assorted things on screen"""
    exit_sign = pygame.image.load('png/exit.png')
    exit_sign = pygame.transform.smoothscale(exit_sign,(60,30))
    background.blit(exit_sign,exit_sign.get_rect().move(0,0))



    #Hopefully this can help troubleshoot, and also illustrate how to access an object's attributes.
    #Getting/setting position or target is done with 'object.target.x = 300' or 'object.position.y = 10'
    if VERBOSE == True:
        for i in Classes.BackgroundImage.register:
            for k,v in zip(i.__dict__.keys(),i.__dict__.values()):
                print ("{}: {}".format(k,v) )
            print("position: {},{}".format(i.position.x,i.position.y))
            print("target: {},{}".format(i.target.x,i.target.y))
            print("-------------------------")

    #myword.target.x,myword.target.y = (400,30)

################## Main update/draw/listen loop ####
    running = True
    while running:
        pygame.key.set_repeat(1,50)

        tick=clock.tick(FPS)

        # UPDATE GAME OBJECTS
        for x in Classes.BackgroundImage.register:
            x.update(tick)
        for x in Classes.Player.register:
            x.update(tick)

        # DRAW GAME OBJECTS
        screen.blit(background, (0, 0))  # Fill entire screen.
        for x in Classes.BackgroundImage.register:
                x.draw(screen)
        for x in Classes.Player.register:
                x.draw(screen)

        pygame.display.update()

        # HANDLE EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                cx,cy = pygame.mouse.get_pos()
                if (cx < 60) and (cy < 30):
                    print("clicked exit sign")
                    running = False
                print("clicked {},{}".format(cx,cy))
                for i in Classes.Player.register:
                    if i.position.collidepoint(cx,cy) == True:
                        print("Clicked: {}".format(i.title) )
                        for k,v in zip(i.__dict__.keys(),i.__dict__.values()):
                            print ("{}: {}".format(k,v) )
                        print("position: {},{}".format(i.position.x,i.position.y))
                        print("target: {},{}".format(i.target.x,i.target.y))
                        print("-------------------------")
                        selected_player = i
                        break

            #keyboard keys
            if event.type == pygame.KEYDOWN:
                try: event.key
                except: event.key="0"
                if event.key == pygame.K_q: #Q - quit
                    print("Quitting due to 'q' press")
                    pygame.quit()
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    selected_player.velocity -=54
                if event.key == pygame.K_RIGHT:
                    direction = 'right'
                    selected_player.velocity +=54
                if event.key == pygame.K_UP:
                    selected_player.target.y = selected_player.position.y -50
                    selected_player.target.x = selected_player.position.x
                if event.key == pygame.K_DOWN:
                    selected_player.target.y = selected_player.position.y +50
                    selected_player.target.x = selected_player.position.x 

                if event.key == pygame.K_t: #N - enter text
                        new_entry = input(prompt='your prompt:')
                        print("user entered: {}".format(new_entry) )
                if event.key == pygame.K_f: #F - full screen
                    if screen.get_width() > 800:
                        init_display(800,600)
                        pygame.event.set_grab(False)
                        break
                    if screen.get_width() == 800:
                        pygame.event.set_grab(True)
                        init_display(*FULLSCREEN_DIM)
                        background.blit(exit_sign,exit_sign.get_rect().move(0,0))

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        selected_player.velocity = 0
                        direction = 0

        if direction == 'right':
            clouds.target.x = clouds.position.x-50
        if direction == 'left':
            clouds.target.x = clouds.position.x+50


if __name__ == '__main__':
    main()
