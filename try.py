from __future__ import print_function
import time, signal
import fcntl, termios, struct
import numpy as np

#copied here
class _getChUnix:
    '''class to take input'''

    def __init__(self):
        '''init def to take input'''
        import tty
        import sys

    def __call__(self):
        '''def to call function'''
        import sys
        import tty
        import termios
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
    print('\033[0;0H SCORE:'+str(score)+' TIME LEFT:'+str(timeLeft))
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
            print('\033['+ str(self.y) +';' + str(self.x)+'H O')





class charObject:
    def __init__(self):
        self.y = terminalSize()[1]-2
        self.x = 7        

    def renderObject(self):
        print('\033['+ str(self.y) +';' + str(self.x) + 'H ' + str(self.x)+str(self.y)+' '+str(terminalSize()[1]))






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

    def moveDin(self, val):
        if self.speedBoost == 0:
            if (val == 'w') and self.y > 3:
                self.y -= 1
            elif (val == 'a' and self.x > 0):
                self.x -= 1
            elif (val == 'd' and self.x < terminalSize()[0]):
                self.x += 1
            self.gravity(val)
         
        else:
            if (val == 'w') and self.y > 3:
                self.y -= 2
            elif (val == 'a' and self.x > 0):
                self.x -= 2
            elif (val == 'd' and self.x < terminalSize()[0]):
                self.x += 2
            self.gravity(val)




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
        self.y = np.random.randint(5,terminalSize()[1]-3)
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
    vertBeamList = []
    horiBeamList = []
    leftBeamList = []
    rightBeamList = []
    timeLeft = 120
    score = 0
    spBoost = None
    shieldBoost = None
    boostRandomiser = np.arange(0, 120, 0.2)
    spBoostTime = np.random.choice(boostRandomiser)
    spBoostEnd = spBoostTime-20
    shieldTime = np.random.choice(boostRandomiser)
    shieldEnd = shieldTime-20
    Din = dinObject()
    while True:
        time.sleep(0.02)
        timeLeft -= 0.2
        background(score, timeLeft)
        if timeLeft <= 0:
            break
        
        if (timeLeft <= spBoostTime and timeLeft >= spBoostEnd and spBoost == None):
            spBoost = speedBoost()
                
        if spBoost != None:
            spBoost.renderObject()

        if (timeLeft <= shieldTime and timeLeft >= shieldEnd and shield == None):
            shieldBoost = shield()
                
        if shieldBoost != None:
            shieldBoost.renderObject()


        Din.renderObject()

        prob = np.random.random_sample()

        if(prob >= 0.90):
            coin = bgCoin()
            coinList.append(coin)

        prob = np.random.random_sample()



        prob = np.random.random_sample()

        if(prob >= 0.95):
            beam=vertBeam()
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

        val=inputChar()

            
        if (val == 'q'):
            break
        elif (val == 'b'):
            x, y = Din.getXY()
            bullet = flyingObject(x, y)
            bulletList.append(bullet)
            
        else:
            Din.moveDin(val)
            
            

'''
    def magForce(self, flagVal, magX, magY):
        if flagVal==1:
            if self.y>magY && self.x>magX:
                self.y-=1
                self.x-=1

            elif self.y>magY && self.x<magX
                self.y-=1

        return 
''' 


mainGame()



