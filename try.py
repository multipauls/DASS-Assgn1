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


def background(score, timeLeft):
    print('\033[0;0H')
    print(' '*terminalSize()[0])
    print('\033[0;1H SCORE:'+str(score)+' TIME LEFT:'+str(timeLeft))
    print('-'*terminalSize()[0])
    for i in range(terminalSize()[1]-4):
        print(' '*terminalSize()[0])
    print('-'*terminalSize()[0])





class bgObject:
    def __init__(self):
        self.y = np.random.randint(5, terminalSize()[1]-3)
        self.x = terminalSize()[0]-1

    def getXY(self):
        return self.x, self.y

    def moveAcross(self):
        if self.x > 0:
            self.x -= 1
        else:
            self.x = -1

class speedBoost(bgObject):
    def renderObject(self):
        self.moveAcross()
        if self.x != -1:
            print('\033['+ str(self.y) +';' + str(self.x)+'H X')

class shield(bgObject):
    def renderObject(self):
        self.moveAcross()
        if self.x != -1:
            print('\033['+ str(self.y) +';' + str(self.x)+'H C')


class bgCoin(bgObject):
    def __init__(self):
        super().__init__()

    def renderObject(self):
        self.moveAcross()
        if self.x != -1:
            print('\033['+ str(self.y) +';' + str(self.x)+'H O')

class magnetObject(bgObject):
    def __init__(self):
        super().__init__()
        self.y = 4


    def renderObject(self):
        self.moveAcross()
        if self.x != -1:
            print('\u001b[38;5;88m')
            print('\033['+ str(self.y) +';' + str(self.x)+'H O')
            print('\u001b[0m')


class dragonObject(bgObject):
    def __init__(self):
        super().__init__()
        self.x = terminalSize()[0]-15
        self.y = 5
    def renderObject(self, dinY):
        f = open('try.txt', 'r')
        if dinY > self.y+9:
            self.y = dinY-9
        elif dinY < self.y:
            self.y = dinY

        self.j = self.y
        for i in f:
            print('\033['+ str(self.j) +';' + str(self.x)+'H '+str(i))
            self.j += 1
        f.close()

class cloudObject(bgObject):
    def __init__(self):
        super().__init__()
        self.x = terminalSize()[0]-11
        self.y = np.random.choice(range(3,8))
    def moveAcross(self):
        if self.x > 5:
            self.x -= 1
        else:
            self.x = -1

    def renderObject(self):
        f = open('cloud.txt', 'r')
        self.moveAcross()
        self.j = self.y

        for i in f:
            print('\033['+ str(self.j) +';' + str(self.x)+'H '+str(i))
            self.j += 1
        f.close()


class charObject:
    def __init__(self):
        self.y = terminalSize()[1]-2
        self.x = 7

    def renderObject(self):
        print('\033['+str(self.y)+';'+str(self.x)+'H '+str(self.x)+str(self.y)+' '+str(terminalSize()[1]))



class dinObject(charObject):
    def __init__(self):
        self.speedBoost = 0
        self.shield = 0
        self.magAttract = 0
        super().__init__()

    def gravity(self, val):#, gravCount):
        if val != 'w' and self.y < terminalSize()[1]-2: #and gravCount==1:
            self.y += 1
        #gravCount= not(gravCount)
        return self.y#, gravCount

    def getXY(self):
        return self.x, self.y

    def magForce(self, flagVal, magX):
        if flagVal==1:
            if self.x>magX:
                self.x-=1

            elif self.x<magX:
                self.x+=1


    def moveDin(self, speedVal, magnetFlag, magX):
        if self.speedBoost == 0:
            if (speedVal == 'w') and self.y > 3:
                self.y -= 1
            elif (speedVal == 'a' and self.x > 0):
                self.x -= 1
            elif (speedVal == 'd' and self.x < terminalSize()[0]):
                self.x += 1
            else:
                self.magForce(magnetFlag, magX)
            self.gravity(speedVal)

        else:
            if (speedVal == 'w') and self.y > 3:
                self.y -= 2
            elif (speedVal == 'a' and self.x > 0):
                self.x -= 2
            elif (speedVal == 'd' and self.x < terminalSize()[0]):
                self.x += 2
            else:
                self.magForce(magnetFlag, magX)
            self.gravity(speedVal)


    



