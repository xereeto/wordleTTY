#!/usr/bin/env python3
from colored import bg, fg, attr
import datetime
import time
from getch import getch
import possible

colors = [bg("white")+fg("black"), bg("dark_gray")+fg("white"),bg("light_yellow")+fg("dark_gray"),bg("green")+fg("white"),bg("light_gray")]
keycolors = [fg("white")+bg("black"), fg("dark_gray")+bg("black"),fg("light_yellow")+bg("black"),fg("green")+bg("black")]
reset = bg("black")+fg("white")

class Wordle:
    def check(self):
        word=self.curGuess.upper()
        if word.lower() not in possible.guesses and word.lower() not in possible.answers:
            return False
        else:
            turn=self.turn
            self.guesses[turn][0]=[4,4,4,4,4]
            self.drawGuessLine(turn)
            time.sleep(0.05)
            self.guesses[turn][1] = word
            processed=[]
            for i,letter in enumerate(word):
                if letter == self.answer[i]:
                    self.guesses[turn][0][i] = 3
                    self.guessedKeys[letter] = 3
                    processed.append(letter)
            for i,letter in enumerate(word):
                if letter in self.answer and processed.count(letter)<self.answer.count(letter) and letter != self.answer[i]:
                    processed.append(letter)
                    self.guesses[turn][0][i] = 2
                    if letter not in self.guessedKeys:
                        self.guessedKeys[letter] = 2
                else:
                    self.guesses[turn][0][i] = max(self.guesses[turn][0][i]%4,1)
                    if letter not in self.guessedKeys:
                        self.guessedKeys[letter] = 1
            self.drawGuessLine(self.turn)
            self.turn +=1
            self.drawStatusLine()
            self.drawKeyboard()
            return True

    def wonGame(self):
        return self.curGuess == self.answer
    def placeCursor(self):
        putCursorInside(self.turn,min(len(self.curGuess),4))
    def drawGuessLine(self,i):
        baseRow = i * 4;
        baseCol = 46
        guess = self.guesses[i]
        for line in range(3):
            placeCursor(baseCol, baseRow+line)
            for k,letter in enumerate(guess[0]):
                if line!=1:
                    put(colors[letter]+"     "+reset+" ")
                else:
                    put(colors[letter]+"  "+guess[1][k]+"  "+reset+" ")
    def drawStatusLine(self):
        placeCursor(9,21)
        put(reset+str(self.number))
        placeCursor(34,21)
        put("Turn: "+str(min(self.turn+1,6))+"/6"+colors[0])

    def drawKeyboard(self):
        placeCursor(13,17)
        for key in "qwertyuiop":
            if key.upper() in self.guessedKeys:
                put(keycolors[self.guessedKeys[key.upper()]]+key+' ')
            else:
                put(reset+key+' ')
        placeCursor(14,18)
        for key in "asdfghjkl":
            if key.upper() in self.guessedKeys:
                put(keycolors[self.guessedKeys[key.upper()]]+key+' ')
            else:
                put(reset+key+' ')
        placeCursor(16,19)
        for key in "zxcvbnm":
            if key.upper() in self.guessedKeys:
                put(keycolors[self.guessedKeys[key.upper()]]+key+' ')
            else:
                put(reset+key+' ')


        put(colors[0])

    def __init__(self):
        start = datetime.date(2021,6,19)
        number = (datetime.date.today()-start).days
        self.number = number
        self.turn = 0
        self.curGuess=""
        self.answer = possible.answers[number].upper()
        self.guessedKeys = {}
        # 0 = no guess, 1 = not in word, 2 = wrong place, 3 = correct
        self.guesses = [[[0 for i in range(5)],"     "] for i in range(6)]
        for i in range(6):
            self.drawGuessLine(i)
        self.drawStatusLine()
        self.drawKeyboard()
        self.errorStatus=""
    def updateError(self,e=reset+"                                        "+colors[0]):
        self.errorStatus = e
        placeCursor(3, 22)
        put(e)
        self.placeCursor()



def put(s):
    print(s,end='',flush=True);
def move(direction,n=1):
    keymap={"u":"A","d":"B","l":"D","r":"C"}
    put("\033["+str(n)+keymap[direction]);
def goHome():
    print("\r")
    move("u",50)
def placeCursor(x,y):
    goHome()
    if x>0:
        move("r",x)
    if y>0:
        move("d",y)
def putCursorInside(guess,letter):
    row = guess * 4 + 1;
    col = 48 + letter * 6;
    placeCursor(col,row);
    put(colors[0])

def main():
    cursorLocation = 0
    print(reset+"\033c")
    screen="\x1b[?25l"+fg('green')+'''
   ████████████████████████████████████████
   █▄─█▀▀▀█─▄█─▄▄─█▄─▄▄▀█▄─▄▄▀█▄─▄███▄─▄▄─█
   ██─█─█─█─██─██─██─▄─▄██─██─██─██▀██─▄█▀█
   ▀▀▄▄▄▀▄▄▄▀▀▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀
                           clone by xereeto
                    original by josh wardle'''+fg('white')+'''
   ----------------------------------------
   Guess the WORDLE in 6 tries.
   Each guess must be a valid 5 letter word.
   Press the enter button to submit.

   After each guess, the color of the tiles
   will change to show how close your guess
   was to the word.
   ----------------------------------------
   Keys:
             q w e r t y u i o p
              a s d f g h j k l
                z x c v b n m
   ----------------------------------------
   Game: XXX
                                                                           '''
    goHome()
    print(screen,end="")
    goHome()
    w = Wordle()
    while w.turn<6 and not w.wonGame():
        turnOver = False
        w.curGuess=""
        prevchar = 0
        char = 0
        w.placeCursor()
        while not turnOver:
            try:
                char = getch().upper()
            except OverflowError:
                pass
            if ord(char)==3:
                return
            prevchar = ord(char)
            if char>="A" and char <="Z" and prevchar !=91:
                if len(w.curGuess)<5:
                    put(char)
                    w.curGuess+=char
                    w.updateError()
                w.placeCursor()
            if ord(char)==127: # backspace
                if len(w.curGuess)>0:
                    if len(w.curGuess)==5:
                        put(" ")
                        w.curGuess=w.curGuess[:-1]
                        w.placeCursor()
                    else:
                        w.curGuess=w.curGuess[:-1]
                        w.placeCursor()
                        put(" ")
                        move("l",1)
                    w.updateError();
            if ord(char)==10: # enter
                if len(w.curGuess)<5:
                    w.updateError("Use all 5 letters!")
                elif w.check():
                    turnOver=True
                else:
                    w.updateError("You have to enter a real word!")
    if w.wonGame():
        s="s"
        if w.turn==1:
            s=""
        w.updateError("You won in "+str(w.turn)+" turn"+s+"!")
    else:
        w.updateError("You lost :( The word was "+w.answer+"!")
    time.sleep(2)
    midnight = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=0, minute=0, microsecond=0, second=0)
    w.updateError("Next WORDLE in: "+str(datetime.timedelta(seconds=(midnight-datetime.datetime.now()).seconds)))	
    time.sleep(2)
    return w




import sys
try:
    w=main()
except KeyboardInterrupt:
    pass
finally:
    print("\033cGoodbye!"+reset,end='')
    cliflag = sys.argv[1] if len(sys.argv) > 1 else ''
    if(cliflag != "--no-unicode"):
        print("\n\nWordle "+str(w.turn)+"/6")
        blocks=["⬛","🟨","🟩"]
        for guess in w.guesses:
            if guess[0][0]:
                for letter in guess[0]:
                    put(blocks[letter-1])
                print()
    print("\x1b[?25h")
