#Noah Giustini
#30041939

#importing 
import pygame
import sys
import math
import random

#creating a new Car class that will be used to make our "car" objects
class Car:
    #initializing
    def __init__(self,name,orient,long,rowPos,colPos):
        self.name = name
        self.orient = str(orient)
        self.long = int(long) 
        self.rowPos = int(rowPos)
        self.colPos = int(colPos)
        self.front = int(self.frontOfCar() )
        self.rear = int(self.backOfCar())

    #function to determine the back of the cars
    def backOfCar(self):
        if self.orient == "v":
            return self.rowPos
        else:
            return self.colPos

    #function to determine the front of the car
    def frontOfCar(self):
        if self.orient == "v":
            return (self.rowPos + (int(self.long) ))
        else:
            return (self.colPos + (int(self.long) ))

    
#creating the game class that will be the core aspect of the game.
#this will import the puzzle, check legallities and actually move the cars
class Game:
    #initializing
    def __init__(self):
        self.listOfCars = self.loadGame()
        self.allCars = []
        self.board = [
            [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
            [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
            [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
            [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
            [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "],
            [" ¤ "," ¤ "," ¤ "," ¤ "," ¤ "," ¤ "]
            ]
        self.red = 255,0,0
        self.green = 0,255,0
        self.blue = 0,0,255
        self.black = 0,0,0
        self.yellow = 255,255,0
        self.size = int(100)
        self.boardSide = self.size * 6
        self.screen = pygame.display.set_mode((self.boardSide,self.boardSide))
        self.listOfSprites = []

        
    #function that will load the game file and put the contents in it into a list    
    def loadGame(self):
        gameFile = open(sys.argv[1],"r")
        content = gameFile.readlines()
        gameFile.close()
        for x in range(len(content)):
            content[x].replace("\n","")
        return content

#sets up the GUI so the game looks nice
    def setup(self):
        pygame.init()
        screen = self.screen
        screen.fill((255,255,255))
        count = 0
        for i in range(6):
            for x in range(6):
                #check if current loop value is even
                if count % 2 == 0:
                    pygame.draw.rect(screen, (255,255,255),[self.size*x,self.size*i,self.size,self.size])
                else:
                    pygame.draw.rect(screen, self.black, [self.size*x,self.size*i,self.size,self.size])
                count +=1
            count-=1
        pygame.draw.rect(screen,self.green,[500,200,100,100])
        for car in self.allCars:
            long_side = int(((self.size*(car.long))-10))
            short_side = int(90)
            x = ((car.colPos)*self.size + (5))
            y = ((car.rowPos)*self.size + (5))
            if car.name == 0:
                image = pygame.Surface((long_side,short_side))
                sprite = pygame.draw.rect(image,self.red,(0,0,((self.size*(car.long))-10),(self.size - 10)))
            elif car.long > 2:
                if car.orient == "h":
                    image = pygame.Surface((long_side,short_side))
                    sprite = pygame.draw.rect(image,self.yellow,(0,0,((self.size*car.long)-10),(self.size - 10)))
                else:
                    image = pygame.Surface((short_side,long_side))
                    sprite = pygame.draw.rect(image,self.yellow,(0,0,(self.size - 10),((self.size*car.long)-10)))
            else:
                if car.orient == "h":
                    image = pygame.Surface((long_side,short_side))
                    sprite = pygame.draw.rect(image,self.blue,(0,0,((self.size*car.long)-10),(self.size - 10)))
                else:
                    image = pygame.Surface((short_side,long_side))
                    sprite = pygame.draw.rect(image,self.blue,(0,0,(self.size - 10),((self.size*car.long)-10)))
            screen.blit(image,(x,y))
        pygame.display.update()

#this fucntion is used to get mouse inputs from the player and decipher what the player has clicked on
#this is then used to get the coords of the new position that the player wants the car to be in
#these new coords are then returned and can be used by the isLegal() function
    def movement(self):
        complete = False
        marker = 0
        target = None
        while complete == False:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    pygame.quit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if marker == 0:
                        marker = 1
                        origin = pygame.mouse.get_pos()
                        originX = origin[0] // 100
                        originY = origin[1] // 100
                        if self.board[originY][originX] != " ¤ ":
                            target = int(self.board[originY][originX])
                            car = self.allCars[target]
                            num = int(car.name)
                        else:
                            marker = 0
                            print("please click on a car")
                    elif marker == 1:
                        newPos = pygame.mouse.get_pos()
                        nCol = newPos[0] // 100
                        nRow = newPos[1] // 100
                        return car,nCol,nRow
                        
    #function to create car objects with all the aspects outlined in the game file
    def addCar(self,name,orient,long,rowPos,colPos):
        return Car(name,orient,long,rowPos,colPos)

    #function that will take all the cars that we have created and add them all together into one list
    def carGen(self):
        for x in range(len(self.listOfCars)):
            self.listOfCars[x].replace("\n","")
            spec = self.listOfCars[x].split(",")
            orient = spec[0]
            long = spec[1]
            rowPos = spec[2]
            colPos = spec[3]

            newCar = self.addCar(x,orient,long,rowPos,colPos)

            self.allCars.append(newCar)

    #function to update the board with the cars and their positions
    def updateBoard(self):
        for car in self.allCars:
            if car.orient == "h":                
                for x in range(int(car.long)):
                    if car.name <10:
                        self.board[int(car.rowPos)][int(car.colPos)+x] = " "+str(car.name)+" "
                    elif car.name >= 10:
                        self.board[int(car.rowPos)][int(car.colPos)+x] = str(car.name)+" "
            elif car.orient == "v":
                for x in range(int(car.long)):
                    if car.name <10:
                        self.board[int(car.rowPos)+x][int(car.colPos)] = " "+str(car.name)+" "
                    elif car.name >= 10:
                        self.board[int(car.rowPos)+x][int(car.colPos)] = str(car.name)+" "

    #fucntion to check the legallity of the player's moves
    #checks to make sur ethe car wont go out of the board and that there are no cars in the way of the move
    def isLegal(self,carnum,newRow,newCol):
        nRow = int(newRow)
        nCol = int(newCol)
        car = self.allCars[carnum]
        deltaR = int(nRow - car.rowPos)
        deltaC = int(nCol - car.colPos)
        if car.orient == "h":
            if nRow != car.rowPos:
                return 0
            elif deltaC > 0:
                for i in range(int(deltaC)):
                    if self.board[car.rowPos][(car.rear + ( 1 + i ))] != " ¤ ":
                        if int(self.board[car.rowPos][(car.rear + ( 1 + i ))]) == int(car.name):
                            pass
                        else:
                            return 0
                    elif (car.colPos + (deltaC)) > 6:
                        return 0
                    else:
                        return 1
            elif deltaC < 0:
                for i in range(int(math.fabs(deltaC))):
                    if self.board[car.rowPos][(car.colPos - ( 1 + i ))] != " ¤ ":
                        if int(self.board[car.rowPos][(car.colPos - ( 1 + i ))]) == int(car.name):
                            pass
                        else:
                            return 0
                    elif (car.colPos + (deltaC)) < 0:
                        return 0
                    else:
                        return 1        
        elif car.orient == "v":
            if nCol != car.colPos:
                return 0
            elif deltaR > 0:
                for i in range(int(deltaR)):
                    if self.board[(car.rowPos + (car.long -1 ) + ( 1 + i ))][(car.colPos)] != " ¤ ":
                        if int(self.board[(car.rowPos + (car.long -1 ) + ( 1 + i ))][(car.colPos)]) == int(car.name):
                            pass
                        else:
                            return 0
                    elif (car.rowPos + (deltaR)) > 6:
                        return 0
                    else:
                        return 1
            elif deltaR < 0:
                for i in range(int(math.fabs(deltaR))):
                    if self.board[car.rowPos - ( 1 + i )][(car.colPos)] != " ¤ ":
                        if int(self.board[car.rowPos - ( 1 + i )][(car.colPos)]) == int(car.name):
                            pass
                        else:
                            return 0
                    elif (car.rowPos + (deltaR)) < 0:
                        return 0
                    else:
                        return 1
#function to remover the cars from the previous list so they can be moved to a new spot  
    def removeCar(self,carnum):
        car = self.allCars[carnum]
        if car.orient == "h":                
            for x in range(int(car.long)):
                self.board[int(car.rowPos)][int(car.colPos)+x] = " ¤ "
        elif car.orient == "v":
            for x in range(int(car.long)):
                self.board[int(car.rowPos)+x][int(car.colPos)] = " ¤ "

    #function to see if the game is over
    def endGame(self):
        car = self.allCars[0]
        if (car.colPos + ((car.long) -1 )) == 5:
            return 1
        else:
            return 0

#function to move cars as long as the move is legal
    def moveCar(self):
        car,newCol,newRow = self.movement()
        num = int(car.name)
        if self.isLegal(num,newRow,newCol) == 1:
            deltaR = newRow - car.rowPos
            deltaC = newCol - car.colPos
            deltaRfront = newRow - (car.rowPos + ( car.long - 1))
            deltaCfront = newCol - (car.colPos + (car.long - 1))
            if car.orient == "h":
                if deltaC > 0:
                    self.removeCar(num)
                    car.colPos += (deltaCfront)
                    self.updateBoard()
                elif deltaC < 0:
                    self.removeCar(num)
                    car.colPos += (deltaC)
                    self.updateBoard()
            elif car.orient == "v":
                if deltaR > 0:
                    self.removeCar(num)
                    car.rowPos += (deltaRfront)
                    self.updateBoard()
                elif deltaR < 0:
                    self.removeCar(num)
                    car.rowPos += (deltaR)
                    self.updateBoard()
        else:
            print("INVALID MOVE")

       
    #the actual function that will run the game
    def play(self):
        self.carGen()
        self.updateBoard()
        self.setup()
        while self.endGame() != 1:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    pygame.quit
            self.moveCar()
            self.setup()
            
#main            
if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write("usage: () game_file.txt\n")
        sys.exit()
    TrafficJam = Game()
    TrafficJam.play()




    

