import sys
import time
from queue import Queue
 
t1 = time.time()
 
class Frontier:
    def __init__(self):
        self.q = Queue()
 
    def enqueue(self, element):
        self.q.put(element)
 
    def dequeue(self):
        return self.q.get()
 
    def size(self):
        return self.q.qsize()
 
    def isEmpty(self):
        return self.q.empty()
 
class Frontier2:
    def __init__(self):
        self.q = {}
        self.head = 0
        self.tail = 0
 
    def enqueue(self, element):
        self.q[self.tail] = element
        self.tail += 1
 
    def dequeue(self):
        toReturn = self.q[self.head]
        self.q.pop(self.head)
        self.head += 1
        return toReturn
 
    def size(self):
        return self.tail - self.head + 1
 
    def isEmpty(self):
        return self.size() == 0
 
class Piece:
 
    printMapping = {"king" : "K", 
    "knight" : "N", 
    "obstacle" : "X", 
    "queen" : "Q",
    "bishop" : "B",
    "rook" : "R"}
 
    def __init__(self, type, team = None):
        self.type = type
        self.team = team     
 
    def getType(self):
        return self.type
 
    def getTeam(self):
        return self.team
 
    def getPrintMapping(self):
        if self.getTeam() == "enemy":
            return f" E{Piece.printMapping[self.getType()]}|"
        elif self.getTeam() == "friendly":
            return f" F{Piece.printMapping[self.getType()]}|"
        else:
            return f" {Piece.printMapping[self.getType()]} |"
 
    def __str__(self):
        return f"{self.getType()} {self.getTeam()}"
 
class Square:
    
    def __init__(self, position, boardDim):
        self.file = position[0]
        self.rank = position[1:]
        self.boardDim = boardDim
    
    def clone(self):
        return Square(self.file + self.rank, self.getBoardDim)
 
    def goLeft(self):
        currX = ord(self.file) - 97
        newPosition = chr(currX - 1 + 97) + self.rank
        return Square(newPosition, self.getBoardDim())
 
    def goRight(self):
        currX = ord(self.file) - 97
        newPosition = chr(currX + 1 + 97) + self.rank
        return Square(newPosition, self.getBoardDim())
 
    def goUp(self):
        currY = int(self.rank)
        newPosition = self.file + str(currY - 1)
        return Square(newPosition, self.getBoardDim())
 
    def goDown(self):
        currY = int(self.rank)
        newPosition = self.file + str(currY + 1)
        return Square(newPosition, self.getBoardDim())
 
    def go(self, direction):
        if type(direction) == list and len(direction) == 0:
            return self
        elif type(direction) == list:
            return self.go(direction[0]).go(direction[1:])
        else:
            if direction == "up":
                return self.goUp()
            elif direction == "down":
                return self.goDown()
            elif direction == "left":
                return self.goLeft()
            elif direction == "right":
                return self.goRight()
            elif direction == "up-right":
                return self.goUp().goRight()
            elif direction == "up-left":
                return self.goUp().goLeft()
            elif direction == "down-right":
                return self.goDown().goRight()
            elif direction == "down-left":
                return self.goDown().goLeft()
            else:
                raise Exception("Square: invalid direction")
 
    def getBoardDim(self):
        return self.boardDim
 
    def isValid(self):
        colCheck = (0 <= ord(self.file) - 97 < self.getBoardDim()[1])
        rowCheck = (0 <= int(self.rank) < self.getBoardDim()[0])
        return colCheck and rowCheck
 
    def getCoord(self):
        return self.file + self.rank
 
    def __str__(self):
        return self.getCoord()
 
    def __eq__(self, square):
        if (not isinstance(square, Square)):
            raise Exception("Square: square is not of object type Square")
        return square.getCoord() == self.getCoord()
 
    def __hash__(self):
        return hash(self.__str__())
 
