# This is my awesome (non-violent) hang person game

from turtle import *
from random import randint
import time
import math

wordList = ['aberration','abnegation', 'abrogate', \
            'adumbrate', 'anachronistic', 'approbation',\
            'aspersion', 'blandishment', 'defenistrate', \
            'enucleation', 'xylophoage', 'pusillanimous', \
              'fatuous', 'legerdemain', 'maelstrom', 'maudlin', \
            'mendacious', 'partisan', 'predilection', 'trenchant',\
             "St.Mark's School", "New England Patriots" \
            "Let's Snag This Sourdough", "Bag This Baguette" ]


#print(len(wordList))

sw = 800
sh = 800
#sw = 200
#sh = 300
sSide = sw
if sh < sw:
    sSide = sh

s=getscreen()
s.setup(sw, sh)
s.bgcolor('#20f9f9')
t1=getturtle()
t1.speed(0)
t1.hideturtle()
lineW = int(sSide*0.01)
if lineW < 2:
    lineW = 2
t1.width(lineW)
hLeg = int(math.hypot((sw/2), (sh*0.5)))
lAngle = int(math.degrees(math.asin( (sw/2)/hLeg))) #leg angle from bot centerline in deg.
#print("lAngle is {}".format(lAngle))
hArm = int(math.hypot((sw/2), (sh*0.4) )) 
aAngle = int(math.degrees(math.acos( (sw/2)/hArm))) #leg angle from bot centerline in deg.
#print("aAngle is {}".format(aAngle))
RIGHT = True
LEFT = False
nooseX = 0
nooseY = 0
headR = 0

#we need to make another turtle 
tWriter = Turtle()  
tWriter.hideturtle()
#tWriter.shape('turtle')

#Let's Make One for Wrong Letters, too
tBadLetters = Turtle()
tBadLetters.hideturtle()

# variables to play the game -- Global Variables
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
lettersWrong =""  #starting as empty strings
lettersCorrect = ""
secretWord=""
displayWord= ""
fails = 6  #how many wrong guesses you have left
fontS = int(sh*0.05)
gameDone = False


def pickSecretWord():
    global secretWord, wordList
    secretWord = wordList[randint(0, len(wordList)-1 )]
    print("The secret word is " + secretWord)


#new and improved to write all texts in one function
def displayText(newText):
    tWriter.clear()
    tWriter.penup()
    tWriter.goto(-int(sw*0.40), -int(sh*0.40) )
    tWriter.write( newText, font=("Arial", fontS, "bold") )

def displayBadLetters(newText):
    tBadLetters.clear()
    tBadLetters.penup()
    tBadLetters.goto(-int(sw*0.40), int(sh*0.36) )
    tBadLetters.write( newText, font=("Arial", fontS, "bold") )

def makeWordString():
    global displayWord, alpha
    displayWord = ""
    for l in secretWord:
        if str(l) in alpha:
            if str(l).lower() in lettersCorrect.lower():
                displayWord += str(l) + " "
            else:
                displayWord += "_" + " "
        else:
            displayWord += str(l) + " "
            
def getGuess():
    boxTitle="Letters Used: " + lettersWrong
    guess = s.textinput(boxTitle, "Enter a Guess type $$ to Guess the word" )
    return guess

def updateHangman():
    global fails
    if fails == 5:
        drawHead()
        drawFace()
    if fails == 4:
        drawTorso()
    if fails == 3:
        drawLeg(LEFT)
        #drawLeftLeg()  -- either way is fine
    if fails == 2:
        drawLeg(RIGHT)
        #drawRightLeg()  -- either way is fine
    if fails == 1:
        drawArm(LEFT)
        #drawLeftArm()
    if fails == 0:
        drawArm(RIGHT)
        #drawRightArm()

        
def checkWordGuess():   #NEW#####
    global fails, gameDone
    boxTitle="Word Guess"
    guess = s.textinput(boxTitle, "Ok Awesome...Guess the word" )
    if guess == secretWord:
        # if people are correct
        displayText("YES!!! the word is " + secretWord)
        gameDone = True
    else:
        displayText("No the word is not: " + guess)
        time.sleep(1)
        displayText(displayWord)
        fails -=1
        updateHangman()
        
def restartGame():
    global fails, lettersCorrect, lettersWrong, gameDone
    boxTitle="Want to play again"
    guess = s.textinput(boxTitle, 'Type "Y" or "Yes" to play again!' )

    if guess.lower()=='y' or guess.lower() == 'yes':
        lettersCorrect = ""
        lettersWrong = ""
        t1.clear()
        drawGallows()
        pickSecretWord()
        displayText("Guess a Letter..")
        displayBadLetters("Not in word: [" + lettersWrong + "]")
        time.sleep(1)
        makeWordString()
        displayText(displayWord)
        fails = 6
        gameDone = False
    else:
        displayBadLetters("Ok, see you later!")
        
