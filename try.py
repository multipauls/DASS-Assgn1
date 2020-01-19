from __future__ import print_function
import time
import tty
import sys
import signal
import fcntl
import termios
import struct
import numpy as np

#copied here
class _getChUnix:
    '''class to take input'''

    def __call__(self):
        '''def to call function'''

        fedvar = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fedvar)
        try:
            tty.setraw(sys.stdin.fileno())
            charvar = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fedvar, termios.TCSADRAIN, old_settings)
        return charvar

class AlarmException(Exception):
    '''This class executes the alarmexception.'''
    pass

#copied code begins here
def inputChar():
    ''' moves Mario'''
    def alarmHandler(signum, frame):
        ''' input method '''
        raise AlarmException

    def userInput(timeout=0.2):
        ''' input method '''
        signal.signal(signal.SIGALRM, alarmHandler)
        signal.setitimer(signal.ITIMER_REAL, timeout)

        try:
            text = _getChUnix()()
            signal.alarm(0)
            return text
        except AlarmException:
            pass
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return ''

    char = userInput()
    return char

#copied code ends here



def terminalSize():

    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h


def background(score, timeLeft, life):
  #  print('\u001b[48;5;232m \033[0;0H')
    print(' '*terminalSize()[0])
    print('\u001b[48;5;232m\u001b[38;5;15m' + '-'*terminalSize()[0] + '\u001b[0m')
    for i in range(terminalSize()[1]-2):
        print('\u001b[48;5;232m' + ' '*terminalSize()[0] + '\u001b[0m')
        #print ('\u001b[48;5;232m'+ ' '*terminalSize()[0])
    print('\u001b[48;5;232m\u001b[38;5;70m' + '-'*(terminalSize()[0]-2) + '\u001b[0m')
    print('\u001b[48;5;232m' + ' '*(terminalSize()[0]-1) + '\u001b[0m')
    print('\u001b[48;5;232m \u001b[38;5;15m \033[0;1H SCORE:'+str(score)+' LIFE:'+ str(life)+' TIME LEFT:'+str(timeLeft)+  '\u001b[0m')




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

        self._j = self._y
        print('\u001b[48;5;232m \u001b[38;5;74m')
        for i in f:
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
        print('\u001b[48;5;232m \u001b[38;5;223m \033['+str(self._y)+';'+str(self._x)+'H O \u001b[0m')
        print('\u001b[48;5;232m \u001b[38;5;58m \033['+str(self._y+1)+';'+str(self._x)+'H K \u001b[0m')
        #+str(self.x)+str(self.y)+' '+str(terminalSize()[1]))

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


    def moveDin(self, speedVal, magnetFlag, magX):
        if self._speedBoost == 0:
            if (speedVal == 'w') and self._y > 3:
                self._y -= 1
            elif (speedVal == 'a' and self._x > 0):
                self._x -= 1
            elif (speedVal == 'd' and self._x < terminalSize()[0]):
                self._x += 1
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
        self._coords=[self._x, self._y]
        if self._x != -1:
            print(' \u001b[48;5;232m \u001b[38;5;14m \033[' + str(self._y) +';' + str(self._x) + 'H * \u001b[0m')




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



def mainGame():

    gravCount = 0
    coinList = []
    bulletList = []
    enBulletList = []
    vertBeamList = []
    horiBeamList = []
    leftBeamList = []
    rightBeamList = []
    cloudList=[]
    timeLeft = 50
    score = 0
    life = 100
    spBoost = None
    shieldBoost = None
    magnet=None
    magnetFlag=0
    boostRandomiser = np.arange(0, 100, 0.2)
    spBoostTime = np.random.choice(boostRandomiser)
    shieldTime = np.random.choice(boostRandomiser)
    magTime = np.random.choice(boostRandomiser)
    Din = dinObject()
    dragon=dragonObject()
    while True:
        time.sleep(0.01)
        timeLeft -= 0.2
        DinPos=Din.getCoords()
        background(score, timeLeft, life)
        for i in range(len(coinList)):
            coinList[i].renderObject()
            coinPos=coinList[i].getCoords()
            #print(DinPos[0], coinPos)
            if DinPos[0] == coinPos or DinPos[1] == coinPos:
                    coinList[i].changeX()
                    score += 20


