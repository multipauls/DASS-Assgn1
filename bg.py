from __future__ import print_function
from termSize import terminalSize

def background(score, timeLeft, life, dragonLife):
  #  print('\u001b[48;5;232m \033[0;0H')
    print(' '*terminalSize()[0])
    print('\u001b[48;5;232m\u001b[38;5;15m' + '-'*terminalSize()[0] + '\u001b[0m')
    for i in range(terminalSize()[1]-2):
        print('\u001b[48;5;232m' + ' '*terminalSize()[0] + '\u001b[0m')
        #print ('\u001b[48;5;232m'+ ' '*terminalSize()[0])
    print('\u001b[48;5;232m\u001b[38;5;70m' + '-'*(terminalSize()[0]-2) + '\u001b[0m')
    print('\u001b[48;5;232m' + ' '*(terminalSize()[0]-1) + '\u001b[0m')
    print('\u001b[48;5;232m \u001b[38;5;15m \033[0;1H SCORE:'+str(score)+' LIFE:'+ str(life)+ ' ENEMY:'+ str(dragonLife) +' TIME LEFT:'+str(timeLeft)+ '\u001b[0m')


