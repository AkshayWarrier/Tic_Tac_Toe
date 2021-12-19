#importing pygame
import pygame as pg
import random
#initializing pygame
pg.init()

#ended is true when the game ends
ended = False
char = 'X'
mode = input('Enter a mode[2P/AI]:')
#creating a pygame window
win = pg.display.set_mode((600,600))
'''
run- as long as run is true, the program will be running
board- list representing the board
placed,char - placed is a list that contains data of type (i,j,char). i and j used for position in board,
              char to represent which player made the move. In this case 'X' is always the
              player and 'O' is
              the computer
'''
run = True
board = [[0,1,2],[3,4,5],[6,7,8]]
#placed = [(1,1,'X'),(0,2,'O'),(1,2,'X'),(1,0,'O')]
placed = []



#function that is used to display X's/O's

def char_text(x,y,char):
    if char == 'X':
        colour = (255,0,0)
    else:
        colour = (0,255,0)
    charFont = pg.font.Font('Multicolore Pro.otf',65)
    charText = charFont.render(char,True,colour)
    win.blit(charText,(x,y))

#returns the number of moves left
def isMovesLeft(placed):
    return 9-len(placed)
    
#evaluates the value of the board, if 'X' wins then +10, if 'O' wins then -10 else return 0
'''
For reference:
(0,0) (1,0) (2,0)
(0,1) (1,1) (2,1)
(0,2) (1,2) (2,2)
'''


def evaluate():
        if (0,0,'X') in placed and (0,1,'X') in placed and (0,2,'X') in placed:
            return 10
        if (1,0,'X') in placed and (1,1,'X') in placed and  (1,2,'X') in placed:
            return 10
        elif (2,0,'X') in placed and  (2,1,'X') in placed and  (2,2,'X') in placed:
            return 10
        elif (0,0,'X') in placed and  (1,0,'X') in placed and  (2,0,'X') in placed:
            return 10
        elif (0,1,'X') in placed and  (1,1,'X') in placed and  (2,1,'X') in placed:
            return 10
        elif (0,2,'X') in placed and  (1,2,'X') in placed and  (2,2,'X') in placed:
            return 10
        elif (0,0,'X') in placed and  (1,1,'X') in placed and  (2,2,'X') in placed:
            return 10
        elif (0,2,'X')  in placed and  (1,1,'X') in placed and  (2,0,'X') in placed:
            return 10

        elif (0,0,'O') in placed and (0,1,'O') in placed and (0,2,'O') in placed:
            return -10
        elif (1,0,'O') in placed and (1,1,'O') in placed and  (1,2,'O') in placed:
            return -10
        elif (2,0,'O') in placed and  (2,1,'O') in placed and  (2,2,'O') in placed:
            return -10
        elif (0,0,'O') in placed and  (1,0,'O') in placed and  (2,0,'O') in placed:
            return -10
        elif (0,1,'O') in placed and  (1,1,'O') in placed and  (2,1,'O') in placed:
            return -10
        elif (0,2,'O') in placed and  (1,2,'O') in placed and  (2,2,'O') in placed:
            return -10
        elif (0,0,'O') in placed and  (1,1,'O') in placed and  (2,2,'O') in placed:
            return -10
        elif (0,2,'O') in placed and  (1,1,'O') in placed and  (2,0,'O') in placed:
            return -10
        else:
            return 0

   