class flyingObject():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def moveAcross(self):

        if self.x < terminalSize()[0] and self.x != -1:
            self.x += 2
        else:
            self.x = -1

    def getXY(self):
        return self.x, self.y

    def renderObject(self):
        self.moveAcross()
        if self.x != -1:
            print('\033[' + str(self.y) +';' + str(self.x) + 'H >')

class enBulletObject(flyingObject):



    def moveAcross(self):

        if self.x < terminalSize()[0] and self.x != -1:
            self.x -= 2
        else:
            self.x = -1

    def renderObject(self):
        self.moveAcross()
        if self.x != -1:
            print('\033[' + str(self.y) +';' + str(self.x) + 'H <')




class bgBeams(bgObject):

    def __init__(self):
        self.sizeSide = 2

        super().__init__()

class vertBeam(bgBeams):
    def __init__(self):
        self.y = np.random.randint(5, terminalSize()[1]-3)
        super().__init__()


    def moveAcross(self):
        if self.x > 0:
            self.x -= 1
        else:
            self.x = -1


    def renderObject(self):
        self.moveAcross()

        if self.x != -1:
            self.j = self.y-2
            for i in range(5):
                print('\033['+ str(self.j) +';' + str(self.x) + 'H 0')
                self.j += 1


class horiBeam(bgBeams):
    def __init__(self):
        self.y = np.random.randint(5, terminalSize()[1]-3)
        super().__init__()


    def moveAcross(self):
        if self.x > 5:
            self.x -= 1
        else:
            self.x = -1


    def renderObject(self):
        self.moveAcross()

        if self.x != -1:
            self.j = self.x-8
            for i in range(5):
                print('\033['+ str(self.y) +';' + str(self.j) + 'H 0')
                self.j += 2

class diagBeam(bgBeams):
    def __init__(self):
        self.y = np.random.randint(5, terminalSize()[1]-3)
        super().__init__()

    def moveAcross(self):
        if self.x > 5:
            self.x -= 1
        else:
            self.x = -1

class diagLeftBeam(diagBeam):
    def __init__(self):
        super().__init__()

    def renderObject(self):
        self.moveAcross()

        if self.x != -1:
            self.j = self.x-8
            self.k = self.y-2
            for i in range(5):
                print('\033['+ str(self.k) +';' + str(self.j) + 'H 0')
                self.j += 2
                self.k += 1

class diagRightBeam(diagBeam):
    def __init__(self):
        super().__init__()

    def renderObject(self):
        self.moveAcross()

        if self.x != -1:
            self.j = self.x-8
            self.k = self.y-2
            for i in range(5):
                print('\033['+ str(self.k) +';' + str(self.j) + 'H 0')
                self.j -= 2
                self.k += 1



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
    timeLeft = 20
    score = 0
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
        time.sleep(0.02)
        timeLeft -= 0.2
        background(score, timeLeft)
        

        if timeLeft <= 0:
            break



        elif timeLeft <= 10:
            DinY=Din.getXY()[1]
            dragon.renderObject(DinY)
            if timeLeft%1 <= 0.001:
                enBullet=enBulletObject(terminalSize()[0]-11,DinY, )
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

            

            if (timeLeft <= magTime and magnet == None):
                magnet = magnetObject()
                magnetFlag=1

            elif magnet != None and magnet.getXY()[0] > -1:
                magnet.renderObject()
        
            else:
                magnetFlag=0
            
            prob = np.random.random_sample()
            if(prob >= 0.99):
                cloud = cloudObject()
                cloudList.append(cloud)
            

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
            
            for i in range(len(coinList)):
                coinList[i].renderObject()

            for i in range(len(bulletList)):
                bulletList[i].renderObject()

            for i in range(len(vertBeamList)):
                vertBeamList[i].renderObject()

            for i in range(len(horiBeamList)):
                horiBeamList[i].renderObject()

            for i in range(len(leftBeamList)):
                leftBeamList[i].renderObject()
            
            for i in range(len(rightBeamList)):
                rightBeamList[i].renderObject()

            for i in range(len(cloudList)):
                cloudList[i].renderObject()

        
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