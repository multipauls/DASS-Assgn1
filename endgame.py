from __future__ import print_function
from termSize import terminalSize
def endGame(exitCode, score):
    '''Prints for exiting game'''
    print(' '*terminalSize()[0]*terminalSize()[1])
    if exitCode == 1:
        print('\u001b[48;5;232m \u001b[38;5;15m \033[0;1H YOU WON. YOUR SCORE IS '+str(score)+' \u001b[0m')
    elif exitCode == 2:
        print('\u001b[48;5;232m \u001b[38;5;15m \033[0;1H YOU LOST. YOUR SCORE IS '+str(score)+' \u001b[0m')
    else:
        print('\u001b[48;5;232m \u001b[38;5;15m \033[0;1H ERROR. EXITED GAME. \u001b[0m')
