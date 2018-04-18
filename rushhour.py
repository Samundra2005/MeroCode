#Noah Giustini
#30041939

#importing 
import pygame
import sys
import math

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

    #function that will load the game file and put the contents in it into a list    
    def loadGame(self):
        gameFile = open(sys.argv[1],"r")
        content = gameFile.readlines()
        gameFile.close()
        for x in range(len(content)):
            content[x].replace("\n","")
        return content

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


    #fucntion that will take the board list and print it out on screen
    def showBoard(self):
        for i in range(len(self.board)):
            row = ""
            for x in range(len(self.board[i])):
                row += self.board[i][x]
            print(row)

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
        self.showBoard()

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
    
    #function that will remove the car from the board so it can be put back in later in a different position
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

    #fuction that will move the cars according to player input as long as the move is legal
    def moveCar(self):
        target = int(input("Target car "))
        newRow = int(input("What row do you want the car in? ")) -1
        newCol = int(input("what column do you want the car in? ")) -1
        car = self.allCars[target]
        if self.isLegal(target,newRow,newCol) == 1:
            deltaR = newRow - car.rowPos
            deltaC = newCol - car.colPos
            deltaRfront = newRow - (car.rowPos + ( car.long - 1))
            deltaCfront = newCol - (car.colPos + (car.long - 1))
            if car.orient == "h":
                if deltaC > 0:
                    self.removeCar(target)
                    car.colPos += (deltaCfront)
                    self.updateBoard()
                elif deltaC < 0:
                    self.removeCar(target)
                    car.colPos += (deltaC)
                    self.updateBoard()
            elif car.orient == "v":
                if deltaR > 0:
                    self.removeCar(target)
                    car.rowPos += (deltaRfront)
                    self.updateBoard()
                elif deltaR < 0:
                    self.removeCar(target)
                    car.rowPos += (deltaR)
                    self.updateBoard()
        else:
            print("INVALID MOVE")
        
    #the actual function that will run the game
    def play(self):
        self.carGen()
        self.updateBoard()
        while self.endGame() != 1:
            self.moveCar()
        print()
        print("YOU WIN!")


#playing the game
if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write("usage: () game_file.txt\n")
        sys.exit()
    TrafficJam = Game()
    TrafficJam.play()
