import time, sys
import numpy as np
import fcntl, termios, struct

def terminal_size():
	
	h, w, hp, wp = struct.unpack('HHHH',
		fcntl.ioctl(0, termios.TIOCGWINSZ,
		struct.pack('HHHH', 0, 0, 0, 0)))
	return w, h


def keypress(*argv):
	for a in argv:
		return a
	return 0
	
def background_screen():
	try:
		for i in range(0, 100):
			time.sleep(0.1)
			
			print ('-'*terminal_size()[0])
			for i in range(terminal_size()[1]-3):
				print(' '*terminal_size()[0])

			print ('-'*terminal_size()[0])
			n=3
			m=7
			print('\u001b['+ str(n) +'A ') 
			print('\u001b['+ str(m) + 'C ' + 'O' )
	except:
		
background_screen()




def loading():
	print ("Loading...")
	for i in range(0, 100):
		time.sleep(0.1)
		sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")
		sys.stdout.flush()
	print()
