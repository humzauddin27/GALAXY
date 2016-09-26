################################# GALAXY #######################################
################### PROGRAM CREATED BY: HUMZA FAHEEMUDDIN ######################
###################### LAST MODIFIED: JANUARY 23 2014 ############################

from Tkinter import*
from time import*
from math import*
from random import*

root = Tk()
root.title("GALAXY BY HUMZA FAHEEMUDDIN")
screen = Canvas( root, width = 800, height = 800, background = "black")


#CURRENTLY GLITCHED: WHEN A LASER IS SHOT, AND THE SPACE BAR IS PRESSED AGAIN, THAT
#LASER THEN STOPS AND A NEW ONE IS CREATED. THE OLD LASER IS NOT DELETED. 

#------------------------------------------------------------------------------#

#Creates the screen that you see at the beginning
def menuScreen():
    global startGame, xText, yStartGame, runTheGame, gameRunning, title, startGame

    xText = 400
    yTitle = 150
    yStartGame = 500

    gameRunning = False
    runTheGame = False

    
    title = screen.create_text(xText,yTitle, text = "GALAXY", font = "fixedsys 40", fill = "white")
    startGame = screen.create_text(xText, yStartGame, text = "START GAME", font = "fixedsys 30", fill = "white")

#------------------------------------------------------------------------------#

#Sets all the initial values and variables
def setupTheProgram ():
    global ship, smallAsteroid, mediumAsteroid, largeAsteroid, missile, enemyOne, enemyTwo
    global xShip, yShip, points, livesLeft, sAsteroidHP, mAsteroidHP, lAsteroidHP, sAsteroidSpeed
    global mAsteroidSpeed, lAsteroidSpeed, numSmallAsteroids, numMedAsteroids, numLargeAsteroids
    global enemySpeed,destSpeed,userQuit,gameRunning, mouseDown, smallAsteroidDeath, smallAsteroidAlive, asteroidAlive, missileCreate
    global laser, shotFired, numLasers,laser, yLaserSpeed,xLaserSpeed,laserX, laserY, laserShot, enemyDestroyer,xLaser, yLaser, shipSpeed, enemyHP, destHP, fighterAlive, destroyerAlive, invulnerable
    
    #Imported images
    ship = PhotoImage(file = "ship.gif")
    enemyOne = PhotoImage(file = "enemy fighter.gif")
    enemyTwo = PhotoImage(file = "enemy destroyer.gif")

    spawn = 400
    
    #Ship starting position
    xShip = spawn
    yShip = spawn

    #Other setup
    points = 0
    livesLeft = 5

    #enemy setup
    enemySpeed = 5
    destSpeed = 8
    shipSpeed = 30
    enemyHP = 20 #20
    destHP = 30  #30

    #

    runTheGame = True    
    userQuit = False #True if user presses Q/q
    gameRunning = True #False if game over or if userQuit = True
    fighterAlive = True #True if the first enemy is alive
    destroyerAlive = False #False by default, therefore only one enemy at a time
    invulnerable = False 
    shotFired = False

    enemyDestroyer = enemyTwo

    #StarCreating
    drawStars( "white", 300, 3 )
    drawStars( "yellow", 300, 3  )
    drawStars( "red", 300, 3)
    drawStars( "green", 300, 3)

#------------------------------------------------------------------------------#

#Draws random stars that appear in the background
    
def drawStars( starColor, numStars, maxSize ):
    for i in range(0, numStars):
        x = randint(0,800)
        y = randint(0,800)
        size = randint(2,3)
        screen.create_oval(x, y, x+size, y+size, fill= starColor)
        screen.update()

#------------------------------------------------------------------------------#
    
def getDistance(x1, y1, x2, y2):
    return sqrt( (x2 - x1)**2 + (y2-y1)**2 )

#------------------------------------------------------------------------------#