def minimax(board,placed,depth,isMaximizingPlayer,alpha,beta):
    score = evaluate()
    
    #if maximizer has won then return their score
    if score == 10:
        return score
    #if minimizer has won then return their score
    if score == -10:
        return score
    #if there are no winners and no moves are left then it's a draw
    if isMovesLeft(placed) == 0:
        return 0
    #if it is maximizing player's move
    if isMaximizingPlayer:
        bestVal = -1000
        #traverse all cells
        for i in range(3):
            for j in range(3):
                #check if cell is empty
                if (i,j,'X') not in placed and (i,j,'O') not in placed:
                    #make the move
                    placed.append((i,j,'X'))
                    #call minimax recursively and choose the max value
                    bestVal = max(bestVal, minimax(board,placed,depth+1,not isMaximizingPlayer,alpha,beta))
                    alpha = max(alpha,bestVal)
                    #undo the move
                    placed.remove((i,j,'X'))
                    if beta <= alpha:
                        break
                    
                    

        return bestVal
    #similary for minimizing player
    else:
        bestVal = 1000
        for i in range(3):
            for j in range(3):
                if (i,j,'O') not in placed and (i,j,'X') not in placed:
                    placed.append((i,j,'O'))
                    bestVal = min(bestVal, minimax(board,placed,depth+1,not isMaximizingPlayer,alpha,beta))
                    beta = min(beta,bestVal)
                    placed.remove((i,j,'O'))
                    if beta <= alpha:
                        break
                    
        return bestVal


#This will return the best possible move for the computer
def findBestMove(board,placed):
    bestVal = 1000
    bx = -1
    by = -1
    '''Traverse all cells, evaluate minimax function for 
       all empty cells. And return the cell with optimal 
       value.'''
    for i in range(3):
        for j in range(3):
            #check if the cell is empty
            if (i,j,'O') not in placed and (i,j,'X') not in placed:
                #make the move
                placed.append((i,j,'O'))
                #get the value for this cell
                moveVal = minimax(board,placed,0,True,-1000,+1000)
                #undo the move
                placed.remove(((i,j,'O')))
                #if value of current move is better than the best value then update the best value
                if moveVal < bestVal:
                    bx = i
                    by = j
                    bestVal = moveVal

    #return random.choice([(bx,by),(random.choice([0,1,2]),random.choice([0,1,2]))])
    return (bx,by)
                
                
                

    

#function that draws the board and the 'Xs' and 'Os'        
def reDrawWindow(): 
    win.fill((255,255,255))
    for i in range(3):
        for j in range(3):
            pg.draw.rect(win,(0,0,0),(i*200,j*200,200,200),2)
    for i in placed:
        char_text((200*i[1]+200*(i[1]+1))//2-25, (200*i[0]+200*(i[0]+1))//2-25,i[2])


while run:
    #draw the board and players every frame or every iteration of while loop
    reDrawWindow()
    
    #update the display
    pg.display.update()


    #if the game has not ended then check whether it has, if it has then update 'ended' to True
    if ended == False:
        if evaluate() == 10:
            print('X has won!')
            ended = True
        if evaluate() == -10:
            print('O has won!')
            ended = True
        if isMovesLeft(placed) == 0:
            print('Draw!')
            ended = True
    #get any input that the user is giving
    for event in pg.event.get():
        
        #if user chooses to close the program then set run to False i.e stop the program
        if event.type == pg.QUIT:
            run = False
        #this if-statement is true whenever any keyboard key is pressed down 
        if event.type == pg.KEYDOWN:
            #check if user has pressed spacebar
            if event.key == pg.K_SPACE:
                #if the user has then reset the game if the game has ended
                if ended == True:
                    char = 'X'
                    placed = []
                    ended = False
        #this if-statement is true when any mouse button is pressed down 
        if event.type == pg.MOUSEBUTTONDOWN:
            #get the position of mouse
            x,y = pg.mouse.get_pos()
            #traverse through the board
            for i in range(3):
                for j in range(3):
                    #check whether if the position of mouse is within a box
                    if 200*i <= y <= 200*(i+1) and 200*j <= x <=200*(j+1):
                        #if it is then check if this position is empty
                        if (i,j,'X') not in placed and (i,j,'O') not in placed:
                            #if it is then play the move only if the game has not ended
                            if ended == False:
                                placed.append((i,j,char))
                                if mode == 'AI':
                                    #findBestMove is called as the player's turn is finished
                                    bestx,besty = findBestMove(board,placed)
                                    if bestx != -1:
                                        placed.append((bestx,besty,'O'))
                                elif mode == '2P':
                                    if char == 'X':
                                        char = 'O'
                                    elif char == 'O':
                                        char = 'X'
            
#close the program if while loop stop
pg.quit()
