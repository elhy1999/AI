import sys
import random

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
 
    printMapping = {"king" : "K", 
    "knight" : "N", 
    "obstacle" : "X", 
    "queen" : "Q",
    "bishop" : "B",
    "rook" : "R"}
 
    def __init__(self, type):
        self.type = type  
 
    def getType(self):
        return self.type
 
 
    def getPrintMapping(self):
        return f" {Piece.printMapping[self.getType()]} |"
 
    def __str__(self):
        return f"{self.getType()}  "
 
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
 
    def __init__(self, numRows, numCols, piecesPositionMapping, positionPiecesMapping = None, obstacles = None, threatenedPieces = None, beingThreatened = None, numThreatenedPieces = None):
        self.boardDim = (numRows, numCols)

        if (obstacles == None):
            self.obstacles = {}
        else:
            self.obstacles = obstacles # Piece Square object: Piece object
 
        self.piecesPositionMapping = piecesPositionMapping # Piece object: Square object

        if (positionPiecesMapping == None):
            self.positionPiecesMapping = {} # Square object : Piece object
            for p, s in piecesPositionMapping.items():
                self.positionPiecesMapping[s] = p
        else:
            self.positionPiecesMapping = positionPiecesMapping
 
        # One more attribute to store which piece is threatening me. To find best candidate to eliminate greedily

        if (threatenedPieces == None): # Only ran once when initiating first Board object
            self.numThreatenedPieces = 0
            self.threatenedPieces = {}
            self.beingThreatened = {} # ThreatenedPiece : {Threatening Pieces : 0}
            for threateningPiece, threateningPieceSquare in self.piecesPositionMapping.items():
                threatenedSquares = self.getThreateningSquares(threateningPiece, threateningPieceSquare)
                self.threatenedPieces[threateningPiece] = {}
                for square in threatenedSquares:
                    if not (square in self.positionPiecesMapping):
                        continue
                    threatenedPiece = self.positionPiecesMapping[square]
                    if threatenedPiece == threateningPiece: # Piece cannot threaten itself
                        continue
                    if not (threatenedPiece in self.beingThreatened): 
                        self.beingThreatened[threatenedPiece] = {}
                    self.beingThreatened[threatenedPiece][threateningPiece] = 0
                    self.threatenedPieces[threateningPiece][threatenedPiece] = 0
                    self.numThreatenedPieces += 1

        else:
            self.beingThreatened = beingThreatened
            self.numThreatenedPieces = numThreatenedPieces
            self.threatenedPieces = threatenedPieces # threateningPiece object : {threatenedPiece objects : 0}
 
 
    def getDim(self):
        return self.boardDim

    def getBestCandidatePiece(self, seed):
        random.seed(seed)
        piece_score_mapping = {}
        for piece, li in self.threatenedPieces.items():
            piece_score_mapping[piece] = len(li)
        for piece, li in self.beingThreatened.items():
            if not (piece in piece_score_mapping):
                piece_score_mapping[piece] = 0
            piece_score_mapping[piece] += len(li)

        bestPieces = []
        bestScore = 0
        for piece, score in piece_score_mapping.items():
            if score > bestScore:
                bestScore = score
                bestPieces = [piece]
            elif score == bestScore:
                bestPieces.append(piece)
        
        return random.choice(bestPieces)

    def getRandomCandidatePiece(self, seed):
        random.seed(seed)
        piece_score_mapping = {}
        all_pieces = []
        for piece, li in self.threatenedPieces.items():
            piece_score_mapping[piece] = len(li)
            all_pieces.append(piece)
        for piece, li in self.beingThreatened.items():
            if not (piece in piece_score_mapping):
                piece_score_mapping[piece] = 0
                all_pieces.append(piece)
            piece_score_mapping[piece] += len(li)
        
        chosenPiece = random.choice(all_pieces)
        while (piece_score_mapping[chosenPiece] == 0):
            chosenPiece = random.choice(all_pieces)
        
        return chosenPiece

    def removePiece(self, piece): # Unable to move enemy pieces
        """Returns a new Board after piece is removed"""

        newNumThreatenedPieces = self.numThreatenedPieces - len(self.threatenedPieces[piece])

        newPiecesPositionMapping = self.piecesPositionMapping.copy()
        newPiecesPositionMapping.pop(piece)

        piecePosition = self.piecesPositionMapping[piece]
        newPositionPiecesMapping = self.positionPiecesMapping.copy()
        newPositionPiecesMapping.pop(piecePosition)

        newThreatenedPieces = self.threatenedPieces.copy()
        newThreatenedPieces.pop(piece)
        for (threateningPiece, threatenedPieces) in newThreatenedPieces.items():
            if piece in threatenedPieces:
                newThreatenedPieces[threateningPiece].pop(piece)
                newNumThreatenedPieces -= 1

        newBeingThreatened = self.beingThreatened.copy()
        newBeingThreatened.pop(piece)
        for (threatenedPiece, threateningPieces) in newBeingThreatened.items():
            if piece in threateningPieces:
                newBeingThreatened[threatenedPiece].pop(piece)

        return Board(self.boardDim[0], 
            self.boardDim[1], 
            newPiecesPositionMapping, 
            newPositionPiecesMapping, 
            self.obstacles, 
            newThreatenedPieces, 
            newBeingThreatened,
            newNumThreatenedPieces)
 
    def getThreateningSquares(self, piece, startSquare):
        """Returns a list of Square objects which are threatened by piece"""
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
 
        return threatening

    def getNumThreatenedPieces(self):
        return self.numThreatenedPieces
 
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
 
    def __eq__(self, b):
        return self.boardDim == b.boardDim and\
            self.numThreatenedPieces == b.numThreatenedPieces and\
                self.obstacles == b.obstacles and\
                    self.piecesPositionMapping == b.piecesPositionMapping and\
                        self.positionPiecesMapping == b.positionPiecesMapping and\
                            self.threatenedPieces == b.threatenedPieces
 
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
    
    def getCurrPathCost(self):
        return self.pathCost
 
    def getParent(self):
        return self.parent
    
    def getDepth(self):
        return self.depth
 
    def __str__(self):
        return self.getBoard().__str__()


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    f = open(testfile, "r").read()
    def process(file):
        information = {}
        information['pieces'] = {}
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
            elif "K (Minimum number of pieces left in goal):" in line:
                information['K'] = int(line[42:])
            elif ("[" in line) and not ("Position" in line):
                li = line[1:-1].split(',')
                pieceType = li[0].lower()
                pieceCoord = li[1]
                piece = Piece(pieceType)
                square = Square(pieceCoord, (information["rows"], information["cols"]))
                information['pieces'][piece] = square
        return information

    information = process(f)
    b0 = Board(information['rows'],
        information['cols'],
        information['pieces'],
        obstacles = information['obstacles'])

    def search(b0, seed):
        current = b0
        k = information['K']
        stuff = []

        while (len(current.piecesPositionMapping) > k) and (current.getNumThreatenedPieces() > 0):
            chosenPiece = current.getBestCandidatePiece(seed)
            coord = current.piecesPositionMapping[chosenPiece].getCoord()
            current = current.removePiece(chosenPiece)
            stuff.append(coord)

        return current, stuff

    def capitalize(string):
        """Returns a string with the first letter capitalized"""
        return string[0].upper() + string[1:]

    seed = 0
    result, stuff = search(b0, seed)
    while result.getNumThreatenedPieces() > 0:
        seed += 10
        b0 = Board(information['rows'],
            information['cols'],
            information['pieces'],
            obstacles = information['obstacles'])
        result, stuff = search(b0, seed)

    resultDict = {}
    result_piece_coord = [((positioning.getCoord()[0], int(positioning.getCoord()[1:])), capitalize(piece.getType())) \
        for piece, positioning in result.piecesPositionMapping.items()]

    return dict(result_piece_coord)