class Board:
 
    def __init__(self, numRows, numCols, kingPosition, obstacles = None, enemyPieces = None, friendlyPieces = None, king = None, threatenedSquares = None):
        self.boardDim = (numRows, numCols)
        self.kingPosition = kingPosition
        if (obstacles == None):
            self.obstacles = {}
        else:
            self.obstacles = obstacles # Piece Square object: Piece object
 
        if (enemyPieces == None):
            self.enemyPieces = {}
        else:
            self.enemyPieces = enemyPieces # Piece Square object: Piece object
 
        if (friendlyPieces == None):
            self.friendlyPieces = {}
        else:
            self.friendlyPieces = friendlyPieces # Piece Square object: Piece object
 
        if (threatenedSquares == None):
            self.threatenedSquares = {}
        else:
            self.threatenedSquares = threatenedSquares # Piece Square object: Piece object
 
        if (king == None): # if no king, put king there
            self.king = Piece("king", "friendly")
            self.friendlyPieces[self.king] = self.kingPosition
            self.obstacles[kingPosition] = self.king
        else:
            self.king = king
 
 
    def getDim(self):
        return self.boardDim
 
    def getKing(self):
        return self.king
 
    def placePiece(self, piece, square):
        """Returns a new Board with piece placed on it"""
        if (not isinstance(piece, Piece)):
            raise Exception("Board: piece is not of object type Piece")
        elif (not isinstance(square, Square)):
            raise Exception("Board: square is not of object type Square")
        elif (not square.isValid()):
            raise Exception("Board: invalid Square")
        elif (piece in self.obstacles) or (piece in self.enemyPieces) or (piece in self.friendlyPieces):
            raise Exception("Board: piece is already on board")
 
        team = piece.getTeam()
        if team == "enemy":
            newEnemyPieces = self.enemyPieces.copy()
            newEnemyPieces[piece] = square
            newObstacles = self.obstacles.copy()
            newObstacles[square] = piece
            newThreatenedSquares = self.threatenedSquares.copy()
            for s in self.getThreateningSquares(piece, square):
                newThreatenedSquares[s] = piece
            
            return Board(numRows = self.boardDim[0],
            numCols = self.boardDim[1],
            kingPosition = self.kingPosition,
            obstacles = newObstacles,
            enemyPieces = newEnemyPieces,
            friendlyPieces = self.friendlyPieces,
            king = self.getKing(),
            threatenedSquares = newThreatenedSquares)
        elif team == "friendly":
            cloned = self.friendlyPieces.copy()
            cloned[piece] = square
            cloned2 = self.obstacles.copy()
            cloned2[square] = piece
 
            return Board(self.boardDim[0],
            self.boardDim[1],
            self.kingPosition,
            cloned2,
            self.enemyPieces,
            cloned,
            self.getKing(),
            self.threatenedSquares)
        else:
            cloned = self.obstacles.copy()
            cloned[square] = piece
            return Board(self.boardDim[0],
            self.boardDim[1],
            self.kingPosition,
            cloned,
            self.enemyPieces,
            self.friendlyPieces,
            self.threatenedSquares,
            self.getKing())
 
    def movePiece(self, piece, square): # Unable to move enemy pieces
        """Returns a new Board after piece is moved"""
        if (not isinstance(piece, Piece)):
            raise Exception("Board: piece is not of object type Piece")
        elif (not isinstance(square, Square)):
            raise Exception("Board: square is not of object type Square")
        elif (not square.isValid()):
            raise Exception("Board: invalid Square")
        elif (not piece in self.obstacles) and (not piece in self.enemyPieces) and (not piece in self.friendlyPieces):
            raise Exception("Board: piece is not on board")
 
        kingPos = self.getKingPosition()
        if self.getKing() == piece:
            kingPos = square
        else:
            kingPos = self.kingPosition
 
        team = piece.getTeam()
        if team == "enemy":
            cloned = self.enemyPieces.copy()
            cloned.pop(piece)
            cloned[piece] = square
            cloned2 = self.obstacles.copy()
            cloned2.pop(self.enemyPieces[piece])
            cloned2[square] = piece
            return Board(self.boardDim[0],
            self.boardDim[1],
            kingPos,
            cloned2,
            cloned,
            self.friendlyPieces)
        elif team == "friendly":
            cloned = self.friendlyPieces.copy()
            cloned.pop(piece)
            cloned[piece] = square
            cloned2 = self.obstacles.copy()
            cloned2.pop(self.friendlyPieces[piece])
            cloned2[square] = piece
            return Board(self.boardDim[0],
            self.boardDim[1],
            kingPos,
            cloned2,
            self.enemyPieces,
            cloned)
        else:
            cloned = self.obstacles.copy()
            cloned.pop(piece)
            cloned[piece] = square
            return Board(self.boardDim[0],
            self.boardDim[1],
            kingPos,
            cloned,
            self.enemyPieces,
            self.friendlyPieces)
 
    def moveKing(self, direction):
        kingPos = self.getKingPosition()
        square = kingPos.go(direction)
        # if (not isinstance(square, Square)):
        #     raise Exception("Board: square is not of object type Square")
        # elif (not square.isValid()):
        #     raise Exception("Board: invalid Square")
        # elif (not square in self.getThreateningSquares(self.king, self.getKingPosition())) or (not self.isSafeSquare(square)):
        #     raise Exception("Board: king cannot go there")
 
        newFriendlyPieces = self.friendlyPieces.copy()
        newFriendlyPieces.pop(self.getKing())
        newFriendlyPieces[self.getKing()] = square
        newObstacles = self.obstacles.copy()
        newObstacles.pop(self.getKingPosition())
        newObstacles[square] = self.king
        return Board(self.boardDim[0], self.boardDim[1],
            square,
            newObstacles,
            self.enemyPieces,
            newFriendlyPieces,
            king = self.getKing(),
            threatenedSquares = self.threatenedSquares)
 
    def canGo(self, direction):
        kingPos = self.getKingPosition()
        square = kingPos.go(direction)
 
        if (not isinstance(square, Square)):
            raise Exception("Board: square is not of object type Square")
        elif (not square.isValid()):
            return False
        
        return self.isSafeSquare(square)
 
    def getThreateningSquares(self, piece, startSquare):
        """Returns a list of Square objects which are threatened by piece"""
        type = piece.getType()
        team = piece.getTeam()
        """ if team == "enemy":
            startSquare = self.enemyPieces[piece]
        elif team == "friendly":
            startSquare = self.friendlyPieces[piece]
        else:
            startSquare = self.obstacles[piece] """
 
        threatening = [startSquare]
        if type == "obstacle":
            return threatening
        elif type == "king":
            if (startSquare.goLeft().isValid()): 
                threatening.append(startSquare.goLeft())
            if (startSquare.goLeft().goUp().isValid()): 
                threatening.append(startSquare.goLeft().goUp())
            if (startSquare.goUp().isValid()): 
                threatening.append(startSquare.goUp())
            if (startSquare.goUp().goRight().isValid()): 
                threatening.append(startSquare.goUp().goRight())
            if (startSquare.goRight().isValid()): 
                threatening.append(startSquare.goRight())
            if (startSquare.goRight().goDown().isValid()): 
                threatening.append(startSquare.goRight().goDown())
            if (startSquare.goDown().isValid()): 
                threatening.append(startSquare.goDown())
            if (startSquare.goDown().goLeft().isValid()): 
                threatening.append(startSquare.goDown().goLeft())
        elif type == "knight":
            if (startSquare.goLeft().goLeft().goUp().isValid()): 
                threatening.append(startSquare.goLeft().goLeft().goUp())
            if (startSquare.goLeft().goUp().goUp().isValid()): 
                threatening.append(startSquare.goLeft().goUp().goUp())
            if (startSquare.goUp().goUp().goRight().isValid()): 
                threatening.append(startSquare.goUp().goUp().goRight())
            if (startSquare.goUp().goRight().goRight().isValid()): 
                threatening.append(startSquare.goUp().goRight().goRight())
            if (startSquare.goRight().goRight().goDown().isValid()): 
                threatening.append(startSquare.goRight().goRight().goDown())
            if (startSquare.goRight().goDown().goDown().isValid()): 
                threatening.append(startSquare.goRight().goDown().goDown())
            if (startSquare.goDown().goDown().goLeft().isValid()): 
                threatening.append(startSquare.goDown().goDown().goLeft())
            if (startSquare.goDown().goLeft().goLeft().isValid()): 
                threatening.append(startSquare.goDown().goLeft().goLeft())
        elif type == "rook":
            # Go UP
            currSquare = startSquare
            while (currSquare.goUp().isValid()) and not ((currSquare.goUp() in self.obstacles)):
                currSquare = currSquare.goUp()
                threatening.append(currSquare.clone())
            # Go DOWN
            currSquare = startSquare
            while (currSquare.goDown().isValid() and not (currSquare.goDown() in self.obstacles)):
                currSquare = currSquare.goDown()
                threatening.append(currSquare.clone())
            # Go LEFT
            currSquare = startSquare
            while (currSquare.goLeft().isValid() and not (currSquare.goLeft() in self.obstacles)):
                currSquare = currSquare.goLeft()
                threatening.append(currSquare.clone())
            # Go RIGHT
            currSquare = startSquare
            while (currSquare.goRight().isValid() and not (currSquare.goRight() in self.obstacles)):
                currSquare = currSquare.goRight()
                threatening.append(currSquare.clone())
        elif type == "bishop":
            # Go UPLEFT
            currSquare = startSquare
            while (currSquare.goUp().goLeft().isValid()) and not ((currSquare.goUp().goLeft() in self.obstacles)):
                currSquare = currSquare.goUp().goLeft()
                threatening.append(currSquare.clone())
            # Go DOWNLEFT
            currSquare = startSquare
            while (currSquare.goDown().goLeft().isValid() and not (currSquare.goDown().goLeft() in self.obstacles)):
                currSquare = currSquare.goDown().goLeft()
                threatening.append(currSquare.clone())
            # Go UPRIGHT
            currSquare = startSquare
            while (currSquare.goUp().goRight().isValid() and not (currSquare.goUp().goRight() in self.obstacles)):
                currSquare = currSquare.goUp().goRight()
                threatening.append(currSquare.clone())
            # Go DOWNRIGHT
            currSquare = startSquare
            while (currSquare.goDown().goRight().isValid() and not (currSquare.goDown().goRight() in self.obstacles)):
                currSquare = currSquare.goDown().goRight()
                threatening.append(currSquare.clone())
        elif type == "queen":
            # Go UP
            currSquare = startSquare
            while (currSquare.goUp().isValid()) and not ((currSquare.goUp() in self.obstacles)):
                currSquare = currSquare.goUp()
                threatening.append(currSquare.clone())
            # Go DOWN
            currSquare = startSquare
            while (currSquare.goDown().isValid() and not (currSquare.goDown() in self.obstacles)):
                currSquare = currSquare.goDown()
                threatening.append(currSquare.clone())
            # Go LEFT
            currSquare = startSquare
            while (currSquare.goLeft().isValid() and not (currSquare.goLeft() in self.obstacles)):
                currSquare = currSquare.goLeft()
                threatening.append(currSquare.clone())
            # Go RIGHT
            currSquare = startSquare
            while (currSquare.goRight().isValid() and not (currSquare.goRight() in self.obstacles)):
                currSquare = currSquare.goRight()
                threatening.append(currSquare.clone())
            # Go UPLEFT
            currSquare = startSquare
            while (currSquare.goUp().goLeft().isValid()) and not ((currSquare.goUp().goLeft() in self.obstacles)):
                currSquare = currSquare.goUp().goLeft()
                threatening.append(currSquare.clone())
            # Go DOWNLEFT
            currSquare = startSquare
            while (currSquare.goDown().goLeft().isValid() and not (currSquare.goDown().goLeft() in self.obstacles)):
                currSquare = currSquare.goDown().goLeft()
                threatening.append(currSquare.clone())
            # Go UPRIGHT
            currSquare = startSquare
            while (currSquare.goUp().goRight().isValid() and not (currSquare.goUp().goRight() in self.obstacles)):
                currSquare = currSquare.goUp().goRight()
                threatening.append(currSquare.clone())
            # Go DOWNRIGHT
            currSquare = startSquare
            while (currSquare.goDown().goRight().isValid() and not (currSquare.goDown().goRight() in self.obstacles)):
                currSquare = currSquare.goDown().goRight()
                threatening.append(currSquare.clone())
 
        return threatening
        
    def isSafeSquare(self, square):
        if (not isinstance(square, Square)):
            raise Exception("Board: square is not of object type Square")
        elif (not square.isValid()):
            raise Exception("Board: invalid Square")
        return (not (square in self.threatenedSquares)) and (not (square in self.obstacles))
 
    def getKingPosition(self):
        return self.kingPosition
 
    def __str__(self):
        numRows = self.getDim()[0]
        numCols = self.getDim()[1]
        board = [["   |" for i in range(numCols)] for j in range(numRows)]
 
        for square, piece in self.obstacles.items():
            position = square.getCoord()
            file = int(position[1:])
            rank = ord(position[0]) - 97
            board[file][rank] = piece.getPrintMapping()
 
        for piece, square in self.enemyPieces.items():
            position = square.getCoord()
            file = int(position[1:])
            rank = ord(position[0]) - 97
            board[file][rank] = piece.getPrintMapping()
 
        for piece, square in self.friendlyPieces.items():
            position = square.getCoord()
            file = int(position[1:])
            rank = ord(position[0]) - 97
            board[file][rank] = piece.getPrintMapping()
 
        string = ""
        for i, row in enumerate(board):
            for j, ele in enumerate(row):
                string += str(ele)
            string += "\n" + "----" * numCols + "\n"
        return string
 
    def __eq__(self, b):
        return self.boardDim == b.boardDim and\
            self.kingPosition == b.kingPosition and\
                self.obstacles == b.obstacles and\
                    self.enemyPieces == b.enemyPieces and\
                        self.friendlyPieces == b.friendlyPieces
 
    def __hash__(self):
        return hash(self.__str__())
 
