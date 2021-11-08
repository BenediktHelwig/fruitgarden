import pygame
import random


class Element:
    def __init__( self, name ):
        self.__name          = name
        self.__picture       = pygame.image.load( "pics/" + self.__name + ".png" ).convert_alpha()
        self.__sizeOfPicture = self.__picture.get_rect()

    def getPicture(self):
        screen.blit(self.__picture,(200,100))

    def getSizeOfPicture(self):
        return self.__sizeOfPicture

class Tree(Element):
    def __init__( self, name, fruits ):
        super.__init__( self, name )
        

class Fruit(Element):
    def __init__(self, type):
        super().__init__(type)
    def putInBasket(self):
        # return -1
        pass

class Raven(Element):
    def __init__(self, type):
        super().__init__(type)
    def moveForward(self):
        # return +1
        pass

class Basket(Element):
    def __init__(self, type):
        super().__init__(type)
    def fill_in(self):
        # Liste plus eins
        pass
    def content(self):
        # Inhalt anzeigen
        pass

class Dice:
    def __init__(self):
        sideOne   = "Red"
        sideTwo   = "Green"
        sideThree = "Blue"
        sideFour  = "Yellow"
        sideFife  = "Basket"
        sideSix   = "Raven"
    def rollTheDice(self):
        number = random.randint( 0, 5 )
        return number
