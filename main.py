# Import of pygame-library
import pygame
import random
from pygame.locals import *

# initialise of pygame
pygame.init()

# variables/constants
WINDOWWIDTH, WINDOWHEIGHT = 1080, 720
FPS                         = 60
WHITE                       = ( 255, 255, 255 )
RED                         = ( 255, 0, 0 )
GREEN                       = ( 0, 255, 0 )
BLUE                        = ( 0, 0, 255 )
YELLOW                      = ( 255, 255, 0 )
GREY                        = ( 155, 155, 155 )

gameaktiv                   = True
gameLost                    = False
draftResult                 = "none"      
ravenPosStart               = 10

# open window
screen = pygame.display.set_mode( ( WINDOWWIDTH, WINDOWHEIGHT ) )

# button function
# define classes
class Element:
    def __init__( self, name, posX, posY, width, height ):
        self.__name          = name
        self.__picture       = pygame.image.load( "pics/" + self.__name + ".png" ).convert_alpha()
        self.picPosX         = posX
        self.picPosY         = posY
        self.__pictureWidth  = width
        self.__pictureHeight = height
        self.__sizeOfPicture = self.__picture.get_rect()

    def drawPicture( self ):
        screen.blit( pygame.transform.scale(self.__picture, ( self.__pictureWidth, self.__pictureHeight ) ) ,( self.picPosX, self.picPosY ))

class Raven( Element ):
    def __init__( self, name, posX, posY, width, height ):
        Element.__init__( self, name, posX, posY, width, height )

    def moveForward( self ):
        self.picPosX += 130
        #print(self.picPosX)

class Fruit( Element ):
    def __init__( self, name, posX, posY, width, height ):
        Element.__init__( self, name, posX, posY, width, height )
        self.__amount = 4

class Basket( Element ):
    def __init__( self, name, posX, posY, width, height ):
        Element.__init__( self, name, posX, posY, width, height )

class Dice( Element ):
    def __init__( self, name, posX, posY, width, height ):
        Element.__init__( self, name, posX, posY, width, height )
        self.__sign = { 1: "red",
                        2: "green",
                        3: "yellow",
                        4: "blue",
                        5: "raven",
                        6: "basket"
                      }
        self.__rolled   = ""

    def overDice(self, mousePos):
        if mousePos[0] > self.picPosX and mousePos[0] < self.picPosX+self._Element__pictureWidth and mousePos[1] > self.picPosY and mousePos[1] < self.picPosY+self._Element__pictureHeight:
            return True

    def rollDice(self):
        self.__rolled = self.__sign[random.randint(1,6)]

        return self.__rolled

# Object initialisation
dice   = Dice( "dice", 0, 0, 209, 181 )

basket = Basket( "basket", 0,  WINDOWHEIGHT - 266, 269, 266 )

treeList = []
for i in range (0,4):
    if i == 0:
        posX = WINDOWWIDTH / 4
        posY = 0
    if i == 1:
        posX = WINDOWWIDTH / 4 + WINDOWWIDTH / 3
        posY = 0
    if i == 2:
        posX = WINDOWWIDTH / 4 + WINDOWWIDTH / 3
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 3 
    if i == 3:
        posX = WINDOWWIDTH / 4
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 3
    tree       = Fruit ( "tree",
                         posX,
                         posY,
                         int( WINDOWWIDTH / 2 ),
                         int( WINDOWHEIGHT / 2 )
                       )
    treeList.append(tree)
    #print(treeList)
    #print(posX, posY)

fieldList = []
for i in range (0,4):
    if i == 0:
        posX = WINDOWWIDTH / 8
        posY = ( WINDOWHEIGHT / 2 ) - ( ( WINDOWHEIGHT / 6 ) / 2 )
    if i == 1:
        posX = ( WINDOWWIDTH / 8 ) * 2
        posY = ( WINDOWHEIGHT / 2 ) - ( ( WINDOWHEIGHT / 6 ) / 2 )
    if i == 2:
        posX = ( ( WINDOWWIDTH / 8 ) * 3 )
        posY = ( WINDOWHEIGHT / 2 ) - ( ( WINDOWHEIGHT / 6 ) / 2 ) 
    if i == 3:
        posX = ( ( WINDOWWIDTH / 8 ) * 4 )
        posY = ( WINDOWHEIGHT / 2 ) - ( ( WINDOWHEIGHT / 6 ) / 2 )
    field       = Fruit ( "field",
                         posX,
                         posY,
                         int( WINDOWWIDTH / 8 ),#80
                         int( WINDOWHEIGHT / 6 )#70
                       )
    fieldList.append(field)
    #print(fieldList)
    #print(posX, posY)