#        for i in range(len(bulletList)):
#            bulletList[i].renderObject()

        for i in range(len(vertBeamList)):
            vertBeamList[i].renderObject()
            vertPos=vertBeamList[i].getCoords()
            for j in range(len(vertPos)):
                if DinPos[0] == vertPos[j] or DinPos[1] == vertPos[j]:
                    vertBeamList[i].changeX()
                    
                    life -= 2
                    break

        for i in range(len(horiBeamList)):
            horiBeamList[i].renderObject()
            horiPos=horiBeamList[i].getCoords()
            for j in range(len(horiPos)):
                if DinPos[0] == horiPos[j] or DinPos[1] == horiPos[j]:
                    horiBeamList[i].changeX()
                    
                    life -= 2
                    break

        for i in range(len(leftBeamList)):
            leftBeamList[i].renderObject()
            leftPos=leftBeamList[i].getCoords()
            for j in range(len(leftPos)):
                if DinPos[0] == leftPos[j] or DinPos[1] == leftPos[j]:
                    leftBeamList[i].changeX()
                    
                    life -= 2
                    break
           
        for i in range(len(rightBeamList)):
            rightBeamList[i].renderObject()
            rightPos=rightBeamList[i].getCoords()
            for j in range(len(rightPos)):
                if DinPos[0] == rightPos[j] or DinPos[1] == rightPos[j]:
                    rightBeamList[i].changeX()
                    
                    life -= 2
                    break

#        for i in range(len(cloudList)):
#            cloudList[i].renderObject()

        if (life <= 0):
            #endgame
            break

        if (timeLeft <= magTime and magnet == None):
            magnet = magnetObject()
            magnetFlag=1

        elif magnet != None and magnet.getXY()[0] > -1:
            magnet.renderObject()
        
        else:
            magnetFlag=0


        if timeLeft <= 0:
            #endgame
            break



        elif timeLeft <= 10:
            DinY=Din.getXY()[1]
            dragon.renderObject(DinY)
            if timeLeft%1 <= 0.2:
                enBullet=enBulletObject(terminalSize()[0]-11,DinY)
                enBulletList.append(enBullet)
            for i in range(len(enBulletList)):
                enBulletList[i].renderObject()


        else:    
            if (timeLeft <= spBoostTime and spBoost == None):
                spBoost = speedBoost()

            elif spBoost != None and spBoost.getXY()[0] > -1:
                spBoost.renderObject()

            if (timeLeft <= shieldTime and shield == None):
                shieldBoost = shield()

            elif shieldBoost != None and shieldBoost.getXY()[0] > -1:
                shieldBoost.renderObject()

            

            
            '''
            prob = np.random.random_sample()
            if(prob >= 0.99):
                cloud = cloudObject()
                cloudList.append(cloud)
            '''

            prob = np.random.random_sample()

            if(prob >= 0.90):
                coin = bgCoin()
                coinList.append(coin)

            prob = np.random.random_sample()
            if(prob >= 0.95):
                beam = vertBeam()
                vertBeamList.append(beam)

            prob = np.random.random_sample()
            if(prob >= 0.95):
                beam = horiBeam()
                horiBeamList.append(beam)
            
            prob = np.random.random_sample()
            if(prob >= 0.95):
                beam = diagLeftBeam()
                leftBeamList.append(beam)

            prob = np.random.random_sample()
            if(prob >= 0.95):
                beam = diagRightBeam()
                rightBeamList.append(beam)
            

        
        Din.renderObject()
        val = inputChar()

        if (val == 'q'):
            break
        elif (val == 'b'):
            x, y = Din.getXY()
            bullet = flyingObject(x, y)
            bulletList.append(bullet)

        elif magnetFlag==1:
            Din.moveDin(val,magnetFlag,magnet.getXY()[0])

        else:
            Din.moveDin(val,magnetFlag,0)


mainGame()