from __future__ import print_function
import time, sys, signal
import numpy as np
import fcntl, termios, struct, os

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


def background():
		print (' '*terminalSize()[0])

		print ('-'*terminalSize()[0])


		for i in range(terminalSize()[1]-4):
			print(' '*terminalSize()[0])

		print ('-'*terminalSize()[0])









class bgObject:
	def __init__(self):
		self.y=np.random.randint(5,terminalSize()[1]-3)
		self.x=terminalSize()[0]-1

	def getXY(self):
		return self.x, self.y

	def moveAcross(self):
		if self.x>0:
			self.x-=1
		else:
			self.x=-1

class bgCoin(bgObject):
	def __init__(self):
		
		super().__init__()

	def renderObject(self):
		self.moveAcross()
		if self.x!=-1:
			print ('\033['+ str(self.y) +';' + str(self.x)+'H O')





class charObject:
	def __init__(self):
		self.y=terminalSize()[1]-3
		self.x=7		

	def renderObject(self):
		print ('\033['+ str(self.y) +';' + str(self.x) + 'H ' + str(self.x)+str(self.y)+' '+str(terminalSize()[1]))






class dinObject(charObject):
	def __init__(self):
		
		super().__init__()

	def gravity(self,val):#,gravCount):
		if val!='w' and self.y<terminalSize()[1]-2: #and gravCount==1:
			self.y+=1
		#gravCount= not(gravCount)
		return self.y#, gravCount

	def getXY(self):
		return self.x, self.y

	def moveDin(self, val):
		if (val=='w') and self.y>3:
					self.y-=1
		elif (val=='a' and self.x>0):
					self.x-=1
		elif (val=='d' and self.x<terminalSize()[0]):
					self.x+=1
		self.gravity(val)


class flyingObject():
	def __init__(self,x,y):
		self.x=x	
		self.y=y

	def moveAcross(self):
		if self.x<terminalSize()[0] and self.x!=-1:
			self.x+=2
		else:
			self.x= -1

	def getXY(self):
		return self.x, self.y

	def renderObject(self):
		self.moveAcross()
		if self.x!=-1:
			print ('\033['+ str(self.y) +';' + str(self.x) + 'H >')


def mainGame():
	
	gravCount=0
	coinList=[]
	bulletList=[]
	Din= dinObject()

	while True:
			time.sleep(0.02)
			background()
			
			Din.renderObject()

			prob=np.random.uniform()

			if(prob>=0.95):
				coin=bgCoin()
				coinList.append(coin)

			for i in range(len(coinList)):
				coinList[i].renderObject()
				

			for i in range(len(bulletList)):
				bulletList[i].renderObject()
				




			val=inputChar()

			
			if (val=='c'):
				break
			elif (val=='b'):
				x,y=Din.getXY()
				bullet=flyingObject(x,y)
				bulletList.append(bullet)
			
			else:
				Din.moveDin(val)
			
			

			


mainGame()



