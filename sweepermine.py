import string
import random

# BEGINING OF ALTERED CODE EDIT AWAY 00000000000000000000000000000000000000000000000000000000

helpmessage = "Type the column followed by the row (eg. a5).\nTo put or remove a flag, add 'f' to the cell (eg. a5f)\n"
numberofmines = 10

# DO NOT EDIT PAST THIS POINT ONLY USE IT AS FOR REFRANCE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def setupgrid(gridsize,start,numberofmines):
    grid = [['0' for i in range(gridsize)] for i in range(gridsize)]
    mines = generatemines(grid,start,numberofmines)
    getnumbers(grid)
    return (grid,mines)
 
def showgrid(grid):
    gridsize = len(grid)
    horizontal = '   '+4*gridsize*'-'+'-'
    # Print top column letters
    toplabel = '     '
    for i in string.ascii_lowercase[:gridsize]:
        toplabel = toplabel+i+'   '
    print toplabel+'\n'+horizontal
    # Print left row numbers
    for idx,i in enumerate(grid):
        row = '{0:2} |'.format(idx+1)
        for j in i:
            row = row+' '+j+' |'
        print row+'\n'+horizontal
    print ''
 
def getrandomcell(grid):
    gridsize = len(grid)
    a = random.randint(0,gridsize-1)
    b = random.randint(0,gridsize-1)
    return (a,b)
 
def getneighbors(grid,rowno,colno):
    gridsize = len(grid)
    row = grid[rowno]
    column = grid[rowno][colno]
 
    neighbors = []
 
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0: continue
            elif -1<rowno+i<gridsize and -1<colno+j<gridsize:
                neighbors.append((rowno+i,colno+j))
    return neighbors
 
# Generate mines
def generatemines(grid,start,numberofmines):
    gridsize = len(grid)
    mines = []
    for i in range(numberofmines):
        cell = getrandomcell(grid)
        while cell==(start[0],start[1]) or cell in mines:
            cell = getrandomcell(grid)
        mines.append(cell)
 
    for i,j in mines: grid[i][j] = 'X'
    return mines
 
def getnumbers(grid):
    gridsize = len(grid)
    for rowno,row in enumerate(grid):
        for colno,col in enumerate(row):
            if col!='X':
                # Gets the values of the neighbors
                values = [grid[r][c] for r,c in getneighbors(grid,rowno,colno)]
 
                # Counts how many are mines
                grid[rowno][colno] = str(values.count('X'))
 
def showcells(grid,currgrid,rowno,colno):
    # Exit function if the cell was already shown
    if currgrid[rowno][colno]!=' ':
        return
 
    # Show current cell
    currgrid[rowno][colno] = grid[rowno][colno]
 
    # Get the neighbors if the cell is empty
    if grid[rowno][colno] == '0':
        for r,c in getneighbors(grid,rowno,colno):
            # Repeat function for each neighbor that doesn't have a flag
            if currgrid[r][c] != 'F':
                showcells(grid,currgrid,r,c)
 
def playagain(lastcell):
    choice = raw_input('Play again? (y/n): ')
    return choice.lower() == 'y'

# BEGINING OF ALTERED CODE EDIT AWAY 00000000000000000000000000000000000000000000000000000000
    
def getinput(currgrid, lastcell, flags, IndexError):
    while True:
        lastcell = str(raw_input('Enter the cell ({} mines left): '.format(numberofmines-len(flags))))            
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
                return False    
        except (IndexError,ValueError):
            showgrid(currgrid)
            print "Invalid cell.",helpmessage
    

# DO NOT EDIT PAST THIS POINT ONLY USE IT AS FOR REFRANCE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
def playgame():
    numberofmines = 10
    gridsize = 9
    helpmessage = "Type the column followed by the row (eg. a5).\nTo put or remove a flag, add 'f' to the cell (eg. a5f)\n"
    
    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]
    showgrid(currgrid)
    grid = []
    flags = []
    print helpmessage

    while True:
        while True:
            lastcell = str(raw_input('Enter the cell ({} mines left): '.format(numberofmines-len(flags))))
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
            rowno,colno = lastcell
     
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
                        if playagain(): playgame()
                        else: exit()
                    else:
                        showcells(grid,currgrid,rowno,colno)
     
            showgrid(currgrid)
     
            if set(flags)==set(mines):
                print 'You Win'
                if playagain(): playgame()
                else: exit()
