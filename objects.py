from __future__ import print_function
import time
from termSize import terminalSize
import numpy as np

class bgObject:
    def __init__(self):
        self._y = np.random.randint(5, terminalSize()[1]-3)
        self._x = terminalSize()[0]-1
        self._coords = []
    def getCoords(self):
        return self._coords
    def getXY(self):
        return self._x, self._y
   
    def changeX(self):
        self._x = -1

    def moveAcross(self):
        if self._x > 0:
            self._x -= 1
        else:
            self._x = -1

class speedBoost(bgObject):
    def renderObject(self):
        self.moveAcross()
        self._coords=[self._x,self._y]
        if self._x != -1:
            print('\u001b[48;5;232m \033['+ str(self._y) +';' + str(self._x)+'H X')

class shield(bgObject):
    def renderObject(self):
        self.moveAcross()
        self._coords=[self._x,self._y]
        if self._x != -1:
            print('\u001b[48;5;232m \033['+ str(self._y) +';' + str(self._x)+'H C \u001b[0m')


class bgCoin(bgObject):
    def __init__(self):
        super().__init__()

    def renderObject(self):
        self.moveAcross()
        self._coords=[self._x,self._y]
        if self._x != -1:
            print('\u001b[48;5;232m \u001b[38;5;214m \033['+ str(self._y) +';' + str(self._x)+'H O \u001b[0m')

class magnetObject(bgObject):
    def __init__(self):
        super().__init__()
        self._y = 4


    def renderObject(self):
        self.moveAcross()
        self._coords=[self._x,self._y]
        if self._x != -1:
            print(' \u001b[48;5;232m \u001b[38;5;88m \033['+ str(self._y) +';' + str(self._x)+'H Ո \u001b[0m')


class dragonObject(bgObject):
    def __init__(self):
        super().__init__()
        self._x = terminalSize()[0]-15
        self._y = 5

    def renderObject(self, dinY):
        f = open('dragon.txt', 'r')
        if dinY > self._y+8:
            self._y = dinY-8
        elif dinY < self._y:
            self._y = dinY
        self._coords=[]
        self._j = self._y
        print('\u001b[48;5;232m \u001b[38;5;74m')
        for i in f:
            self._coords.append([self._x, self._j])
            print('\033['+ str(self._j) +';' + str(self._x)+'H '+str(i))
            self._j += 1
        print('\u001b[0m')
        f.close()

class cloudObject(bgObject):
    def __init__(self):
        super().__init__()
        self._x = terminalSize()[0]-11
        self._y = 3
    def moveAcross(self):
        if self._x > 11:
            self._x -= 1
        else:
            self._x = -1

    def renderObject(self):
        f = open('cloud.txt', 'r')
        self.moveAcross()
        self._j = self._y
        for i in f:
            print('\u001b[48;5;232m \u001b[38;5;194m \033['+ str(self._j) +';' + str(self._x)+'H '+str(i)+ ' \u001b[0m')
            self._j += 1
        f.close()






class dinObject(bgObject):
    def __init__(self):
        super().__init__()
        self._y = terminalSize()[1]-3
        self._x = 7
        self._speedBoost = 0
        self._shield = 0
        self._magAttract = 0

    def renderObject(self):
        self._coords=[[self._x,self._y],[self._x,self._y+1] ]
        if (self._shield == 0):
            print('\u001b[48;5;232m \u001b[38;5;216m \033['+str(self._y)+';'+str(self._x)+'H O \u001b[0m')
            print('\u001b[48;5;232m \u001b[38;5;58m \033['+str(self._y+1)+';'+str(self._x)+'H K \u001b[0m')
        else:
            print('\u001b[48;5;232m \u001b[38;5;147m \033['+str(self._y)+';'+str(self._x)+'H O \u001b[0m')
            print('\u001b[48;5;232m \u001b[38;5;147m \033['+str(self._y+1)+';'+str(self._x)+'H K \u001b[0m')

    def gravity(self, val):
        if val != 'w' and self._y < terminalSize()[1]-3: 
            self._y += 1
        return self._y

    def magForce(self, flagVal, magX):
        if flagVal==1:
            if self._x>magX:
                self._x-=1

            elif self._x<magX:
                self._x+=1

    def speedUp(self):
        self._speedBoost=1


    def shieldUp(self):
        self._shield=1

    def getShield(self):
        return self._shield

    def moveDin(self, speedVal, magnetFlag, magX):
        if self._speedBoost == 0:
            if (speedVal == 'w') and self._y > 3:
                self._y -= 1
            elif (speedVal == 'a' and self._x > 0):
                self._x -= 1
            elif (speedVal == 'd' and self._x < terminalSize()[0]):
                self._x += 1
            elif (speedVal == ' '):
                self.shieldUp()
            else:
                self.magForce(magnetFlag, magX)
            self.gravity(speedVal)

        else:
            if (speedVal == 'w') and self._y > 3:
                self._y -= 2
            elif (speedVal == 'a' and self._x > 0):
                self._x -= 2
            elif (speedVal == 'd' and self._x < terminalSize()[0]):
                self._x += 2
            elif (speedVal == ' '):
                self.shieldUp()
            else:
                self.magForce(magnetFlag, magX)
            self.gravity(speedVal)


    



