"""
Author @ Villaire A. Pierre

A wordle clone
The objective is to have the game generate a random word and give the user chances at guessing that word. 

"""

from bs4 import BeautifulSoup as bs
from PyDictionary import PyDictionary as pdc
import os,string,random
import urllib.request as rq


class Bordle:

    """Class Members"""
    __CPU:str
    __guess:str
    __turns:int
    __hintLimit:int 
    __options = []


    """Constructor"""
    def __init__(self):
        self.__turns = 6
        self.__hintLimit = 1


    """get random word for game"""
    def getBordle(self) -> str:
        if not self.__options: #no words loaded into game
            try:
                with open("urls.txt") as urls:
                    options = urls.read().splitlines()

                    url = random.choice(options)
                    response = rq.urlopen(url)

                    soup = bs(response.read(), "html.parser")
                    for item in soup(["script","style"]):
                        item.extract()
                    
                    self.__options = soup.get_text().split()
                    self.__CPU = random.choice(self.__options)

            except Exception as e:
                #print(e)
                with open("local.txt") as locals:
                    self.__options = locals.read().splitlines()
                    self.__CPU = random.choice(self.__options)

        else: #if options has words, pick another random one
            self.__CPU = random.choice(self.__options)



    """display a hint to the user"""
    def getHint(self):
        print("Hint Requested!")
        print("What hint would you like?\n")
        ans = input("Please enter \"d\" for a definition of the word or \"r\" to reveal a random letter in the word! Quit with \"q\"\n").lower()

        if not isinstance(ans,str):
            print("Sorry I didnt understand that!")
            #return False
        if self.__hintLimit < 1:
            print("Sorry You are all out of hints!\n")
            #return False
        else:
            while self.__hintLimit > 0:
                if ans not in ["d","r","q"]:
                    print("Sorry I didnt understand that.")
                    print("Please enter \"d\" for a definition of the word or \"r\" to reveal a random letter in the word! Quit with \"q\"\n")
                    continue
                elif ans in "d":
                    self.define()
                    break
                elif ans in "r":
                    self.reveal()
                    break
                elif ans in "q":
                    print("Quitting!")
                    break
                else:
                    print("Sorry I still do not understand! Exiting...")
                    #return False
        #return True


    def define(self):
        definition = pdc.meaning(self.__CPU)
        print("The definition of the word is as follows!\n")
        for defi in definition:
            print(definition[defi], "\n")
        self.__hintLimit = 0

    
    def reveal(self):
        hint = random.randint(0,len(self.__CPU))
        print(f"The word contains the letter '{self.__CPU[hint]}'")
        self.__hintLimit = 0


    """display starting message"""
    @staticmethod
    def displayIntroMessage():
        print("\n\nWELCOME TO BORDLE!")
        print("Todays we have a 5 letter word for you to guess!")
        print("You have 6 tries to guess the word!\n\n")
        print("Lets Begin!\n")


    """display the results of a wrong guess"""
    def display(self):
        response = ""
        good = "✅ "
        bad = "❎"
        included = "~" 

        for i in range(len(self.__CPU)):
            if self.__guess[i] == self.__CPU[i]:
                response+=good
            elif self.__guess[i] in self.__CPU:
                response+=included
            else:
                response+=bad

        print(self.__guess)
        print(response)


    """
    validate the guess the user gives
    returns a boolean value if the guess is valid or not
    """
    def validate_guess(self) -> bool:
        if not isinstance(self.__guess, str):
            print("Invalid Input! Please try again!")
            return False

        if (len(self.__guess) != len(self.__CPU)):
            print("This Guess Was Not The Correct Length! Try Again!\n")
            return False

        punc = list(string.punctuation)
        if any(char in punc for char in self.__guess):
            print("This Guess Contained an Invalid Character! Try Again!\n")
            return False
        return True


    """start the game"""
    def bordleStart(self):
        self.getBordle()
        while(self.__turns > 0):
            self.__guess = input("Please Enter Your Guess! Enter \"h\" If You Would Like a Hint!\n").lower()

            if self.__guess == "h":             
                self.getHint()
                continue

            if not self.validate_guess():
                continue

            if self.__guess == self.__CPU:
                print(f"CONGRATULATIONS, YOU WIN! THE WORD WAS {self.__CPU.upper()}")
                print("PLAY AGAIN? (y/n)\n")
                ans = input().lower()
                
                if ans == "n":
                    print("THANKS FOR PLAYING.\n GOODBYE!")
                    break
                elif ans == 'y':
                    self.reset()
                    continue
                else: break
                    
            else:
                self.display()
                self.__turns -= 1
                print(f"You Have {self.__turns} try(s) left!\n")


    """reset the game if user wants to play again"""
    def reset(self):
        print("RESETING...\n")
        self.__turns = 6
        self.__hintLimit = 1
        self.getBordle()
    

    """prototype to display a game over screen with their stats"""
    def game_end():
        pass
    

    """prototype to record stats after every round"""
    def stats(self):
        pass


    """cache stats in stats file after game end"""
    def cache_stats(self):
        pass
