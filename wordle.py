#!/usr/bin/env python3
from colored import bg, fg, attr
import blessed
import datetime
import time
from getch import getch
import possible
import os

term = blessed.Terminal()

unicode=False
eightColor=True
termwhite = term.bold_white
termgreen = term.bold_green
if 'TERM' in os.environ:
    if 'xterm' in os.environ['TERM']:
        unicode=True
    if not 'ansi' in os.environ['TERM']:
        eightColor=False
        termwhite=term.bright_white
        termgreen=term.bright_green
if eightColor:
    colors =[ term.white_on_white, term.gray_on_gray,term.yellow_on_yellow,term.green_on_green,term.black_on_lightgray]
    cardLetterColors =[ term.black_on_white, term.black_on_gray,term.bold_white_on_yellow,term.bold_white_on_green,term.black_on_lightgray]

    keycolors = [term.bold_white_on_black, term.black_on_black,term.yellow_on_black,term.bold_green_on_black]
    reset = term.white_on_black
else:
    colors =[ term.white_on_white, term.dimgray_on_dimgray,term.bright_yellow_on_bright_yellow,term.reverse_green_on_bright_white,term.lightgray_on_lightgray]
    cardLetterColors =[ term.black_on_white, term.bright_white_on_dimgray,term.reverse_bright_yellow_on_dimgray,term.reverse_green_on_bright_white,term.on_lightgray]
    keycolors = [termwhite, term.black_on_black,term.bright_yellow_on_black,term.bold_green_on_black]
    reset=term.white_on_black + term.normal

class Wordle:
    def check(self):
        word=self.curGuess.upper()
        if word.lower() not in possible.guesses and word.lower() not in possible.answers:
            return False
        else:
            turn=self.turn
            self.guesses[turn][0]=[4,4,4,4,4]
            self.drawGuessLine(turn)
            time.sleep(0.01)
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
        putCursorInside(min(self.turn,5),min(len(self.curGuess),4))
    def drawGuessLine(self,i):
        baseRow = i * 4;
        baseCol = 46
        guess = self.guesses[i]
        for line in range(3):
            placeCursor(baseCol, baseRow+line)
            for k,letter in enumerate(guess[0]):
                drawing=["_|","_|","_|"," |","_|"];
                if line==0:
                    put(colors[letter]+"     "+reset+term.black_on_black+drawing[letter][1]+reset)
                elif line==2:
                    put(colors[letter]+drawing[letter][0]*5+reset+term.black_on_black+drawing[letter][1]+reset)
                else:
                    put(colors[letter]+"  "+cardLetterColors[letter]+guess[1][k]+term.normal+colors[letter]+"  "+reset+term.black_on_black(drawing[letter][1])+reset)
    def drawStatusLine(self):
        placeCursor(9,21)
        put(reset+str(self.number))
        placeCursor(34,21)
        if(self.wonGame()):
            t=self.turn
        else:
            t=self.turn+1
        placeCursor(40,21)
        put(str(min(t,6))+"/6"+colors[0])

    def drawKeyboard(self):
        def putKey(key):
            if key.upper() in self.guessedKeys:
                if self.guessedKeys[key.upper()] > 1:
                    put(keycolors[self.guessedKeys[key.upper()]]+key+' '+term.normal)
                else:
                    put(reset+'  ')
            else:
                put(reset+key+' ')

        placeCursor(13,17)
        for key in "qwertyuiop":
            putKey(key)
        placeCursor(14,18)
        for key in "asdfghjkl":
            putKey(key)
        placeCursor(16,19)
        for key in "zxcvbnm":
            putKey(key)


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
    def updateError(self,e="                                        +"):
        if e[-1]=="+":
            e=e[:-1]
            put(reset)
        else:
            put(term.white_on_black_reverse)
        self.errorStatus = e
        placeCursor(3, 22)
        put(e+colors[0]+term.normal)
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
def blankScreen():
    put(reset+term.clear)
    placeCursor(0,0)
    '''
    put(reset+'\033[2J')
    placeCursor(0,0)
    put(reset+((" "*80+"\n")*24));
    placeCursor(0,0)'''
def main():
    cursorLocation = 0
    blankScreen()
    if not unicode: 
    	  screen=termgreen+'''                             _ _         
      __      _____  _ __ __| | | ___    
      \ \ /\ / / _ \| '__/ _` | |/ _ \   
       \ V  V / (_) | | | (_| | |  __/   
        \_/\_/ \___/|_|  \__,_|_|\___|   '''
    else:
        screen=term.bright_green+'''
   ████████████████████████████████████████
   █▄─█▀▀▀█─▄█─▄▄─█▄─▄▄▀█▄─▄▄▀█▄─▄███▄─▄▄─█
   ██─█─█─█─██─██─██─▄─▄██─██─██─██▀██─▄█▀█
   ▀▀▄▄▄▀▄▄▄▀▀▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀'''
    screen +='''
               clone by xereeto
           original by josh wardle       '''+termwhite+'''
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
   Game:                         Turn:    
                                                                           '''
    put(screen)
    goHome()
    #print(screen,end="")
    goHome()
    w = Wordle()
    while w.turn<6 and not w.wonGame():
        turnOver = False
        w.curGuess=""
        prevchar = 0
        char = 0
        w.placeCursor()
        while not turnOver:
            put(term.black)
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
            if ord(char)==127 or ord(char)==8: # backspace
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
                    w.updateError("Word not in dictionary!")
    if w.wonGame():
        s="s"
        if w.turn==1:
            s=""
        w.updateError("You won in "+str(w.turn)+" turn"+s+"!")
    else:
        w.updateError("You lost :( The word was "+w.answer+"!")
    time.sleep(2)
    midnight = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=0, minute=0, microsecond=0, second=0)
    w.updateError()
    w.updateError("Next WORDLE in: "+str(datetime.timedelta(seconds=(midnight-datetime.datetime.now()).seconds)))	
    time.sleep(2)
    w.updateError("Press any key to exit...")
    x=getch()
    return w




import sys
w=None
try:
    with term.fullscreen(), term.hidden_cursor():
        w=main()

except KeyboardInterrupt:
    pass
finally:
    with term.fullscreen():
        put(term.clear)
    print(reset+"Goodbye!")
    #put("Goodbye!")
    cliflag = sys.argv[1] if len(sys.argv) > 1 else ''
    if(w and cliflag != "--no-unicode" and unicode):
        print("\n\nWordle "+str(w.turn)+"/6")
        blocks=["⬛","🟨","🟩"]
        for guess in w.guesses:
            if guess[0][0]:
                for letter in guess[0]:
                    put(blocks[letter-1])
                print()