class Node:
 
    def __init__(self, board, parent = None, pathCost = 0, depth = 0):
        self.board = board
        self.parent = parent
        self.pathCost = pathCost
        self.depth = depth
 
    def getBoard(self):
        return self.board
 
    def getKingPosition(self):
        return self.board.getKingPosition()
    
    def getCurrPathCost(self):
        return self.pathCost
 
    def getParent(self):
        return self.parent
    
    def getDepth(self):
        return self.depth
 
    def __str__(self):
        if (self.getParent()):
            p = self.getParent().getKingPosition()
        else:
            p = None
        return f"""My Board:
{self.getBoard()}
        Parent: {p}
        King Position: {self.getKingPosition()}
        Curr PathCost: {self.getCurrPathCost()}
        Depth: {self.getDepth()}
 
        """
        
 
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type
    information = {}
 
    def process(i, line, inputLines):
        if "Rows:" in line:
            numRows = int(line[5:])
            information["rows"] = numRows
        elif "Cols:" in line:
            numCols = int(line[5:])
            information["cols"] = numCols
        elif "Number of Obstacles:" in line:
            numObstacles = int(line[20:])
            information["numObstacles"] = numObstacles
        elif "Position of Obstacles (space between):" in line:
            coords = line[38:].split(" ")
            obstacles = {}
            if coords[0] != "":
                for coord in coords:
                    square = Square(coord, (information["rows"], information["cols"]))
                    obstacles[square] = Piece('obstacle')
            information["obstacles"] = obstacles
        elif "Step cost to move to selected grids (Default cost is 1) [Pos, Cost]:" in line:
            if "costs" not in information:
                information["costs"] = {}
            if "-" in line:
                return
            else:
                startIndex = i + 1
                while (inputLines[startIndex][0] == '['):
                    currLine = inputLines[startIndex][1:-1].split(",")
                    square = currLine[0]
                    cost = int(currLine[1])
                    information["costs"][square] = cost
                    startIndex += 1
        elif "Position of Enemy Pieces:" in line:
            if "enemyPieces" not in information:
                information["enemyPieces"] = {}
            if "-" in line:
                return
            else:
                startIndex = i + 1
                while (inputLines[startIndex][0] == '['):
                    currLine = inputLines[startIndex][1:-1].split(",")
                    pieceName = currLine[0]
                    if (pieceName == "King"):
                        piece = Piece("king", "enemy")
                    elif (pieceName == "Bishop"):
                        piece = Piece("bishop", "enemy")
                    elif (pieceName == "Rook"):
                        piece = Piece("rook", "enemy")
                    elif (pieceName == "Queen"):
                        piece = Piece("queen", "enemy")
                    else:
                        piece = Piece("knight", "enemy")
                    position = currLine[1]
                    square = Square(position, (information["rows"], information["cols"]))
                    information["enemyPieces"][piece] = square
                    startIndex += 1
        elif "Starting Position of Pieces [Piece, Pos]:" in line:
            if "friendlyPieces" not in information:
                information["friendlyPieces"] = {}
            if "-" in line:
                return
            else:
                startIndex = i + 1
                while (inputLines[startIndex][0] == '['):
                    currLine = inputLines[startIndex][1:-1].split(",")
                    pieceName = currLine[0]
                    if (pieceName == "King"):
                        piece = Piece("king", "friendly")
                        information["kingPosition"] = Square(currLine[1], (information["rows"], information["cols"]))
                    elif (pieceName == "Bishop"):
                        piece = Piece("bishop", "friendly")
                    elif (pieceName == "Rook"):
                        piece = Piece("rook", "friendly")
                    elif (pieceName == "Queen"):
                        piece = Piece("queen", "friendly")
                    else:
                        piece = Piece("knight", "friendly")
                    position = currLine[1]
                    square = Square(position, (information["rows"], information["cols"]))
                    # print(f"SQUARE: {square}")
 
                    information["friendlyPieces"][piece] = square
                    startIndex += 1
        elif "Goal Positions (space between):" in line:
            goals = line[31:].split(" ")
            information["goals"] = goals
    
    def actions(board):
        possibleActions = ['right', 'left', 'up', 'down', 'up-right', 'up-left', 'down-right', 'down-left']
        validActions = []
        for action in possibleActions:
            if board.canGo(action):
                validActions.append(action)
        return validActions
 
    def cost(goalBoard):
        kingPos = goalBoard.getKingPosition().getCoord()
        if kingPos in information["costs"]:
            return information["costs"][kingPos]
        else:
            return 1
 
    def t(fromBoard, action):
        return fromBoard.moveKing(action)
 
    def euclidean(board): # Heuristic, not run in BFS
        kingPos = board.getKingPosition().getCoord()
        xKingPos = ord(kingPos[0]) - 97
        yKingPos = int(kingPos[1:])
 
        def dist(tup1, tup2):
            return ((tup1[0]-tup2[0])**2 + (tup1[1]-tup2[1])**2) ** 0.5
 
        return min([dist((xKingPos, yKingPos), (ord(g[0]) - 97, int(g[1:]))) for g in information["goals"]])
 
    def isGoal(node):
        return node.getKingPosition().getCoord() in information["goals"]
 
    def backtrack(endNode):
        actionsTaken = []
        totalPathCost = endNode.getCurrPathCost()
        curr = endNode
        while (curr.getParent()):
            fromPos = curr.getParent().getKingPosition().getCoord()
            toPos = curr.getKingPosition().getCoord()
            actionTaken = [(fromPos[0], int(fromPos[1:])), (toPos[0], int(toPos[1:]))]
            actionsTaken.insert(0, actionTaken)
            curr = curr.getParent()
 
        # actionTaken = (curr.getParent().getKingPosition().getCoord(), curr.getKingPosition().getCoord())
        # actionsTaken.insert(0, actionTaken)
 
        return actionsTaken, totalPathCost
 
    # Getting started, reading information
 
    t0 = time.time()
 
    filename = sys.argv[1]
    f = open(filename, "r")
    inputLines = f.read().split("\n")
    for i, line in enumerate(inputLines):
        process(i, line, inputLines)
 
    b0 = Board(information["rows"], 
    information["cols"], 
    information["kingPosition"], 
    obstacles = information["obstacles"], 
    king = None)
    for piece, square in information["enemyPieces"].items():
        b0 = b0.placePiece(piece, square)
    for piece, square in information["friendlyPieces"].items():
        if piece.getType() == "king" and piece.getTeam() == "friendly":
            continue
        b0 = b0.placePiece(piece, square)
 
    t1 = time.time()
    # Initializing the starting node
    n0 = Node(b0)
    frontier = Frontier()
    frontier.enqueue(n0)
    visited = {n0.getKingPosition() : 0}
    nodesExplored = 0
    t_1 = time.time()
    totalTime = 0
    
    while (not frontier.isEmpty()):
        currNode = frontier.dequeue()
        nodesExplored += 1
 
        if isGoal(currNode):
            actionsTaken, totalPathCost = backtrack(currNode)
            t2 = time.time()
            # print(t1 - t0, t2 - t1)
            # print(time.time() - t_1)
            # print(f"t__: {totalTime}")
            return actionsTaken, nodesExplored
 
        validActions = actions(currNode.getBoard())
        t = time.time()
 
        newBoards = []
        for a in validActions:
            newBoards.append(currNode.getBoard().moveKing(a))
        # newBoards = [currNode.getBoard().moveKing(a) for a in validActions] # Too slow
 
        t_ = time.time()
        for board in newBoards:
            if board.getKingPosition() in visited:
                continue
            actionCost = cost(board)
            newNode = Node(board,
                parent = currNode, 
                pathCost = actionCost + currNode.getCurrPathCost(), 
                depth = currNode.getDepth() + 1)
            g_n = newNode.getCurrPathCost()
            if (newNode.getKingPosition() not in visited):
                frontier.enqueue(newNode)
                visited[newNode.getKingPosition()] = newNode.getCurrPathCost()
        t__ = t_ - t
        totalTime += t__
 
 
    """ moves, nodesExplored, pathCost = search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned """
    t2 = time.time()
    # print(t1 - t0, t2 - t1)
    # print(time.time() - t_1)
    return [], nodesExplored
 