def playGame():
    global gameDone, fails, alpha, lettersCorrect, lettersWrong
    while gameDone == False and fails > 0:
        # get input
        theGuess = getGuess()
        #you can also add this to get out of the loop
        #gameDone = True
        if theGuess == "$$":
            print("Let them guess word")
            checkWordGuess()  ######NEW
        elif len(theGuess) > 1 or theGuess =="":
                displayText("Sorry I need a letter, guess again.")
                time.sleep(1)
                displayText(displayWord)
        elif theGuess not in alpha:
                displayText(theGuess + " is not a letter, guess again.")
                time.sleep(1)
                displayText(displayWord)
        elif theGuess.lower() in secretWord.lower():
            lettersCorrect += theGuess.lower()
            makeWordString()
            displayText(displayWord)
        else:
            if theGuess.lower() not in lettersWrong:
                lettersWrong += theGuess.lower() +", "
                fails -= 1
                displayText(theGuess + " is not in the word")
                time.sleep(1)
                updateHangman()
                displayText(displayWord)
                displayBadLetters("Not in word: [" + lettersWrong + "]")
            else:
                displayText(theGuess + " was already guessed. Try again")
                time.sleep(1)
                displayText(displayWord)
        # end of loop tests    
        if "_" not in displayWord:
            displayText("YES!!! You Won-Word is: " + secretWord)
            gameDone = True
            
        if fails <= 0:
            displayText("Sorry Out of Guesses-Word is: " + secretWord)
            gameDone = True
            
        if gameDone == True:
            restartGame()
            

        
            
            
            

         


def drawGallows():
    global nooseX, nooseY

    t1.color('black')
    # draw base
    t1.penup()
    t1.setheading(0)
    t1.goto(-int(sw/6), -int(sh*0.3) )
    t1.pendown()
    t1.forward(int(sw*0.3))
    # draw main pole
    t1.penup()
    t1.backward(int(sw*0.10))
    t1.pendown()
    t1.left(90)
    t1.forward(int(sh*0.60))
    #draw top
    t1.left(90)
    t1.forward(int(sw*0.25))
    #draw hanger
    t1.left(90)
    t1.forward(int(sh*0.10))
    nooseX = t1.xcor()
    nooseY = t1.ycor()
    

def drawHead():
    global headR
    headR = int(sSide*0.08)
    t1.penup()
    t1.goto(t1.xcor()-headR, t1.ycor()-headR)
    t1.pendown()
    t1.circle(headR)
    t1.penup()
    t1.goto(t1.xcor()+headR, t1.ycor()-headR)
    
    
def drawTorso():
    t1.pendown()
    t1.forward(int(sh*0.15))

def drawLeg(whichL):
    #save turtle position
    tx = t1.xcor()
    ty = t1.ycor()
    t1.setheading(-90)
    if(whichL == RIGHT):
        t1.left(lAngle)
    else:
        t1.right(lAngle)
    t1.pendown()
    t1.forward(int(sh*0.15))
    t1.penup()
    t1.goto(tx, ty)
    t1.setheading(-90)
    # good to go

def drawArm(whichA):
    #assumes that turtle is at -90 position
    #assumes that turtle is at bottom of torso
    tx = t1.xcor()  # remember x and y coords for later
    ty = t1.ycor()
    t1.backward(int(sh*0.1))
    if(whichA == RIGHT):
        t1.left(aAngle + 90)
    else:
        t1.right(aAngle + 90)
    t1.pendown()
    t1.forward(int(sw*0.1))
    t1.penup()
    t1.goto(tx, ty)
    t1.setheading(-90)

def drawFace():
    print('hi')
    
    eR = int(sw*0.005)
    #print("eR is {}".format(eR))
    #print("hearR is {}".format(headR))
    xLoc = t1.xcor()
    yLoc = t1.ycor()
    hLoc = t1.heading()

    for i in range(2):
        t1.penup()
        #drawEyes
        t1.goto(nooseX, nooseY)
        if i % 2 >= 1:
            t1.goto(t1.xcor()-int(headR*0.4 + eR*0.5), t1.ycor()-int(headR*0.6))
        else:
            t1.goto(t1.xcor()+int(headR*0.4 + eR*0.5), t1.ycor()-int(headR*0.6))
        t1.pendown()
        t1.circle(eR)
        t1.penup()
        t1.goto(nooseX, nooseY)

    #drawMouth
    t1.goto(nooseX - int(headR*0.4 + eR*0.8), nooseY-int(headR*1.2))
    t1.pendown()
    mPiece = int( (headR*math.pi)/(10*2) )
    for i in range(3):
        forward(mPiece)
        left(14)
        #t1.showturtle()
    left(10)
    for i in range(7):
        forward(int(mPiece *1.03))
        left(16)
    for i in range(2):
        forward(mPiece)
        left(14)

    t1.penup()
    t1.goto(xLoc, yLoc)
    t1.setheading(hLoc)
    
    
            
    
    

#game starts here  -- this is like an intro
drawGallows()
drawHead()
drawTorso()
drawLeg(RIGHT)
drawLeg(LEFT)
drawArm(RIGHT)
drawArm(LEFT)
drawFace()
time.sleep(1)


#actual game setup
t1.clear()
drawGallows()
pickSecretWord()
displayText("Guess a Letter..")
displayBadLetters("Not in word: [" + lettersWrong + "]")
time.sleep(1)
makeWordString()
displayText(displayWord)
playGame()





