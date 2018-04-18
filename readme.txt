Before running the game please install pygame: https://www.pygame.org/wiki/GettingStarted

To run the textgame:
	in console do: python3 rushhour.py gamex.txt
	"gamex.txt" will be your game file of choice

To run the GUI game:
	in console do: python3 rushhour_gui.py gamex.txt
	"gamex.txt" will be your game file of choice

How to play:
the goal of the game is to move the red car (the "0" car in the text version) the right most tile of the board. The cars can only move forward and backward in the direction they face and no car is able to go through any other car. While playing the gui version click on the car you wish to move then click on where you would like it to move. If the location you want the car to move to is a valid location it will be moved, otherwise the car will remain in place. In the text version of the game type the number of the car you wish to move, press enter, type the number of the row you want the car in (numbered 1-6 1 being at the top and 6 being at the bottom), press enter, type the number of the column you want the car in (numbered 1-6 1 being at the farthest left and 6 being the farthest right). If this is a valid move the screen will update and the cars new location will be show. 