def getKeyStroke( event ):
    global shotFired, xMissile, yMissile, moveUp, userQuit, gameRunning, moveLeft, moveRight, stop, xShip, yShip
    
    if event.keysym == "q" or event.keysym == "Q": #If the user presses Q/q, the game stops running
        userQuit = True
        gameRunning = False

    elif event.keysym == "Up": #moves the ship
        yShip = yShip - shipSpeed

            
    elif event.keysym == "Left": #moves the ship
        xShip = xShip - shipSpeed


    elif event.keysym == "Down": #moves the ship
        yShip = yShip + shipSpeed


    elif event.keysym == "Right": #moves the ship
        xShip = xShip + shipSpeed


    elif event.keysym == "space": #shoots a laser
        #updateLaserPositions()
        shotFired = True
        updateLaserPositions()



#------------------------------------------------------------------------------#

def stopGame():

    if userQuit == True: #If the user presses Q/q
        gameOverMessage = "You just quit the game! Goodbye!" 
        
        screen.create_text( 400, 400, text = gameOverMessage, font = "fixedsys 30", anchor=CENTER, fill = "white" )
    screen.update()
    
    sleep(2)
    
    root.destroy() 

#------------------------------------------------------------------------------#

#Checks the position of the ship. If the ship is about to leave the screen, it
#resets the position so that it hits a "wall".
    
def checkPos():
    global yShip, xShip

    if yShip >= 775:
        yShip = 775
    if yShip <= 50:
        yShip = 50
    if xShip >= 775:
        xShip = 775
    if xShip <= 50:
        xShip = 50

#------------------------------------------------------------------------------#


#Helps with the clicking. Essentially is my runGame() Program, and it runs
#once the user clicks between the specified coordinates.

def mouseClickDetector(event):
    global runTheGame, gameRunning

    print ( "Mouse clicked at " + str( event.x ) + "," + str(event.y ))

    xMouse = event.x
    yMouse = event.y
    
    if event.x > 285 and event.x < 500:
        
        if event.y < 520 and event.y > 480:
            
            runTheGame = True
            gameRunning = True
            setupTheProgram()
            enemyPlacer()
            updateLaserPositions()
            screen.delete(title, startGame)

            sleep(2)

        while gameRunning == True:

                drawShip()
                whosAlive()
                updateEnemyShips()

                scoreKeeping()
                life()

                checkPos()
                checkHP()
                invulnerableCheck()
                
                if shotFired == True:
                    drawLasers()
                    updateLaserY()
                    
                 ## try deleting lasers   
                distanceChecker()
                winCheck()
                
                screen.update()
                sleep(0.001)
                
                deleteImages()


                if gameRunning == False:
                    if userQuit == True:
                        stopGame()
                    
                    else:
                        sleep(2)
                        root.destroy()

        

#------------------------------------------------------------------------------#

#Draws the ship in its current position.

def drawShip():
    global shipImage
    shipImage = screen.create_image(xShip, yShip, image = ship)

#------------------------------------------------------------------------------#
#Sets the X and Y coordinates for the two enemies. Gives them both random X values
    
def enemyPlacer():
    global xEnemy, yEnemy, xDest, yDest
    xEnemy = randint (0,800)
    yEnemy = 0
    xDest = randint (0,800)
    yDest = 0

#------------------------------------------------------------------------------#

#Draws the first enemy in its current position
def drawEnemyShip():
    global enemyFighter
    enemyFighter = screen.create_image(xEnemy, yEnemy, image = enemyOne)

#------------------------------------------------------------------------------#

#Draws the second enemy in its current position, but only runs if destroyerAlive == False
def drawEnemyShipTwo():
    global enemyDestroyer
    enemyDestroyer = screen.create_image(xDest, yDest, image = enemyTwo)

#------------------------------------------------------------------------------#