gate           = Element( "gate",
                          int( ( ( WINDOWWIDTH / 8 ) * 5 ) ),
                          int( ( WINDOWHEIGHT / 2 ) - ( ( WINDOWHEIGHT / 6 ) / 2 ) ),
                          int( WINDOWWIDTH / 8 ),#80
                          int( WINDOWHEIGHT / 6 )#70
                        )

raven          = Raven ( "raven",
                         int( ravenPosStart ),
                         int( ( WINDOWHEIGHT / 2 ) - ( ( WINDOWHEIGHT / 6 ) / 2 ) ),
                         int( WINDOWWIDTH / 8 ),#80
                         int( WINDOWHEIGHT / 6 )#70
                       )

redAppleList = []
for i in range (0,4):
    if i == 0:
        posX = WINDOWWIDTH / 3
        posY = 0
    if i == 1:
        posX = WINDOWWIDTH / 3 + WINDOWWIDTH / 5.5
        posY = 0
    if i == 2:
        posX = WINDOWWIDTH / 3
        posY = WINDOWHEIGHT / 10
    if i == 3:
        posX = WINDOWWIDTH / 3 + WINDOWWIDTH / 5.5
        posY = WINDOWHEIGHT / 10
    redApple      = Fruit ( "redApple",
                         posX,
                         posY, 
                         int( WINDOWWIDTH / 12 ),
                         int( WINDOWHEIGHT / 10 )
                       )
    redAppleList.append(redApple)
    #print(redAppleList)
    #print(posX, posY)

greenAppleList = []
for i in range (0,4):
    if i == 0:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 6
        posY = 0
    if i == 1:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 3
        posY = 0
    if i == 2:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 6
        posY = WINDOWHEIGHT / 10
    if i == 3:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 3
        posY = WINDOWHEIGHT / 10
    greenApple = Fruit ( "greenApple",
                         posX,
                         posY, 
                         int( WINDOWWIDTH / 12 ),
                         int( WINDOWHEIGHT / 10 )
                       )
    greenAppleList.append(greenApple)
    #print(greenAppleList)
    #print(posX, posY)

plumList = []
for i in range (0,4):
    if i == 0:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 6
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 2.8
    if i == 1:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 3
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 2.8
    if i == 2:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 6
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 2.2
    if i == 3:
        posX = WINDOWWIDTH / 2 + WINDOWWIDTH / 3
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 2.2
    plum       = Fruit ( "plum",
                         posX,
                         posY, 
                         int( WINDOWWIDTH / 12 ),
                         int( WINDOWHEIGHT / 10 )
                       )
    plumList.append(plum)
    #print(plumList)
    #print(posX, posY)

pearList = []
for i in range (0,4):
    if i == 0:
        posX = WINDOWWIDTH / 3
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 3
    if i == 1:
        posX = WINDOWWIDTH / 3 + WINDOWWIDTH / 5.5
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 3
    if i == 2:
        posX = WINDOWWIDTH / 3
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 2.2
    if i == 3:
        posX = WINDOWWIDTH / 3 + WINDOWWIDTH / 5.5
        posY = WINDOWHEIGHT / 4 + WINDOWHEIGHT / 2.2
    pear       = Fruit ( "pear",
                         posX,
                         posY, 
                         int( WINDOWWIDTH / 12 ),
                         int( WINDOWHEIGHT / 10 )
                       )
    pearList.append(pear)
    #print(pearList)
    #print(posX, posY)

# window title
pygame.display.set_caption( "Fruit Garden" )

# screen refresh
clock = pygame.time.Clock()

