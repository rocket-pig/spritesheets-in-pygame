# spritesheets-in-pygame
A working example of using spritesheets in pygame. 
### Spritesheets! What in the g-d hell! ### 
A spritesheet houses all the frames necessary to make a character walk,
or a cloud ...well, make a cloud cloud around a bit. It houses it all in one file.  And pygame is a bit persnickety
about how much howling and screaming you're going to need to do before it will use them.  I read countless pages and
(ahem) "explanations" about how it works, and in the end I just resorted to trying every conveivable combination..
just kidding.  But it was challenging.
![example](https://darknesseverytime.live/mirror/sprites.gif?&raw=true)

  
  
  ...the tricky part boils down to the screen.blit. You need to find your frames' "offset", (think "cursor". Cursor
  makes a lot more sense to my brain anyway.  But in the parlance of our times..."offset".) and set this in your blit.
  
  `screen.blit(self.image,self.position,area=(self.index[0],self.index[1],self.offset[0],self.offset[1]))`
  
  ..something like that.  Anyhow! There's lots of random notes in the code, and the part about controlling the
  character's direction and 'velocity' was also pored over forever and heavily commented. You're free to steal,
  upgrade, enhance, burn, mock, cherish forever, I'm down with whatever.
  
  ### What you get: ###
  Little fluffy clouds. I think theyre from a Simpson's rip. Characters that can walk up, down, left and right. 
  You can click them and (unfortunately only sometimes) it will select them, and change walking control to that
  character.  You can click the EXIT sign in top right to exit, or press 'f' to go in and out of fullscreen.
  
  I hope to have feedback and maybe even collaboration on making 'base model' stuff for pygame.  Please do if so inspired.