#Helps the ship moves towards you as they try to attack. 
def updateEnemyShips():
    global xEnemy, yEnemy, xDest, yDest
    
    xEnemyDir = xShip - xEnemy
    yEnemyDir = yShip - yEnemy

    xDestDir = xShip - xDest
    yDestDir = yShip - yDest

    enemyDistFromShip = getDistance (xShip, yShip, xEnemy, yEnemy)
    destDistFromShip = getDistance (xShip, yShip, xDest, yDest)
    
    xEnemySpeed = enemySpeed * xEnemyDir / enemyDistFromShip
    yEnemySpeed = enemySpeed * yEnemyDir / enemyDistFromShip

    xDestSpeed = destSpeed * xDestDir / destDistFromShip 
    yDestSpeed = destSpeed * yDestDir / destDistFromShip 

    xEnemy = xEnemy + xEnemySpeed #updates the fighters speeds
    yEnemy = yEnemy + yEnemySpeed

    if destroyerAlive == True: #This is so that the second enemy doesn't start attacking you beforehand

        xDest = xDest + xDestSpeed #updates the destroyers speeds
        yDest = yDest + yDestSpeed 
        

    if fighterAlive == False: #So that when the first enemy dies, he disappears off screen.
        xEnemy = -100
        yEnemy = 0


#------------------------------------------------------------------------------#

def updateLaserPositions():
    global laser, i, xLaser, yLaser, xLaserSpeed, yLaserSpeed, laserX, laserY, xSpeedLaser, ySpeedLaser, xShip, yShip
    #empty arrays for coordinates of the lasers to be added to
    
    xLaser = []
    yLaser = []
    xLaserSpeed = []
    yLaserSpeed = []
    laserX = None
    laserY = None
    laser = [1]

    for i in range(0,len(laser)):    

        laserX = xShip
        laserY = yShip
        xSpeedLaser = 0
        ySpeedLaser = 20

        #appending the coordinates
        xLaser.append(laserX)
        yLaser.append(laserY)
        xLaserSpeed.append(xSpeedLaser)
        yLaserSpeed.append(ySpeedLaser)
        laser.append(0)


#------------------------------------------------------------------------------#
      
#Updates the Y position of the laser so that it goes up.
def updateLaserY():
    global yLaser

    yLaser[i] = yLaser[i] - yLaserSpeed[i]

#------------------------------------------------------------------------------#

#Draws the lasers
def drawLasers():
    global laser
    laser[i] = screen.create_line(xLaser[i], yLaser[i], xLaser[i], yLaser[i]-20, fill = "red", width = 3)
#------------------------------------------------------------------------------#

#Checks the distance between enemies and lasers. Also awards points on hit/kill,
#and triggers the explosion() procedure.

def distanceChecker():
    global enemyHP, points, destHP, fighterAlive, destroyerAlive

    if getDistance (xEnemy, yEnemy, xLaser[i], yLaser[i]) <= 20:
        enemyHP = enemyHP - 1 #subtracts HP
        points = points + 10 #gives points
        print ("You hit the fighter!")
        print ("Fighter HP is now: " + str(enemyHP))
        screen.delete(enemyFighter) #makes the picture blink
        

        if enemyHP == 0:
            points = points + 1000 #gives large amount of points after succeeding to kill
            print ("You killed a fighter!")
            explosion() #triggers explosion
            fighterAlive = False
            destroyerAlive = True #sends second enemy

    #same as above
    
    if getDistance (xDest, yDest, xLaser[i], yLaser[i]) <= 15:
        destHP = destHP - 1
        points = points + 20
        print ("You hit the Destroyer!")
        print ("Dest HP is now: " + str(destHP))
        screen.delete(enemyDestroyer)

        if destHP == 0:
            points = points + 10000
            print ("You killed a destroyer!")
            otherExplosion()
            destroyerAlive = False

#------------------------------------------------------------------------------#

#Explosion for the first enemy's death.
            
