def terminalSize():

    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h



class bgObject:
    def __init__(self):
        self.y = 4
        self.x = terminalSize()[0]-1

    def getXY(self):
        return self.x, self.y


class dragonObject(bgObject):
    def renderObject(self):
        f=open('try.txt', 'r')
        for i in f:
            print('\033['+ str(self.y) +';' + str(self.x)+'H '+str(i))