# main-programm
while gameaktiv:
    # Check if user has performed an action
    for event in pygame.event.get():
        mousePosition = pygame.mouse.get_pos()
        #print(mousePosition)
        # exit by [X] or [ESC]
        if event.type == QUIT or ( event.type == KEYDOWN and event.key == K_ESCAPE ):
            gameaktiv = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            # for testing
            pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            if dice.overDice(mousePosition):
                draftResult = dice.rollDice()
            if draftResult == "raven":
                raven.moveForward()
    
            if ( draftResult == "red" ) and ( redAppleList != [] ):
                redAppleList.pop()
            if ( draftResult == "green" ) and ( greenAppleList != [] ):
                greenAppleList.pop()
            if ( draftResult == "blue" ) and ( plumList != [] ):
                plumList.pop()
            if ( draftResult == "yellow" ) and ( pearList != [] ):
                pearList.pop()
            if ( draftResult == "basket" ):
                randomFruit = random.randint(1,4)
                if randomFruit == 1:
                    if redAppleList != []:
                        redAppleList.pop()
                    elif greenAppleList != []:
                        greenAppleList.pop()
                    elif plumList != []:
                        plumList.pop()
                    elif pearList != []:
                        pearList.pop()
                if randomFruit == 2:
                    if greenAppleList != []:
                        greenAppleList.pop()
                    elif redAppleList != []:
                        redAppleList.pop()
                    elif plumList != []:
                        plumList.pop()
                    elif pearList != []:
                        pearList.pop()
                if randomFruit == 3:
                    if plumList != []:
                        plumList.pop()
                    elif redAppleList != []:
                        redAppleList.pop()
                    elif greenAppleList != []:
                        greenAppleList.pop()
                    elif pearList != []:
                        pearList.pop()
                if randomFruit == 4:
                    if pearList != []:
                        pearList.pop()
                    elif redAppleList != []:
                        redAppleList.pop()
                    elif greenAppleList != []:
                        greenAppleList.pop()
                    elif plumList != []:
                        plumList.pop()


    # integrate Gamelogic
    if raven.picPosX > ( ( WINDOWWIDTH /10 ) + ( WINDOWWIDTH /2 ) ):
        gameLost  = True
        gameaktiv = False

    if gameLost == False and not redAppleList and not greenAppleList and not plumList and not pearList:
        gameaktiv = False

    # clear Field
    screen.fill( GREY )

    # Field/Figure draw
    dice.drawPicture()
    sign = pygame.image.load( "pics/" + draftResult + ".png" ).convert_alpha()
    screen.blit( pygame.transform.scale( sign, ( 145, 129 ) ) , ( 32, 26 ) )

    basket.drawPicture()

    for tree in treeList:
        tree.drawPicture()

    for field in fieldList:
        field.drawPicture()

    gate.drawPicture()

    raven.drawPicture()

    for redApple in redAppleList:
        redApple.drawPicture()
    
    for greenApple in greenAppleList:
        greenApple.drawPicture()
    
    for plum in plumList:
        plum.drawPicture()
    
    for pear in pearList:
        pear.drawPicture()
    
    # update Window
    pygame.display.flip()
    clock.tick( FPS )

endsequenz = True

while endsequenz:
    if gameLost == True:
        # Check if user has performed an action
        for event in pygame.event.get():
            # exit by [X] or [ESC]
            if event.type == QUIT or ( event.type == KEYDOWN and event.key == K_ESCAPE ):
                endsequenz = False

        font = pygame.font.SysFont( "comicsansms", 40 )
        lost = font.render( "Verloren", True, ( 0, 128, 0 ) )

        screen.fill( WHITE )
        screen.blit( lost, ( WINDOWWIDTH / 2.5, WINDOWHEIGHT / 3 ) )

        # update Window
        pygame.display.flip()
        clock.tick( FPS )

    else:
        # Check if user has performed an action
        for event in pygame.event.get():
            # exit by [X] or [ESC]
            if event.type == QUIT or ( event.type == KEYDOWN and event.key == K_ESCAPE ):
                endsequenz = False

        font = pygame.font.SysFont( "comicsansms", 40 )
        won = font.render( "Gewonnen", True, ( 0, 128, 0 ) )

        screen.fill( WHITE )
        screen.blit( won, ( WINDOWWIDTH / 2.5, WINDOWHEIGHT / 3 ) )

        # update Window
        pygame.display.flip()
        clock.tick( FPS )

pygame.quit()
print("Kleine Änderung")