class flyingObject(bgObject):
    def __init__(self, x, y):
        super().__init__()
        self._x = x
        self._y = y
        self._coords=[]
    def moveAcross(self):

        if self._x < terminalSize()[0] and self._x != -1:
            self._x += 2
        else:
            self._x = -1

    def renderObject(self):
        self.moveAcross()
        self._coords=[self._x, self._y]
        if self._x != -1:
            print('\u001b[48;5;232m \u001b[38;5;196m \033[' + str(self._y) +';' + str(self._x) + 'H > \u001b[0m')

class enBulletObject(flyingObject):

    def moveAcross(self):

        if self._x < terminalSize()[0] and self._x != -1:
            self._x -= 2
        else:
            self._x = -1

    def renderObject(self):
        self.moveAcross()
        self._coords=[[self._x, self._y], [self._x+1, self._y]]
        if self._x != -1:
            print(' \u001b[48;5;232m \u001b[38;5;14m \033[' + str(self._y) +';' + str(self._x) + 'H <@ \u001b[0m')




class bgBeams(bgObject):

    def __init__(self):

        super().__init__()
    def changeX(self):
        self._x = -1
        for i in range(len(self._coords)):
            self._coords[i][0]=-1

class vertBeam(bgBeams):
    def __init__(self):
        super().__init__()
        self._y = np.random.randint(5, terminalSize()[1]-3)


    def moveAcross(self):
        if self._x > 0:
            self._x -= 1
        else:
            self._x = -1


    def renderObject(self):
        self.moveAcross()


        if self._x != -1:
            self._j = self._y-2

            for i in range(5):
                self._coords.append([self._x,self._j])
                print('\u001b[48;5;232m \u001b[38;5;228m \033['+ str(self._j) +';' + str(self._x) + 'H 0 \u001b[0m')
                self._j += 1


class horiBeam(bgBeams):
    def __init__(self):
        self._y = np.random.randint(5, terminalSize()[1]-3)
        super().__init__()


    def moveAcross(self):
        if self._x > 5:
            self._x -= 1
        else:
            self._x = -1


    def renderObject(self):
        self.moveAcross()

        if self._x != -1:
            self._j = self._x-8
            for i in range(5):
                self._coords.append([self._j,self._y])
                self._coords.append([self._j+1,self._y])
                print('\u001b[48;5;232m \u001b[38;5;228m \033['+ str(self._y) +';' + str(self._j) + 'H 0 \u001b[0m')
                self._j += 2

class diagBeam(bgBeams):
    def __init__(self):
        super().__init__()
        self._y = np.random.randint(5, terminalSize()[1]-3)


    def moveAcross(self):
        if self._x > 5:
            self._x -= 1
        else:
            self._x = -1

class diagLeftBeam(diagBeam):
    def __init__(self):
        super().__init__()

    def renderObject(self):
        self.moveAcross()

        if self._x != -1:
            self._j = self._x-8
            self._k = self._y-2
            
            for i in range(5):
                self._coords.append([self._j,self._k])
                self._coords.append([self._j+1,self._k])
                print('\u001b[48;5;232m \u001b[38;5;209m \033['+ str(self._k) +';' + str(self._j) + 'H 0 \u001b[0m')
                self._j += 2
                self._k += 1
            
class diagRightBeam(diagBeam):
    def __init__(self):
        super().__init__()

    def renderObject(self):
        self.moveAcross()

        if self._x != -1:
            self._j = self._x-8
            self._k = self._y-2
            for i in range(5):
                self._coords.append([self._j,self._k])
                self._coords.append([self._j-1,self._k])
                print('\u001b[48;5;232m \u001b[38;5;209m \033['+ str(self._k) +';' + str(self._j) + 'H 0 \u001b[0m')                
                self._j -= 2
                self._k += 1
            print('\u001b[0m')