def backtrack(end):
    curr = end
    while (curr.getParent()):
        input()
        print(curr)
        curr = curr.getParent()
    input()
    print(curr)
 
def playGame(b0):
    def isValidMove(direction):
        return direction in ['right', 'left', 'up', 'down', 'up-right', 'up-left', 'down-right', 'down-left']
 
    while True:
        direction = input('direction: ')
        if isValidMove(direction) and b0.canGo(direction):
            b0 = b0.moveKing(direction)
            print(b0)
        else:
            print('invalid direction')
 
def euclid(coord): # Heuristic
    xKingPos = ord(coord[0]) - 97
    yKingPos = int(coord[1:])
    g = 'r4'
 
    def dist(tup1, tup2):
        return ((tup1[0]-tup2[0])**2 + (tup1[1]-tup2[1])**2) ** 0.5
 
    return dist((xKingPos, yKingPos), (ord(g[0]) - 97, int(g[1:])))
 
def readInfo():
 
    information = {}
    def process(i, line, inputLines):
        if "Rows:" in line:
            numRows = int(line[5:])
            information["rows"] = numRows
        elif "Cols:" in line:
            numCols = int(line[5:])
            information["cols"] = numCols
        elif "Number of Obstacles:" in line:
            numObstacles = int(line[20:])
            information["numObstacles"] = numObstacles
        elif "Position of Obstacles (space between):" in line:
            coords = line[38:].split(" ")
            obstacles = {}
            if coords[0] != "":
                for coord in coords:
                    square = Square(coord, (information["rows"], information["cols"]))
                    obstacles[square] = Piece('obstacle')
            information["obstacles"] = obstacles
        elif "Step cost to move to selected grids (Default cost is 1) [Pos, Cost]:" in line:
            if "costs" not in information:
                information["costs"] = {}
            if "-" in line:
                return
            else:
                startIndex = i + 1
                while (inputLines[startIndex][0] == '['):
                    currLine = inputLines[startIndex][1:-1].split(",")
                    square = currLine[0]
                    cost = int(currLine[1])
                    information["costs"][square] = cost
                    startIndex += 1
        elif "Position of Enemy Pieces:" in line:
            if "enemyPieces" not in information:
                information["enemyPieces"] = {}
            if "-" in line:
                return
            else:
                startIndex = i + 1
                while (inputLines[startIndex][0] == '['):
                    currLine = inputLines[startIndex][1:-1].split(",")
                    pieceName = currLine[0]
                    if (pieceName == "King"):
                        piece = Piece("king", "enemy")
                    elif (pieceName == "Bishop"):
                        piece = Piece("bishop", "enemy")
                    elif (pieceName == "Rook"):
                        piece = Piece("rook", "enemy")
                    elif (pieceName == "Queen"):
                        piece = Piece("queen", "enemy")
                    else:
                        piece = Piece("knight", "enemy")
                    position = currLine[1]
                    square = Square(position, (information["rows"], information["cols"]))
                    information["enemyPieces"][piece] = square
                    startIndex += 1
        elif "Starting Position of Pieces [Piece, Pos]:" in line:
            if "friendlyPieces" not in information:
                information["friendlyPieces"] = {}
            if "-" in line:
                return
            else:
                startIndex = i + 1
                while (inputLines[startIndex][0] == '['):
                    currLine = inputLines[startIndex][1:-1].split(",")
                    pieceName = currLine[0]
                    if (pieceName == "King"):
                        piece = Piece("king", "friendly")
                        information["kingPosition"] = Square(currLine[1], (information["rows"], information["cols"]))
                    elif (pieceName == "Bishop"):
                        piece = Piece("bishop", "friendly")
                    elif (pieceName == "Rook"):
                        piece = Piece("rook", "friendly")
                    elif (pieceName == "Queen"):
                        piece = Piece("queen", "friendly")
                    else:
                        piece = Piece("knight", "friendly")
                    position = currLine[1]
                    square = Square(position, (information["rows"], information["cols"]))
                    # print(f"SQUARE: {square}")
 
                    information["friendlyPieces"][piece] = square
                    startIndex += 1
        elif "Goal Positions (space between):" in line:
            goals = line[31:].split(" ")
            information["goals"] = goals
 
    filename = sys.argv[1]
    f = open(filename, "r")
    inputLines = f.read().split("\n")
    for i, line in enumerate(inputLines):
        process(i, line, inputLines)
 
    b0 = Board(information["rows"], 
    information["cols"], 
    information["kingPosition"], 
    obstacles = information["obstacles"],
    king = None)
    for piece, square in information["enemyPieces"].items():
        b0 = b0.placePiece(piece, square)
    for piece, square in information["friendlyPieces"].items():
        if piece.getType() == "king" and piece.getTeam() == "friendly":
            continue
        b0 = b0.placePiece(piece, square)
 
    return b0, information
 
# b0, information = readInfo()
 
# print(run_BFS())
# t2 = time.time()
# print(f"Code finished in {t2-t1} seconds")
 
 
 
def actions(board):
    possibleActions = ['right', 'left', 'up', 'down', 'up-right', 'up-left', 'down-right', 'down-left']
    validActions = []
    for action in possibleActions:
        if board.canGo(action):
            validActions.append(action)
    return validActions