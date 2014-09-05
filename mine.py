import string
import random
from sweepermine import * 
from Automata import *
from Util import *
from PartitionRefinement import *
from Sequence import *
from ttable import * 

#INPUT ALPHABET FOR NFA
alphabet =  ['1?', '0?', '2?', '3?', '4?', '5?', '?B', '??', '00', '11', '1B', '22', '2B', '33', '3B', '44', '4B', '5B', 'BB']    
#CREATE NFA
nfa = LookupNFA(alphabet, '0', ttable, {'0','1','2','3','4','5','6','7','8','9', '10', '11', '12', '25', '26','27','28','29', '30'})    

def checkFlag(grid, rowNum, colNum, coords):

    cellNeighbors = getneighbors(grid, rowNum, colNum)
    # print "cellNeighbors: \n", cellNeighbors
    flagCount = 0
    
    for i in cellNeighbors:
        if (grid[i[0]][i[1]] == 'F' and i not in coords):
             flagCount += 1
             
    return flagCount

#CREATE THE NEW BOARDS FOR A CONSTSTANT BOARDS
def derivation_tree(inputTape, state, derTree, branch):
    dTree = derTree
    iTape = inputTape[:]
    
    if iTape:
        input = iTape.pop(0)       
        newStates = nfa.transition(state, input)
            
        for nState in newStates:            
            newBranch = branch[:]    
            derTree = dTree
            stateName = descriptor.pop(int(nState))
            descriptor.insert( int(nState), stateName ) 
            
            newBranch.append((state, input, nState, stateName))
            
            derivation_tree(iTape, nState, derTree, newBranch)
            derTree.append((state, input, nState, stateName))              
                  
    else:
        print "Printing full tree:"
        for leaf in branch:
            print leaf[0], ',', leaf[1], '->', leaf[2], '(', leaf[3], ')' 
        print ""
    return derTree           
                
def get_2xn(grid):

    topLeftCell = str(raw_input('Enter the top left cell of the 2 x n board you would like to test for consistency: '))
    topLeftCell = (int(topLeftCell[1])-1,string.ascii_lowercase.index(topLeftCell[0]))
    botRightCell = str(raw_input('Enter the bottom right cell of the 2 x n board you would like to test for consistency: '))
    botRightCell = (int(botRightCell[1])-1,string.ascii_lowercase.index(botRightCell[0]))
    lRow, lCol = topLeftCell
    rRow, rCol = botRightCell

    tempTape = []
    modifiedTape = []
    tempCoords = []

    while ((rRow - lRow) != 1 and (rCol - lCol) != 1):
        print "That is not a 2 x n board. Please re-enter: "
        topLeftCell = str(raw_input('Enter the top left cell of the 2 x n board you would like to test for consistency: '))
        topLeftCell = (int(topLeftCell[1])-1,string.ascii_lowercase.index(topLeftCell[0]))
        botRightCell = str(raw_input('Enter the bottom right cell of the 2 x n board you would like to test for consistency: '))
        botRightCell = (int(botRightCell[1])-1,string.ascii_lowercase.index(botRightCell[0]))
        lRow, lCol = topLeftCell
        rRow, rCol = botRightCell

    if (rRow - lRow == 1):
        for d in range(lCol, rCol + 1):
            tempTape.append([grid[lRow][d], grid[rRow][d]])
            tempCoords.append((lRow, d))
            tempCoords.append((rRow, d))

    else:
        for d in range(lRow, rRow + 1):
            tempTape.append([grid[d][lCol], grid[d][rCol]])
            tempCoords.append((d, lCol))
            tempCoords.append((d, rCol))

    if (rRow - lRow == 1):
        for d in range(lCol, rCol + 1):
            # tempTape.append([grid[lRow][d], grid[rRow][d]])
            # tempCoords.append((lRow, d))
            # tempCoords.append((rRow, d))

            

            lFlags = checkFlag(grid, lRow, d, tempCoords)
            rFlags = checkFlag(grid, rRow, d, tempCoords)
            # print "grid[lRow][d]: ", grid[lRow][d]
            
            if (grid[lRow][d] != " " and grid[lRow][d] != 'F'):
                # print "inside if statement int(grid[lRow][d]):", int(grid[lRow][d]) 
                modTapeL = str(int(grid[lRow][d]) - lFlags)
                # print "modTapeL: ", modTapeL
            else:
                modTapeL = grid[lRow][d]

            if (grid[rRow][d] != " " and grid[rRow][d] != 'F'):
                modTapeR = str(int(grid[rRow][d]) - rFlags)
                # print "modTapeR: ", modTapeR

            else:
                modTapeR = grid[rRow][d]    
                
            modifiedTape.append([modTapeL, modTapeR])
            #print "cell at ", lRow, d, "has " , checkFlag(grid, lRow, d), " bombs around it" 
    else:
        for d in range(lRow, rRow + 1):
            # tempTape.append([grid[d][lCol], grid[d][rCol]])
            # tempCoords.append((d, lCol))
            # tempCoords.append((d, rCol))

            lFlags = checkFlag(grid, d, lCol, tempCoords)
            rFlags = checkFlag(grid, d, rCol, tempCoords)
            # print "grid[lRow][d]: ", grid[lRow][d]
            
            if (grid[d][lCol] != " " and grid[d][lCol] != 'F'):
                # print "inside if statement int(grid[d][lCol]):", int(grid[d][lCol]) 
                modTapeL = str(int(grid[d][lCol]) - lFlags)
                # print "modTapeL: ", modTapeL
            else:
                modTapeL = grid[d][lCol]

            if (grid[d][rCol] != " " and grid[d][rCol] != 'F'):
                modTapeR = str(int(grid[d][rCol]) - rFlags)
                # print "modTapeR: ", modTapeR

            else:
                modTapeR = grid[d][rCol]    
                
            modifiedTape.append([modTapeL, modTapeR])
    
    return modifiedTape 
    
