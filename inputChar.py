import tty
import sys
import signal
import fcntl
import termios
import struct

class _getChUnix:

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
    pass


def inputChar(timeout):
    def alarmHandler(signum, frame):
        raise AlarmException

    def userInput(timeout):
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