def explosion():
    numFrames = 25

    numBoxes = 200

    size = []
    x = []
    y = []
    xSpeed = []
    ySpeed = []
    box = []
    colours = ["green", "yellow", "red"]

    for i in range(0,numBoxes):
        newSize = randint(5,10)
        newXspeed = randint(-8,8)
        newYspeed = randint(-8,8)

        size.append( newSize )
        
        x.append( xEnemy )
        y.append( yEnemy )
            
        xSpeed.append( newXspeed )
        ySpeed.append( newYspeed )
        box.append ( 0 )
        

    for frameCount in range( 1, numFrames + 1 ):
        
        for i in range(0,numBoxes):
            x[i] = x[i] + xSpeed[i]
            y[i] = y[i] + ySpeed[i]
            box[i] = screen.create_rectangle( x[i], y[i], x[i] +size[i], y[i] +size[i], fill=colours[i%3])

        screen.update()  
        sleep(0.05)  

        for i in range(0,numBoxes):
            screen.delete( box[i] )

#------------------------------------------------------------------------------#

#Explosion for the second enemy's death.
            
def otherExplosion():
    numFrames = 25

    numBoxes = 200

    size = []
    x = []
    y = []
    xSpeed = []
    ySpeed = []
    box = []
    colours = ["blue", "purple", "red"]

    for i in range(0,numBoxes):
        newSize = randint(5,10)
        newXspeed = randint(-8,8)
        newYspeed = randint(-8,8)

        size.append( newSize )
        x.append( xDest )
        y.append( yDest )
        xSpeed.append( newXspeed )
        ySpeed.append( newYspeed )
        box.append ( 0 )
        

    for frameCount in range( 1, numFrames + 1 ):
        
        for i in range(0,numBoxes):
            x[i] = x[i] + xSpeed[i]
            y[i] = y[i] + ySpeed[i]
            box[i] = screen.create_rectangle( x[i], y[i], x[i] +size[i], y[i] +size[i], fill=colours[i%3])

        screen.update()  
        sleep(0.05)  

        for i in range(0,numBoxes):
            screen.delete( box[i] )

#------------------------------------------------------------------------------#

#Explosion for when the user dies.
            
def oneLastExplosion():

    numFrames = 25
    numBoxes = 200

    size = []
    x = []
    y = []
    xSpeed = []
    ySpeed = []
    box = []
    colours = ["white", "red"]

    for i in range(0,numBoxes):
        newSize = randint(5,10)
        newXspeed = randint(-8,8)
        newYspeed = randint(-8,8)

        size.append( newSize )
        x.append( xShip )
        y.append( yShip )
        xSpeed.append( newXspeed )
        ySpeed.append( newYspeed )
        box.append ( 0 )
        

    for frameCount in range( 1, numFrames + 1 ):
        
        for i in range(0,numBoxes):
            x[i] = x[i] + xSpeed[i]
            y[i] = y[i] + ySpeed[i]
            box[i] = screen.create_rectangle( x[i], y[i], x[i] +size[i], y[i] +size[i], fill=colours[i%2])

        screen.update()  
        sleep(0.05)  

        for i in range(0,numBoxes):
            screen.delete( box[i] )

#------------------------------------------------------------------------------#
            
#Checks to see whos alive, if one is True the other is False. This avoids two
#enemies at once.
            
def whosAlive():
    global fighterAlive, destroyerAlive
    
    if fighterAlive == True:
        destroyerAlive = False
        drawEnemyShip()

    if fighterAlive == False:
        screen.delete(enemyFighter)
        destroyerAlive = True
        drawEnemyShipTwo()
#------------------------------------------------------------------------------#
        
#Checks to see whether you have won or not. When you do, it prints a congratulations
#message and provides extra points based on lives. Also deletes all the images.        

def winCheck():
    global gameRunning, points
    
    if fighterAlive == False and destroyerAlive == False:
        points = points + (livesLeft*1000)
        screen.create_text(400,400, text = "You beat the enemies with " + str(livesLeft) + " lives remaining!", font = "fixedsys 20", fill = "white")
        screen.create_text(400,600, text = "Your final score is: " + str(points), font = "fixedsys 20", fill = "white")
        screen.delete(enemyDestroyer, shipImage, laser[i])
        gameRunning = False
        
            
