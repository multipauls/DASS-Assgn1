import tty
import sys
import signal
import termios

class _getChUnix:
    ''' Class to get char input'''
    def __call__(self):

        fedvar = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fedvar)
        try:
            tty.setraw(sys.stdin.fileno())
            charvar = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fedvar, termios.TCSADRAIN, old_settings)
        return charvar

class AlarmException(Exception):
    ''' Class for alarm exceptions ''' 
    pass


def inputChar(timeout):
    ''' Function for input '''
    def alarmHandler(signum, frame):
        ''' Alarm handler for input '''
        raise AlarmException

    def userInput(timeout):
        ''' Function that takes and returns the input '''
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

    char = userInput(timeout)
    return char
