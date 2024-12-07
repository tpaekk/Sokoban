from cmu_graphics import *
from sokoban_loader import *

def onAppStart(app):
    app.levels = [
        'level1-10x10.png',
        'level2-7x9.png',
        'level3-8x6.png',
        'level4-8x6.png'
    ]
    app.currentLevel = 0
    app.moveHistory = [] 
    loadLevelData(app)
    app.won = False

# load level from sokoban_loader.py
def loadLevelData(app):
    level, images = loadLevel(app.levels[app.currentLevel])
    app.board = []
    for row in level:
        newRow = []
        for cell in row:
            if cell in 'RGBVC':
                newRow.append('-')
            else:
                newRow.append(cell)
        app.board.append(newRow)

    app.targets = []
    for row in level:
        newRow = []
        for cell in row:
            if cell in 'RGBVC':
                newRow.append(cell.lower())
            else:
                newRow.append('-')
        app.targets.append(newRow)
    app.playerRow, app.playerCol = findPlayerPosition(app.board)
    app.moveHistory = []
    app.won = False

    # centering the level on canvas
    app.cellSize = min(500 // len(app.board), 500 // len(app.board[0]))
    app.boardWidth = app.cellSize * len(app.board[0])
    app.boardHeight = app.cellSize * len(app.board)
    app.xOffset = (600 - app.boardWidth) // 2
    app.yOffset = (500 - app.boardHeight) // 2 + 100

def findPlayerPosition(board):
    for rowIndex in range(len(board)):
        for colIndex in range(len(board[rowIndex])):
            if board[rowIndex][colIndex] == 'p':
                return rowIndex, colIndex
    return None, None

def onKeyPress(app, key):
    # restart game
    if key == 'r':
        loadLevelData(app)
    # ignore all key presses except 'restart'
    elif app.won:
        return
    # undo
    elif key == 'u':
        undoLastMove(app)
    # set level 1 to one move from solved
    elif key == 'a' and app.currentLevel == 0:
        hardcodedLevel(app)
    # load respective level
    elif key in ['1', '2', '3', '4']:
        app.currentLevel = int(key) - 1
        loadLevelData(app)
    # move player in respective directions
    elif key in ['up', 'down', 'left', 'right']:
        movePlayer(app, key)
        checkWinCondition(app)

def movePlayer(app, direction):
    dr, dc = getDirections(direction)
    newRow = app.playerRow + dr
    newCol = app.playerCol + dc
    # checking cells beyond the block player is trying to move
    beyondRow = newRow + dr
    beyondCol = newCol + dc

    if not isValidMove(app, newRow, newCol):
        return

    # save the current state before making a move
    app.moveHistory.append({
        'board': [row[:] for row in app.board],
        'playerRow': app.playerRow,
        'playerCol': app.playerCol
    })

    # if there is a block in the way
    if app.board[newRow][newCol] in 'rgbvc':
        # illegal move
        if not isValidMove(app, beyondRow, beyondCol) or app.board[beyondRow][beyondCol] != '-':
            app.moveHistory.pop() 
            return
        app.board[beyondRow][beyondCol] = app.board[newRow][newCol]
        app.board[newRow][newCol] = '-'

    app.board[app.playerRow][app.playerCol] = '-'
    app.playerRow, app.playerCol = newRow, newCol
    app.board[app.playerRow][app.playerCol] = 'p'

def hardcodedLevel(app):
    # hardcoded "one move off" map for Level 1
    if app.currentLevel == 0:
        app.board = [
            [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
            [ '-', '-', '-', '-', 'w', 'w', 'w', 'r', 'r', 'w' ],
            [ '-', '-', '-', '-', 'w', 'p', 'g', '-', 'b', 'w' ],
            [ '-', '-', '-', '-', 'w', '-', '-', 'r', 'r', 'w' ],
            [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
            [ 'w', '-', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
            [ 'w', 'w', '-', '-', '-', '-', '-', '-', '-', 'w' ],
            [ '-', 'w', '-', '-', '-', '-', '-', 'w', '-', 'w' ],
            [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
            [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ]
        ]
        app.targets = [
            [ '-', '-', '-', '-', '-', '-', '-', '-', '-', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', 'r', 'r', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', 'g', 'b', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', 'r', 'r', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', '-', '-', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', '-', '-', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', '-', '-', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', '-', '-', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', '-', '-', '-' ],
            [ '-', '-', '-', '-', '-', '-', '-', '-', '-', '-' ]
        ]
        app.playerRow, app.playerCol = 2, 5
        app.won = False
        app.moveHistory = []

def getDirections(direction):
    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    return directions[direction]

def isValidMove(app, row, col):
    return 0 <= row < len(app.board) and 0 <= col < len(app.board[0]) and app.board[row][col] != 'w'

def undoLastMove(app):
    # undo the last move by reverting to the previous state
    if app.moveHistory:
        lastState = app.moveHistory.pop()
        app.board = lastState['board']
        app.playerRow = lastState['playerRow']
        app.playerCol = lastState['playerCol']
        app.won = False

def checkWinCondition(app):
    # check if all color blocks are on their respective target blocks
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            if app.targets[row][col] in 'rgbvc' and app.board[row][col] != app.targets[row][col]:
                return 
    app.won = True

def redrawAll(app):
    drawTitleAndInstructions()
    drawGameBoard(app)
    if app.won:
        # win messsage
        drawRect(100, 300, 400, 100, fill='white', border='black', 
                    borderWidth=3)
        drawLabel('You Win!', 300, 350, size=40, bold=True, 
                    fill='green', align='center')

def drawGameBoard(app):
    drawBackground(app)
    drawBoard(app)
    drawTargets(app)
    drawPlayer(app)

def drawBackground(app):
    backgroundColor = 'lightGreen' if app.won else 'white'
    drawRect(0, 100, 600, 500, fill=backgroundColor) 

def drawBoard(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            drawCell(app, row, col)

def drawTargets(app):
    for row in range(len(app.targets)):
        for col in range(len(app.targets[row])):
            if app.targets[row][col] != '-':
                drawTarget(app, row, col)

def drawCell(app, row, col):
    cell = app.board[row][col]
    x = app.xOffset + col * app.cellSize
    y = app.yOffset + row * app.cellSize
    if cell == '-':
        return
    if cell == 'w':
        drawRect(x, y, app.cellSize, app.cellSize, fill='darkGoldenrod')
    elif cell in 'rgbvc':
        # draws color blocks with empty (white) star in the middle
        color = getColor(cell)
        drawRect(x, y, app.cellSize, app.cellSize, fill=color)
        drawStar(x + app.cellSize // 2, y + app.cellSize // 2, 
                    app.cellSize // 4, 5, fill='white')

def drawTarget(app, row, col):
    color = getColor(app.targets[row][col])
    x = app.xOffset + col * app.cellSize
    y = app.yOffset + row * app.cellSize
    drawStar(x + app.cellSize // 2, y + app.cellSize // 2, 
                app.cellSize // 4, 5, fill=color)

def drawPlayer(app):
    x = app.xOffset + app.playerCol * app.cellSize
    y = app.yOffset + app.playerRow * app.cellSize
    drawCircle(x + app.cellSize // 2, y + app.cellSize // 2, 
                app.cellSize // 3, fill='black')

def drawTitleAndInstructions():
    drawLabel('Sokoban!', 300, 20, size=30, bold=True, align='center')
    drawLabel('Use arrow keys to solve the puzzle', 300, 50, size=15, 
                align='center')
    drawLabel('Press u to undo moves, r to reset level', 300, 70, size=15, 
                align='center')
    drawLabel('Press 1-4 to choose levels, press a to make level 1 almost solved'
                , 300, 90, size=15, align='center')
    drawLine(0, 100, 600, 100, fill='black', lineWidth=2)

def getColor(cell):
    # map cell characters to colors
    colorMapping = {
        # color blocks
        'r': 'fireBrick', 
        'g': 'oliveDrab', 
        'b': 'royalBlue', 
        'v': 'darkMagenta', 
        'c': 'mediumTurquoise',
        # target blocks
        'R': 'fireBrick', 
        'G': 'oliveDrab', 
        'B': 'royalBlue', 
        'V': 'darkMagenta', 
        'C': 'mediumTurquoise'
    }
    return colorMapping[cell]

runApp(600, 600)