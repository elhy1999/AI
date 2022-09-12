from queue import PriorityQueue
import sys

### IMPORTANT: Remove any #kmslol) functions or rename any functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any function.

# Helper functions to aid in your implementation. Can edit/remove

class myPQ:
    
    def __init__(self, pq = None):
        if pq == None:
            self.pq = PriorityQueue()
            self.items = {}
        else:
            self.items = {}
            self.pq = PriorityQueue()
            while not pq.empty():
                self.items[pq.get()] = 0
            for i in self.items:
                self.pq.put(i)
            
    def clone(self):
        newPQ = myPQ()
        for i in self.items:
            newPQ = newPQ.put(i)
        return newPQ
    
    def put(self, item):
        pq = PriorityQueue()
        for i in self.items:
            pq.put(i)
        pq.put(item)
        return myPQ(pq)

    def get(self):
        copy = self.clone()
        item = copy.pq.get()
        copy.items.pop(item)
        return item, copy

    def empty(self):
        return self.size() == 0

    def __str__(self):
        return str(self.items.keys())

    def size(self):
        return len(self.items)

class Piece:
 
    printMapping = {"king" : "K", 
    "knight" : "N", 
    "obstacle" : "X", 
    "queen" : "Q",
    "bishop" : "B",
    "rook" : "R"}

    scoreMapping = {"queen" : 1,
        "rook" : 2,
        "bishop" : 3,
        "king" : 4,
        "knight" : 5}

    numPieces = 0
 
    def __init__(self, type):
        self.type = type
        self.id = Piece.numPieces
        Piece.numPieces += 1
 
    def getType(self):
        return self.type

    def getPriority(self):
        return Piece.scoreMapping[self.getType()]

    def getPrintMapping(self):
        return f" {Piece.printMapping[self.getType()]} |"
 
    def __str__(self):
        return f"{self.getType()}  "
 
    def __hash__(self):
        return self.scoreMapping[self.getType()]


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
        return square.getCoord() == self.getCoord()
 
    def __hash__(self):
        return hash(self.__str__())