#------------------------------------------------------------------------------#
#Checks to see if you are within range of the enemy ships. If so, it triggers
#the user explosion procedure. It also subtracts a life from you, and allows
#you to respawn safely.
        
def checkHP():
    global livesLeft, invulnerable

    #for when the first enemy is alive
    if getDistance (xShip, yShip, xEnemy, yEnemy) <= 15:
        livesLeft = livesLeft - 1
        print ("you lost a life")
        oneLastExplosion()
        invulnerable = True
        
    #for when the second enemy is alive
    if getDistance (xShip, yShip, xDest, yDest) <= 15:
        livesLeft = livesLeft - 1
        print ("you lost a life")
        oneLastExplosion()
        invulnerable = True

#------------------------------------------------------------------------------#

#If you do die, this is set to True. It resets your position and then sets
#invulnerable to False after the respawn.

def invulnerableCheck():
    global xShip, yShip, xDest, yDest, xEnemy, yEnemy, invulnerable, wellmaybenot, uknowwhatitis
    
    if invulnerable == True and destroyerAlive == True:
        xShip = 400
        yShip = 750
        xDest = 400
        yDest = 0
        sleep (1)
        invulnerable = False
        
    elif invulnerable == True and fighterAlive == True:
        xShip = 400
        yShip = 750
        xEnemy = 400
        yEnemy = 0
        sleep (1)
        invulnerable = False

#------------------------------------------------------------------------------#
#If you lose all your lives, quits the game automatically.
        
def life():
    global livesLeft, gameRunning
    ggMessage = "You ran out of lives...GG!"

    if livesLeft <= 0:
        screen.create_text(400, 400, text = ggMessage, fill = "white", font = "fixedsys 30")
        sleep (0.01)
        gameRunning = False

#------------------------------------------------------------------------------#

#Deletes all the images on the screen. 
def deleteImages():
    global shotFired
    screen.delete(laser[i], enemyOneHP, realPoints, shipImage, enemyFighter, realLives) #removed enemyDestroyer

    if destroyerAlive == True:
        screen.delete(enemyDestroyer)

    for x in range(0, len(laser)):
        screen.delete(laser[x])
        
#------------------------------------------------------------------------------#

#Prints the current amount of points and the amount of lives you have on screen.
def scoreKeeping():
    global realPoints, realLives, enemyOneHP

    #always shows points and amount of lives that the user has
    pts = str(points)
    realPoints = screen.create_text(675,785, text = pts, fill = "white", font = "fixedsys 30")
    lifes = "Lives: " + str(livesLeft)
    realLives = screen.create_text(125, 785, text = lifes, fill = "white", font = "fixedsys 30")

    #If the first enemy is alive, it shows its HP and if the second is alive, then it shows the second enemy's HP.
    if fighterAlive == True:
        fighterLives = "Enemy HP is: " + str(enemyHP)
        enemyOneHP = screen.create_text(200, 50, text = fighterLives, fill = "white", font = "fixedsys 30")
    elif destroyerAlive == True:
        destroyerLives = "Enemy HP is: " + str(destHP)
        enemyOneHP = screen.create_text(200, 50, text = destroyerLives, fill = "white", font = "fixedsys 30")

#------------------------------------------------------------------------------#

#Runs the menuScreen() procedure (which is essentially the real runGame(), which eventually triggers all the other procedures and functions.
def runGame():

    menuScreen()
    
#------------------------------------------------------------------------------#
    
root.after(1000, runGame)
screen.bind("<Button-1>", mouseClickDetector )
screen.bind("<Key>", getKeyStroke)

screen.pack()
screen.focus_set()

root.mainloop()

#------------------------------------------------------------------------------#
