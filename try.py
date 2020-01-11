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

	def userInput(timeout=0.1):
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


def background(y, x):
		print (' '*terminalSize()[0])

		print ('-'*terminalSize()[0])


		for i in range(terminalSize()[1]-4):
			print(' '*terminalSize()[0])

		print ('-'*terminalSize()[0])




def gravity(y,val):
	if val!='w' and y<terminalSize()[1]-4:
		y+=1
	return y




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







def mainGame():
	y=terminalSize()[1]-3
	x=7
	coinList=[]
	while True:
			time.sleep(0.1)
			background(y,x)
			if (y<terminalSize()[1]-3):
				y=terminalSize()[1]-3
			print ('\033['+ str(y) +';' + str(x) + 'H ' + str(x)+str(y)+' '+str(terminalSize()[1]))
			
			#f = open("demofile.txt", "a")


			prob=np.random.uniform()
			


			if(prob>=0.9):
				coin=bgCoin()
				coinList.append(coin)
#			f.write("\n"+str(len(coinList))+"\n")

			for i in range(len(coinList)):
				coinList[i].renderObject()
#				f.write(str(coinList[i].getY())+"\n")
#			f.close()


			val=inputChar()

			if (val=='w' and y<terminalSize()[1]-1):
					y-=1
			elif (val=='a' and x>0):
					x-=1
			elif (val=='d' and x<terminalSize()[0]):
					x+=1
			elif (val=='c'):
				break
			y=gravity(y,val)
		
			

			


mainGame()



