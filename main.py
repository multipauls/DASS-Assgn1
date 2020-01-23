from __future__ import print_function
import time
import numpy as np
from termSize import terminalSize
from endgame import endGame
from bg import background
from objects import *
from inputChar import inputChar


exitCode = -1
score = 0
def mainGame():
    ''' The game loop '''
    global exitCode
    global score
    timeHere = time.time() 
    coinList = []
    bulletList = []
    enBulletList = []
    vertBeamList = []
    horiBeamList = []
    leftBeamList = []
    rightBeamList = []
    cloudList = []
    timeLeft = 120
    timeEnd = timeHere + 120
    life = 100
    spBoost = None
    shieldBoost = None
    magnet = None
    speedFlag = 0
    magnetFlag = 0
    boostRandomiser = np.arange(25, 120, 1)
    spBoostTime = np.random.choice(boostRandomiser)
    magTime = np.random.choice(boostRandomiser)
    shieldEnd = 0
    shieldRecharge = 0
    Din = dinObject()
    dragon = dragonObject()
    dragonLife = 100
    while True:
        if speedFlag == 1:
            time.sleep(0.01)
            timeLeft = timeEnd - time.time()
        else:
            time.sleep(0.02)
            timeLeft = timeEnd - time.time()


        DinPos = Din.getCoords()
        dragonPos = dragon.getCoords()
        background(score, timeLeft, life, dragonLife)
        
        for i in range(len(cloudList)):
            cloudList[i].renderObject()

        for i in range(len(coinList)):
            coinList[i].renderObject()
            coinPos = coinList[i].getCoords()
            if DinPos[0] == coinPos or DinPos[1] == coinPos:
                coinList[i].changeX()
                score += 20

        for i in range(len(vertBeamList)):
            vertBeamList[i].renderObject()
            vertPos = vertBeamList[i].getCoords()
            for j in range(len(vertPos)):
                if DinPos[0] == vertPos[j] or DinPos[1] == vertPos[j]:
                    vertBeamList[i].changeX()
                    if not(Din.getShield()):
                        life -= 2                    
                    break
                for k in range(len(bulletList)):
                    bulletPos = bulletList[k].getCoords()
                    if bulletPos == vertPos[j]:
                        bulletList[k].changeX()
                        vertBeamList[i].changeX()
                        break
                    
        for i in range(len(horiBeamList)):
            horiBeamList[i].renderObject()
            horiPos = horiBeamList[i].getCoords()
            for j in range(len(horiPos)):
                if DinPos[0] == horiPos[j] or DinPos[1] == horiPos[j]:
                    horiBeamList[i].changeX()
                    if not(Din.getShield()):
                        life -= 2
                    break
                for k in range(len(bulletList)):
                    bulletPos = bulletList[k].getCoords()
                    if bulletPos == horiPos[j]:
                        bulletList[k].changeX()
                        horiBeamList[i].changeX()
                        break

        for i in range(len(leftBeamList)):
            leftBeamList[i].renderObject()
            leftPos = leftBeamList[i].getCoords()
            for j in range(len(leftPos)):
                if DinPos[0] == leftPos[j] or DinPos[1] == leftPos[j]:
                    leftBeamList[i].changeX()
                    if not(Din.getShield()):
                        life -= 2
                    break
                for k in range(len(bulletList)):
                    bulletPos = bulletList[k].getCoords()
                    if bulletPos == leftPos[j]:
                        bulletList[k].changeX()
                        leftBeamList[i].changeX()
                        break

        for i in range(len(rightBeamList)):
            rightBeamList[i].renderObject()
            rightPos = rightBeamList[i].getCoords()
            for j in range(len(rightPos)):
                if DinPos[0] == rightPos[j] or DinPos[1] == rightPos[j]:
                    rightBeamList[i].changeX()
                    if not(Din.getShield()):
                        life -= 2
                    break
                for k in range(len(bulletList)):
                    bulletPos = bulletList[k].getCoords()
                    if bulletPos == rightPos[j]:
                        bulletList[k].changeX()
                        rightBeamList[i].changeX()
                        break

        for i in range(len(bulletList)):
            bulletList[i].renderObject()
            bulletPos = bulletList[i].getCoords()
            for j in range(len(dragonPos)):
                if bulletPos == dragonPos[j]:
                    bulletList[i].changeX()
                    dragonLife -= 10
                    score += 30
                    break

        if (life <= 0):
            exitCode = 2
            break

        if (dragonLife <= 0):
            exitCode = 1
            break

        if (timeLeft <= magTime and magnet == None):
            magnet = magnetObject()
            magnetFlag = 1

        elif magnet != None and magnet.getXY()[0] != None and magnet.getXY()[0] > 0:
            magnet.renderObject()

        else:
            magnetFlag = 0


        if timeLeft <= 0:
            exitCode = 2
            break

        elif timeLeft <= 20:
            DinY = Din.getXY()[1]
            dragon.renderObject(DinY)
            if timeLeft%1 <= 0.2:
                enBullet = enBulletObject(terminalSize()[0]-11, DinY)
                enBulletList.append(enBullet)
            for i in range(len(enBulletList)):
                enBulletList[i].renderObject()
                enBulletPos = enBulletList[i].getCoords()
                for j in range(len(enBulletPos)):
                    if DinPos[0] == enBulletPos[j] or DinPos[1] == enBulletPos[j]:
                        enBulletList[i].changeX()
                        if not(Din.getShield()):
                            life -= 20
                        break

        else:    
            if (timeLeft <= spBoostTime and spBoost == None):
                spBoost = speedBoost()

            elif spBoost != None and spBoost.getXY()[0] != None and spBoost.getXY()[0] > 0:
                spBoost.renderObject()
                spPos = spBoost.getCoords()
                if spPos == DinPos[0] or spPos == DinPos[1]:
                    speedFlag = 1
                    spBoost.changeX()
            

            
            prob = np.random.random_sample()
            if(prob >= 0.99):
                cloud = cloudObject()
                cloudList.append(cloud)
            

            prob = np.random.random_sample()
            if(prob >= 0.90):
                coin = bgCoin()
                coinList.append(coin)

            prob = np.random.random_sample()
            if(prob >= 0.99):
                beam = vertBeam()
                vertBeamList.append(beam)

            prob = np.random.random_sample()
            if(prob >= 0.99):
                beam = horiBeam()
                horiBeamList.append(beam)

            prob = np.random.random_sample()
            if(prob >= 0.99):
                beam = diagLeftBeam()
                leftBeamList.append(beam)

            prob = np.random.random_sample()
            if(prob >= 0.99):
                beam = diagRightBeam()
                rightBeamList.append(beam)
            
        if (time.time() >= shieldEnd and Din.getShield() == 1):
            Din.shieldDown()
            shieldRecharge = time.time() + 60
        Din.renderObject()
        if speedFlag == 1:
            val = inputChar(0.05)
        else:
            val =  inputChar(0.1)
        if (val == ' ' and time.time() > shieldRecharge):
            Din.shieldUp()
            shieldEnd = time.time() + 10
        if (val == 'q'):
            break
        elif (val == 'b'):
            x, y = Din.getXY()
            bullet = flyingObject(x, y)
            bulletList.append(bullet)
        elif magnetFlag == 1:
            Din.moveDin(val, magnetFlag, magnet.getXY()[0])
        else:
            Din.moveDin(val, magnetFlag, 0)

mainGame()
endGame(exitCode, score)