class Board:

    threateningSquares = {}
 
    def __init__(self, numRows, numCols, 
    possiblePositions, obstacles = None, 
    piecesPositionMapping = None, positionPiecesMapping = None):
        self.boardDim = (numRows, numCols)

        if (obstacles == None):
            self.obstacles = {}
        else:
            self.obstacles = obstacles # Piece Square object: Piece object

        self.possiblePositions = possiblePositions # {Square object : 0}

        if (piecesPositionMapping == None):
            self.piecesPositionMapping = {} # Piece object : Square object, for confirmed pieces
            self.positionPiecesMapping = {} # Square object : Piece object, for confirmed pieces
        else:
            self.piecesPositionMapping = piecesPositionMapping
            self.positionPiecesMapping = positionPiecesMapping

    def getDim(self):
        return self.boardDim

    def placePiece(self, piece, square):
        """Returns a new Board object with the piece assigned"""
        threateningSquares = self.getThreateningSquares(piece, square)

        newPiecesPositionMapping = self.piecesPositionMapping.copy()
        newPiecesPositionMapping[piece] = square

        newPositionPiecesMapping = self.positionPiecesMapping.copy()
        newPositionPiecesMapping[square] = piece
        
        newPossiblePositions = self.possiblePositions.copy()

        for s in threateningSquares:
            if s in newPossiblePositions:
                newPossiblePositions.pop(s)


        return Board(self.boardDim[0], self.boardDim[1],
            newPossiblePositions,
            self.obstacles,
            newPiecesPositionMapping,
            newPositionPiecesMapping)

    def getThreateningSquares(self, piece, startSquare):
        """Returns a list of Square objects which are threatened by piece"""

        if (piece.getType(), startSquare) in Board.threateningSquares:
            return Board.threateningSquares[(piece.getType(), startSquare)]

        type = piece.getType()
 
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
 
        Board.threateningSquares[(piece.getType(), startSquare)] = threatening

        return threatening

    def getNumPossiblePositions(self):
        return len(self.possiblePositions)

    def printState(self):
        return str(sorted([(piece.getType(), s.getCoord()) for piece, s in self.piecesPositionMapping.items()]))

    def __str__(self):
        numRows = self.getDim()[0]
        numCols = self.getDim()[1]
        board = [["   |" for i in range(numCols)] for j in range(numRows)]
 
        for square, piece in self.obstacles.items():
            position = square.getCoord()
            file = int(position[1:])
            rank = ord(position[0]) - 97
            board[file][rank] = piece.getPrintMapping()
 
        for piece, square in self.piecesPositionMapping.items():
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

    def __eq__(self, b): # Redo
        if type(b) != type(self):
            return False
        return self.boardDim == b.boardDim and\
            self.numThreatenedPieces == b.numThreatenedPieces and\
                self.obstacles == b.obstacles and\
                    self.piecesPositionMapping == b.piecesPositionMapping and\
                        self.positionPiecesMapping == b.positionPiecesMapping and\
                            self.threatenedPieces == b.threatenedPieces

    def __hash__(self):
        return hash(self.__str__())

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    f = open(testfile, "r").read()

    def generateCoords(numRows, numCols):
        possibleSquares = {}
        for i in range(numRows):
            for j in range(numCols):
                coord = str(chr(97 + i)) + str(j)
                square = Square(coord, (numRows, numCols))
                possibleSquares[square] = 0
        return possibleSquares

    def process(file):
        information = {}
        inputLines = file.split('\n')
        for i, line in enumerate(inputLines):
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
                if "-" in line:
                    information["obstacles"] = {}
                    continue
                coords = line[38:].split(" ")
                obstacles = {}
                if coords[0] != "":
                    for coord in coords:
                        square = Square(coord, (information["rows"], information["cols"]))
                        obstacles[square] = Piece('obstacle')
                information["obstacles"] = obstacles
            elif "Number of King, Queen, Bishop, Rook, Knight (space between):" in line:
                nums_str = line[60:]
                nums_pieces = nums_str.split(" ")
                nums_pieces = [int(i) for i in nums_pieces]

                information['possiblePositionsMapping'] = generateCoords(information["rows"], information["cols"])
                for s in information['obstacles']:
                    information['possiblePositionsMapping'].pop(s)

                information['exploredSquares'] = {}

                pq = myPQ()
                information['numKings'] = nums_pieces[0]
                for i in range(information['numKings']):
                    piece = Piece("king")
                    pq = pq.put((piece.getPriority(), piece.id, piece))
                    information['exploredSquares'][piece] = {}
                
                information['numQueens'] = nums_pieces[1]
                for i in range(information['numQueens']):
                    piece = Piece("queen")
                    pq = pq.put((piece.getPriority(), piece.id, piece))
                    information['exploredSquares'][piece] = {}
                
                information['numBishops'] = nums_pieces[2]
                for i in range(information['numBishops']):
                    piece = Piece("bishop")
                    pq = pq.put((piece.getPriority(), piece.id, piece))
                    information['exploredSquares'][piece] = {}
                
                information['numRooks'] = nums_pieces[3]
                for i in range(information['numRooks']):
                    piece = Piece("rook")
                    pq = pq.put((piece.getPriority(), piece.id, piece))
                    information['exploredSquares'][piece] = {}
                
                information['numKnights'] = nums_pieces[4]
                for i in range(information['numKnights']):
                    piece = Piece("knight")
                    pq = pq.put((piece.getPriority(), piece.id, piece))
                    information['exploredSquares'][piece] = {}
                
                information['unassignedPieces'] = pq

        return information

    exploredBoards = {}

    def backtrack(currBoard, unassignedPieces):
        state = currBoard.printState()
        if state in exploredBoards and state != "[]":
            return False
        
        exploredBoards[state] = 0
        
        if unassignedPieces.size() == 0:
            return currBoard
        bestPiece, newUnassignedPieces = unassignedPieces.get()
        bestPiece = bestPiece[-1]
        for square in currBoard.possiblePositions:
            if square in information['exploredSquares'][bestPiece]: # Cannot place bestPiece on threatened square
                continue
            
            threateningSquares = currBoard.getThreateningSquares(bestPiece, square) # Cannot place bestPiece on square that threatens existing piece
            toContinue = False
            for s in threateningSquares:
                if s in currBoard.positionPiecesMapping:
                    toContinue = True
            if toContinue:
                continue
            
            newBoard = currBoard.placePiece(bestPiece, square)
            
            information['exploredSquares'][bestPiece][square] = 0 ## 
            inferences = len(newBoard.possiblePositions) >= newUnassignedPieces.size()
            
            
            if inferences != False:
                result = backtrack(newBoard, newUnassignedPieces)
                if result != False: return result
                
            information['exploredSquares'][bestPiece].pop(square)
        return False

    def capitalize(string):
        """Returns a string with the first letter capitalized"""
        return string[0].upper() + string[1:]

    information = process(f)
    b0 = Board(information['rows'],
        information['cols'],
        information['possiblePositionsMapping'],
        information['obstacles'])

    
    result = backtrack(b0, information['unassignedPieces'])
    
    result_piece_coord = [((positioning.getCoord()[0], int(positioning.getCoord()[1:])), capitalize(piece.getType())) \
        for piece, positioning in result.piecesPositionMapping.items()]

    #kmslolt2 - t1)
    return dict(result_piece_coord)


    # #kmslolresult)
#kmslolrun_CSP())