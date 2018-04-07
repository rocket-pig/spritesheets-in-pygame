
#get 'close enough' to target. returns how close we are in px.
def calc_distance(c1,c2):
    test = max( (abs(c1[0] - c2[0])), (abs(c1[1] - c2[1])) )
    return(test)

class BackgroundImage: #totally
    register = []
    def __init__(self, title, image, target, position, cloud2, speed=1, left=False, right=False,next_side=None):
        self.__class__.register.append(self)
        self.title      = title
        self.image      = image
        self.target     = image.get_rect().move(*target)
        self.position   = image.get_rect().move(*position)
        self.c2i        = cloud2
        self.c2t        = cloud2.get_rect().move(*target)
        self.c2p        = cloud2.get_rect().move(*position)
        self.speed      = speed
        self.right      = right
        self.left       = left
        self.next_side  = None
        self.next_cloud   = False
    def update(self,screen,tick=0):
        if calc_distance(
          (self.position.x,self.position.y),
          (self.target.x,self.target.y)   ) <= self.speed:
                self.position.x = self.target.x
                self.position.y = self.target.y
        if self.position.y > self.target.y:
            self.position.y -= self.speed
        elif self.position.y < self.target.y:
            self.position.y += self.speed
        if self.position.x > self.target.x:
            self.position.x -= self.speed
        elif self.position.x < self.target.x:
            self.position.x += self.speed

        #keep track of scrolling, toggle next cloud if needed.
        #print("position x:{}".format(self.position.x<1))
        if self.position.x < 1:
            self.next_side = 'right'
            self.c2p.x,self.c2p.y = self.position.x+800,0
        if self.position.x > 1:
            self.next_side = 'left'
            self.c2p.x,self.c2p.y = self.position.x-800,0
        if self.position.x > 800:
            self.position.x = 0
        if self.position.x < -800:
                self.position.x = 0
    #draw
    def draw(self, screen):
        if self.next_side == 'right':
            screen.blit(self.c2i,self.c2p)
        if self.next_side == 'left':
            screen.blit(self.c2i,self.c2p)
        screen.blit(self.image, self.position)


#this spritesheet shit is so fucking confusing. Notes for later.
# 'offset' set in instantiation is the width,height of an individual pic in the sheet.
#the update() func expects a sheet where player is moving left on top row, right on bottom.
#if we're moving right, it will shift down by length of height 'offset' and start loading pics from there.
#for each time update is called and keydown hasnt stopped, it will advance width-offset-length out from 0
#and return that pic. until it reaches width*5. why 5 when theres 7 pics you say? because pic 1
#is standing still. pic2 is the one we begin on when key goes down. every advance from there = a total of 5.
#TLDR: when you use a spritesheet, youll want to know the width and height of individual frames, and dump that into
#'offset' when you instantiate. if its in a diff format than described above (top row moves left, etc), youll
#have to dig into the 'velocity' stuff below and figure out how to tell it to move the 'cursor' somewhere else in the file.

class Player:
    register = []
    def __init__(self,title,image,offset=[0,0],position=[0,0],target=[0,0],speed=1):
        self.__class__.register.append(self)
        self.title      = title
        self.image      = image
        self.target     = image.get_rect().move(*target)
        self.position   = image.get_rect().move(*position)
        self.velocity     = 0
        self.offset     = offset
        self.speed      = 5
        self.length     = offset[0]*5
        self.current    = 0
        self.index      = [0,0]
    def update(self,tick):
        current_vel = 0 #only used to make sure right animation is displayed. ignore otherwise.
        if self.target.x != 0 and self.target.y != 0: #reserved for 'no target'
            if calc_distance(
              (self.position.x,self.position.y),
              (self.target.x,self.target.y)   ) <= self.speed:
                    self.position.x = self.target.x
                    self.position.y = self.target.y
                    self.velocity = 0
                    self.target.x = 0
                    self.target.y = 0
                    return
            if self.position.y > self.target.y:
                self.position.y -= self.speed
                current_vel -=1
            elif self.position.y < self.target.y:
                self.position.y += self.speed
                current_vel+=1
            if self.position.x > self.target.x:
                self.position.x -= self.speed
                current_vel-=1
            elif self.position.x < self.target.x:
                self.position.x += self.speed
                current_vel+=1
            # then theres the case where character
            #  is being sent right-to-left and down:
            if self.position.x > self.target.x and\
             self.position.y < self.target.y: current_vel-=1

        #get current direction from ^^:
        #x 52 y 85
        self.velocity += current_vel
        if self.velocity > 0:       # we are velocity right
           self.index[1] = self.offset[1] # = 85      # move down to bottom row of pics.
           self.position.x+=3      #move our on-screen position +1

        elif self.velocity < 0:     #we are velocity left.
            self.index[1] = 0       # = 0      #use top row of pics.
            self.position.x-=3     #move our on-screen position -1

        if self.velocity == 0:      #if this isnt here, animation continues even when we lift key.
            self.index[0] = 0       # = 0
        else:                       #..because 'else' of velocity being zero: we only continue if vel is +/- zero.

            self.current+= self.offset[0]       #advance out 52 pix to next offset.
            if self.current >= self.length: #if we just advanced off the pic, go back to zero
                self.current = 0
            if self.index[0] >= self.length - self.offset[0]: #if offset is insane, reset that too.
                self.index[0] = 0
            self.index[0]+=self.current #update offset with our +1 right/left frame.

    def draw(self,screen):
        #'area='cursor position x, cursor position y. move here, then select to offset x, offset y. jeez.
        screen.blit(self.image,self.position,area=(self.index[0],self.index[1],self.offset[0],self.offset[1]))