def make_tape(grid):
    
    inputTape = []
    for row in grid:
        tempRow = []
        temp = ""
        for cell in row:
            if cell == " ":    
                temp += '?'
            elif cell == 'F':
                temp += 'B'
            else:
                temp += cell
        if (temp in alphabet):
            inputTape.append(temp)   
        else:
            temp = temp[::-1]
            inputTape.append(temp)

    print "Input tape: ", inputTape
    return inputTape
        
def main():
    numberofmines = 10
    gridsize = 9
 
    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]
    showgrid(currgrid)
    grid = []
    flags = []
    helpmessage = "Type the column followed by the row (eg. a5).\nTo put or remove a flag, add 'f' to the cell (eg. a5f)\n"
    doNfa = False
    print helpmessage
    while True:
        while True:
            lastcell = str(raw_input('Enter the cell ({} mines left): '.format(numberofmines-len(flags))))
            if lastcell == "nfa":
                doNfa = True
                break;
            print '\n\n'
            flag = False
            try:
                if lastcell[2] == 'f': flag = True
            except IndexError: pass

            try:
                if lastcell == 'help':
                    print helpmessage
                else:
                    lastcell = (int(lastcell[1])-1,string.ascii_lowercase.index(lastcell[0]))
                    break
            except (IndexError,ValueError):
                showgrid(currgrid)
                print "Invalid cell.",helpmessage
                
        if len(grid)==0:
            grid,mines = setupgrid(gridsize,lastcell,numberofmines)
        # grid = [['0', '1', 'X', '1', '0', '0', '0', '0', '0'], ['0', '2', '2', '2', '0', '0', '0', '0', '0'], ['0', '1', 'X', '1', '0', '0', '0', '0', '0'], ['0', '1', '2', '3', '2', '1', '0', '0', '0'], ['0', '0', '1', 'X', 'X', '1', '1', '1', '1'], ['1', '1', '2', '2', '2', '1', '1', 'X', '1'], ['1', 'X', '1', '1', '1', '2', '2', '3', '2'], ['2', '2', '1', '1', 'X', '2', 'X', '2', 'X'], ['X', '1', '0', '1', '1', '2', '1', '2', '1']]
        # mines = [(0, 2), (7, 8), (5, 7), (7, 6), (4, 4), (4, 3), (6, 1), (2, 2), (7, 4), (8, 0)]
        
        if not doNfa:
            rowno,colno = lastcell
            f = open('temp','w')
            f.write(str(grid))
            f.write('\n')
            f.write(str(mines))
            f.close()
            print grid
            print mines
            
            if flag:
                # Add a flag if the cell is empty
                if currgrid[rowno][colno]==' ':
                    currgrid[rowno][colno] = 'F'
                    flags.append((rowno,colno))
                # Remove the flag if there is one
                elif currgrid[rowno][colno]=='F':
                    currgrid[rowno][colno] = ' '
                    flags.remove((rowno,colno))
                else: print 'Cannot put a flag there'

            else:
                # If there is a flag there, show a message
                if (rowno,colno) in flags:
                    print 'There is a flag there'
                else:
                    if grid[rowno][colno] == 'X':
                        print 'Game Over\n'
                        showgrid(grid)
                        # if playagain(): playgame()
                        exit()
                    else:
                        showcells(grid,currgrid,rowno,colno)

            showgrid(currgrid)
        # BEGINING OF COPY CODE
        # print "grid: \n" , grid
        # print "currgrid: \n" , currgrid            
        # print "mines \n", mines
        if doNfa:
            tempGrid = get_2xn(currgrid)
            print "Copied board: ", tempGrid
            #END OF COPY CODE
            inputTape = make_tape(tempGrid)
            
            if( nfa.__call__( inputTape ) ):
                dTree = derivation_tree(inputTape, '0', [],[])
                # print "dTree: ", dTree
                # while dTree:
                    # tree = [dTree.pop()]
                
                    # conBoards = consistant_boards(tree, dTree, tempGrid)
                # print "consistant boards ", conBoards 
                
            else:
                print "Input not consistent."     
            doNfa = False
        
        if set(flags)==set(mines):
            print 'You Win'
            # if playagain(): playgame()
            exit()        
main()