from math import inf
from queue import PriorityQueue
import sys
from time import time

### IMPORTANT: Remove cany print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove

class Piece:

    printMapping = {
        "king" : "K", 
        "knight" : "N", 
        "pawn" : "P", 
        "queen" : "Q",
        "bishop" : "B",
        "rook" : "R"
    }

    evalMapping = {
        "king" : 100, 
        "knight" : 2.5, 
        "pawn" : 1, 
        "queen" : 9,
        "bishop" : 3,
        "rook" : 5
    }

    def __init__(self, type, team):
        self.type = type
        self.team = team

    def getType(self):
        return self.type

    def getTeam(self):
        return self.team

    def getScore(self):
        return Piece.evalMapping[self.getType()]

    def getPrintMapping(self):
        if self.getTeam() == "enemy":
            return f" E{Piece.printMapping[self.getType()]}|"
        elif self.getTeam() == "friendly":
            return f" F{Piece.printMapping[self.getType()]}|"
        else:
            return f" {Piece.printMapping[self.getType()]} |"

    def __str__(self):
        return f"{self.getType()} {self.getTeam()}"

    def getHashMapping(self):
        if self.getTeam() == "enemy":
            return f"E{Piece.printMapping[self.getType()]}"
        elif self.getTeam() == "friendly":
            return f"F{Piece.printMapping[self.getType()]}"

class Knight(Piece):
    def __init__(self, team):
        super().__init__("knight", team)
        
class Rook(Piece):
    def __init__(self, team):
        super().__init__("rook", team)

class Bishop(Piece):
    def __init__(self, team):
        super().__init__("bishop", team)
        
class Queen(Piece):
    def __init__(self, team):
        super().__init__("queen", team)
        
class King(Piece):
    def __init__(self, team):
        super().__init__("king", team)
        
class Pawn(Piece):
    def __init__(self, team):
        super().__init__("pawn", team)

class Square:
    
    def __init__(self, position):
        self.file = position[0]
        self.rank = position[1:]
        self.boardDim = (5,5)
    
    def clone(self):
        return Square(self.file + self.rank)

    def goLeft(self):
        currX = ord(self.file) - 97
        newPosition = chr(currX - 1 + 97) + self.rank
        return Square(newPosition)

    def goRight(self):
        currX = ord(self.file) - 97
        newPosition = chr(currX + 1 + 97) + self.rank
        return Square(newPosition)

    def goUp(self):
        currY = int(self.rank)
        newPosition = self.file + str(currY - 1)
        return Square(newPosition)

    def goDown(self):
        currY = int(self.rank)
        newPosition = self.file + str(currY + 1)
        return Square(newPosition)

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

    count = 0
    hashing1 = {
        'FK' : 'a',
        'FQ' : 'b',
        'FB' : 'c',
        'FN' : 'd',
        'FR' : 'e',
        'FP' : 'f',
        'EK' : 'g',
        'EQ' : 'h',
        'EB' : 'i',
        'EN' : 'j',
        'ER' : 'k',
        'EP' : 'l',
    }

    hashing2 = {
        'a' : 'FK',
        'b' : 'FQ',
        'c' : 'FB',
        'd' : 'FN',
        'e' : 'FR',
        'f' : 'FP',
        'g' : 'EK',
        'h' : 'EQ',
        'i' : 'EB',
        'j' : 'EN',
        'k' : 'ER',
        'l' : 'EP',
    }


    def __init__(self, enemyPieces = None, 
            friendlyPieces = None, 
            squarePiecesMapping = None,
            turn = 'white'):
            
        self.boardDim = (5, 5)
        self.turn = turn # 'white' or 'black'

        if (enemyPieces == None):
            self.enemyPieces = {
                Piece("rook", "enemy") : Square("a0"),
                Piece("knight", "enemy") : Square("b0"),
                Piece("bishop", "enemy") : Square("c0"),
                Piece("queen", "enemy") : Square("d0"),
                Piece("king", "enemy") : Square("e0"),
                Piece("pawn", "enemy") : Square("a1"),
                Piece("pawn", "enemy") : Square("b1"),
                Piece("pawn", "enemy") : Square("c1"),
                Piece("pawn", "enemy") : Square("d1"),
                Piece("pawn", "enemy") : Square("e1")
            }
        else:
            self.enemyPieces = enemyPieces # Piece object: Square object

        if (friendlyPieces == None):
            self.friendlyPieces = {
                Piece("rook", "friendly") : Square("a4"),
                Piece("knight", "friendly") : Square("b4"),
                Piece("bishop", "friendly") : Square("c4"),
                Piece("queen", "friendly") : Square("d4"),
                Piece("king", "friendly") : Square("e4"),
                Piece("pawn", "friendly") : Square("a3"),
                Piece("pawn", "friendly") : Square("b3"),
                Piece("pawn", "friendly") : Square("c3"),
                Piece("pawn", "friendly") : Square("d3"),
                Piece("pawn", "friendly") : Square("e3")
            }
        else:
            self.friendlyPieces = friendlyPieces # Piece object: Square object

        if (squarePiecesMapping == None):
            self.squarePiecesMapping = {}
            for p, s in self.friendlyPieces.items():
                self.squarePiecesMapping[s] = p
            for p, s in self.enemyPieces.items():
                self.squarePiecesMapping[s] = p
        else:
            self.squarePiecesMapping = squarePiecesMapping

        self.itemMapping = {}
        self.pieceThreatenMapping = {}
        self.possibleMoves = {}
        self.whiteMaterial = 0
        self.blackMaterial = 0
        self.whiteThreateningSquares = {} # Keeps track of the squares that are threatened by the white. Square object : {Piece object : 0}
        self.blackThreateningSquares = {} # Keeps track of the squares that are threatened by the black. Square object : {Piece object : 0}

        for p, s in self.friendlyPieces.items():
            threateningSquares = self.getThreateningSquares(p, s)
            self.pieceThreatenMapping[p] = threateningSquares
            self.whiteMaterial += p.getScore()
            if turn == "white": # Calculate what moves I can take
                self.possibleMoves[p] = threateningSquares
                if p.getType() == "pawn":
                    possibleMoves = []
                    # If can move diagonally
                    for square in self.possibleMoves[p]:
                        if self.hasEnemyPiece(p, square):
                            possibleMoves.append(square)
                    # Can move up
                    if s.goUp().isValid() and (not s.goUp() in self.squarePiecesMapping):
                        possibleMoves.append(s.goUp())
                    self.possibleMoves[p] = possibleMoves
            if p.getType() != "pawn":
                self.itemMapping[p.getType() + " " + p.getTeam()] = p
        for p, s in self.enemyPieces.items():
            threateningSquares = self.getThreateningSquares(p, s)
            self.pieceThreatenMapping[p] = threateningSquares
            self.blackMaterial += p.getScore()
            if turn == "black":
                self.possibleMoves[p] = threateningSquares
                if p.getType() == "pawn":
                    possibleMoves = []
                    # If can move diagonally
                    for square in self.possibleMoves[p]:
                        if self.hasEnemyPiece(p, square):
                            possibleMoves.append(square)
                    # Can move up
                    if s.goDown().isValid() and (not s.goDown() in self.squarePiecesMapping):
                        possibleMoves.append(s.goDown())
                    self.possibleMoves[p] = possibleMoves
            if p.getType() != "pawn":
                self.itemMapping[p.getType() + " " + p.getTeam()] = p

    def kingInCheck(self, team):
        if team == "white":
            turn = "friendly" 
            king = self.itemMapping["king " + turn]
            kingPos = self.friendlyPieces[king]
            return kingPos in self.blackThreateningSquares
        else: 
            turn = "enemy" 
            king = self.itemMapping["king " + turn]
            kingPos = self.enemyPieces[king]
        return kingPos in self.whiteThreateningSquares

    def getPossibleMoves(self):
        turn = "white" if self.turn == "white" else "black"
        possibleMoves = PriorityQueue()
        for piece, squares in self.possibleMoves.items():
            for square in squares:
                newBoard = self.movePiece(piece, square.getCoord())
                if newBoard.kingInCheck(turn):
                    continue
                else:
                    eval = newBoard.evalPosition()
                    c = Board.count
                    Board.count += 1
                    possibleMoves.put((eval, c, (piece, square)))
        return possibleMoves
                
    def getDim(self):
        return self.boardDim

    def movePiece(self, piece, coord):
        """Returns a new Board after piece is moved"""

        square = Square(coord)
        team = piece.getTeam()
        if team == "enemy":
            clonedEnemyPieces = self.enemyPieces.copy()
            clonedFriendlyPieces = self.friendlyPieces.copy()
            clonedSquarePiecesMapping = self.squarePiecesMapping.copy()
            clonedPiecesThreatenMapping = self.pieceThreatenMapping.copy()
            oldPosition = clonedEnemyPieces[piece]

            if square in clonedSquarePiecesMapping: # There is a piece on the square that we want to move to
                existingPiece = self.getPiece(coord)
                if existingPiece.getTeam() == "enemy": # Invalid move
                    raise Exception("Cannot take own piece")
                else:
                    clonedFriendlyPieces.pop(existingPiece)
                    clonedPiecesThreatenMapping.pop(existingPiece)
                    
            clonedPiecesThreatenMapping[piece] = self.getThreateningSquares(piece, square)
            clonedEnemyPieces[piece] = square
            clonedSquarePiecesMapping.pop(oldPosition)
            clonedSquarePiecesMapping[square] = piece

            nextTurn = "white" if self.turn == "black" else "black"

            return Board(enemyPieces = clonedEnemyPieces,
                friendlyPieces = clonedFriendlyPieces,
                squarePiecesMapping = clonedSquarePiecesMapping,
                turn = nextTurn)

        elif team == "friendly":
            clonedEnemyPieces = self.enemyPieces.copy()
            clonedFriendlyPieces = self.friendlyPieces.copy()
            clonedSquarePiecesMapping = self.squarePiecesMapping.copy()
            clonedPiecesThreatenMapping = self.pieceThreatenMapping.copy()
            oldPosition = clonedFriendlyPieces[piece]

            if square in clonedSquarePiecesMapping: # There is a piece on the square that we want to move to
                existingPiece = self.getPiece(coord)
                if existingPiece.getTeam() == "friendly": # Invalid move
                    raise Exception("Cannot take own piece")
                else:
                    clonedEnemyPieces.pop(existingPiece)
                    clonedPiecesThreatenMapping.pop(existingPiece)
                    
            clonedPiecesThreatenMapping[piece] = self.getThreateningSquares(piece, square)
            clonedFriendlyPieces[piece] = square
            clonedSquarePiecesMapping.pop(oldPosition)
            clonedSquarePiecesMapping[square] = piece

            nextTurn = "white" if self.turn == "black" else "black"

            return Board(enemyPieces = clonedEnemyPieces,
                friendlyPieces = clonedFriendlyPieces,
                squarePiecesMapping = clonedSquarePiecesMapping,
                turn = nextTurn)

    def hasFriendlyPiece(self, piece, coord):
        """Returns True if piece has a friendly piece on coord"""
        if coord in self.squarePiecesMapping:
            existingPiece = self.getPiece(coord.getCoord())
            if existingPiece.getTeam() == piece.getTeam():
                return True
        return False

    def hasEnemyPiece(self, piece, coord):
        """Returns True if piece has an enemy piece on coord"""
        if coord in self.squarePiecesMapping:
            existingPiece = self.getPiece(coord.getCoord())
            if existingPiece.getTeam() != piece.getTeam():
                return True
        return False

    def getThreateningSquares(self, piece, startSquare):
        """Returns a list of Square objects which are threatened by piece"""
        type = piece.getType()
        team = piece.getTeam()

        threatening = []
        if type == "pawn": # Done
            if team == "friendly":
                leftUpSquare = startSquare.goLeft().goUp()
                coord = leftUpSquare.getCoord()
                if (leftUpSquare.isValid()):
                    if (self.hasPiece(leftUpSquare)):
                        existingPiece = self.getPiece(coord)
                        if existingPiece.getTeam() != piece.getTeam():
                            threatening.append(leftUpSquare)
                    else:
                        threatening.append(leftUpSquare)

                upRightSquare = startSquare.goUp().goRight()
                coord = upRightSquare.getCoord()
                if (upRightSquare.isValid()):
                    if (self.hasPiece(upRightSquare)):
                        existingPiece = self.getPiece(coord)
                        if existingPiece.getTeam() != piece.getTeam():
                            threatening.append(upRightSquare)
                    else:
                        threatening.append(upRightSquare)
            else:
                rightDownSquare = startSquare.goRight().goDown()
                coord = rightDownSquare.getCoord()
                if (rightDownSquare.isValid()):
                    if (self.hasPiece(rightDownSquare)):
                        existingPiece = self.getPiece(coord)
                        if existingPiece.getTeam() != piece.getTeam():
                            threatening.append(rightDownSquare)
                    else:
                        threatening.append(rightDownSquare)

                leftDownSquare = startSquare.goLeft().goDown()
                coord = leftDownSquare.getCoord()
                if (leftDownSquare.isValid()):
                    if (self.hasPiece(leftDownSquare)):
                        existingPiece = self.getPiece(coord)
                        if existingPiece.getTeam() != piece.getTeam():
                            threatening.append(leftDownSquare)
                    else:
                        threatening.append(leftDownSquare)

        elif type == "king": # Done
            leftSquare = startSquare.goLeft()
            coord = leftSquare.getCoord()
            if (leftSquare.isValid()):
                if (self.hasPiece(leftSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(leftSquare)
                else:
                    threatening.append(leftSquare)

            leftUpSquare = startSquare.goLeft().goUp()
            coord = leftUpSquare.getCoord()
            if (leftUpSquare.isValid()):
                if (self.hasPiece(leftUpSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(leftUpSquare)
                else:
                    threatening.append(leftUpSquare)

            upSquare = startSquare.goUp()
            coord = upSquare.getCoord()
            if (upSquare.isValid()):
                if (self.hasPiece(upSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(upSquare)
                else:
                    threatening.append(upSquare)

            upRightSquare = startSquare.goUp().goRight()
            coord = upRightSquare.getCoord()
            if (upRightSquare.isValid()):
                if (self.hasPiece(upRightSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(upRightSquare)
                else:
                    threatening.append(upRightSquare)

            rightSquare = startSquare.goRight()
            coord = rightSquare.getCoord()
            if (rightSquare.isValid()):
                if (self.hasPiece(rightSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(rightSquare)
                else:
                    threatening.append(rightSquare)

            rightDownSquare = startSquare.goRight().goDown()
            coord = rightDownSquare.getCoord()
            if (rightDownSquare.isValid()):
                if (self.hasPiece(rightDownSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(rightDownSquare)
                else:
                    threatening.append(rightDownSquare)

            downSquare = startSquare.goDown()
            coord = downSquare.getCoord()
            if (downSquare.isValid()):
                if (self.hasPiece(downSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(downSquare)
                else:
                    threatening.append(downSquare)

            leftDownSquare = startSquare.goLeft().goDown()
            coord = leftDownSquare.getCoord()
            if (leftDownSquare.isValid()):
                if (self.hasPiece(leftDownSquare)):
                    existingPiece = self.getPiece(coord)
                    if existingPiece.getTeam() != piece.getTeam():
                        threatening.append(leftDownSquare)
                else:
                    threatening.append(leftDownSquare)

        elif type == "knight": # Done
            if (startSquare.goLeft().goLeft().goUp().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goLeft().goLeft().goUp())): 
                threatening.append(startSquare.goLeft().goLeft().goUp())

            if (startSquare.goLeft().goUp().goUp().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goLeft().goUp().goUp())): 
                threatening.append(startSquare.goLeft().goUp().goUp())

            if (startSquare.goUp().goUp().goRight().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goUp().goUp().goRight())): 
                threatening.append(startSquare.goUp().goUp().goRight())
            if (startSquare.goUp().goRight().goRight().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goUp().goRight().goRight())): 
                threatening.append(startSquare.goUp().goRight().goRight())
            if (startSquare.goRight().goRight().goDown().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goRight().goRight().goDown())): 
                threatening.append(startSquare.goRight().goRight().goDown())
            if (startSquare.goRight().goDown().goDown().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goRight().goDown().goDown())): 
                threatening.append(startSquare.goRight().goDown().goDown())
            if (startSquare.goDown().goDown().goLeft().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goDown().goDown().goLeft())): 
                threatening.append(startSquare.goDown().goDown().goLeft())
            if (startSquare.goDown().goLeft().goLeft().isValid() and \
                not self.hasFriendlyPiece(piece, startSquare.goDown().goLeft().goLeft())): 
                threatening.append(startSquare.goDown().goLeft().goLeft())
        
        elif type == "rook": # Done
            # Go UP
            currSquare = startSquare
            while (currSquare.goUp().isValid() and (not currSquare.goUp() in self.squarePiecesMapping)):
                currSquare = currSquare.goUp()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goUp()):
                threatening.append(currSquare.goUp())
            # Go DOWN
            currSquare = startSquare
            while (currSquare.goDown().isValid() and (not currSquare.goDown() in self.squarePiecesMapping)):
                currSquare = currSquare.goDown()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goDown()):
                threatening.append(currSquare.goDown())
            # Go LEFT
            currSquare = startSquare
            while (currSquare.goLeft().isValid() and (not currSquare.goLeft() in self.squarePiecesMapping)):
                currSquare = currSquare.goLeft()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goLeft()):
                threatening.append(currSquare.goLeft())
            # Go RIGHT
            currSquare = startSquare
            while (currSquare.goRight().isValid() and (not currSquare.goRight() in self.squarePiecesMapping)):
                currSquare = currSquare.goRight()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goRight()):
                threatening.append(currSquare.goRight())

        elif type == "bishop": # Done
            # Go UPLEFT
            currSquare = startSquare
            while (currSquare.goUp().goLeft().isValid() and (not currSquare.goUp().goLeft() in self.squarePiecesMapping)):
                currSquare = currSquare.goUp().goLeft()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goUp().goLeft()):
                threatening.append(currSquare.goUp().goLeft())
            # Go DOWNLEFT
            currSquare = startSquare
            while (currSquare.goDown().goLeft().isValid() and (not currSquare.goDown().goLeft() in self.squarePiecesMapping)):
                currSquare = currSquare.goDown().goLeft()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goDown().goLeft()):
                threatening.append(currSquare.goDown().goLeft())
            # Go UPRIGHT
            currSquare = startSquare
            while (currSquare.goUp().goRight().isValid() and (not currSquare.goUp().goRight() in self.squarePiecesMapping)):
                currSquare = currSquare.goUp().goRight()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goUp().goRight()):
                threatening.append(currSquare.goUp().goRight())
            # Go DOWNRIGHT
            currSquare = startSquare
            while (currSquare.goDown().goRight().isValid() and (not currSquare.goDown().goRight() in self.squarePiecesMapping)):
                currSquare = currSquare.goDown().goRight()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goDown().goRight()):
                threatening.append(currSquare.goDown().goRight())
                
        elif type == "queen": # Done
            # Go UPLEFT
            currSquare = startSquare
            while (currSquare.goUp().goLeft().isValid() and (not currSquare.goUp().goLeft() in self.squarePiecesMapping)):
                currSquare = currSquare.goUp().goLeft()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goUp().goLeft()):
                threatening.append(currSquare.goUp().goLeft())
            # Go DOWNLEFT
            currSquare = startSquare
            while (currSquare.goDown().goLeft().isValid() and (not currSquare.goDown().goLeft() in self.squarePiecesMapping)):
                currSquare = currSquare.goDown().goLeft()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goDown().goLeft()):
                threatening.append(currSquare.goDown().goLeft())
            # Go UPRIGHT
            currSquare = startSquare
            while (currSquare.goUp().goRight().isValid() and (not currSquare.goUp().goRight() in self.squarePiecesMapping)):
                currSquare = currSquare.goUp().goRight()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goUp().goRight()):
                threatening.append(currSquare.goUp().goRight())
            # Go DOWNRIGHT
            currSquare = startSquare
            while (currSquare.goDown().goRight().isValid() and (not currSquare.goDown().goRight() in self.squarePiecesMapping)):
                currSquare = currSquare.goDown().goRight()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goDown().goRight()):
                threatening.append(currSquare.goDown().goRight())
            # Go UP
            currSquare = startSquare
            while (currSquare.goUp().isValid() and (not currSquare.goUp() in self.squarePiecesMapping)):
                currSquare = currSquare.goUp()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goUp()):
                threatening.append(currSquare.goUp())
            # Go DOWN
            currSquare = startSquare
            while (currSquare.goDown().isValid() and (not currSquare.goDown() in self.squarePiecesMapping)):
                currSquare = currSquare.goDown()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goDown()):
                threatening.append(currSquare.goDown())
            # Go LEFT
            currSquare = startSquare
            while (currSquare.goLeft().isValid() and (not currSquare.goLeft() in self.squarePiecesMapping)):
                currSquare = currSquare.goLeft()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goLeft()):
                threatening.append(currSquare.goLeft())
            # Go RIGHT
            currSquare = startSquare
            while (currSquare.goRight().isValid() and (not currSquare.goRight() in self.squarePiecesMapping)):
                currSquare = currSquare.goRight()
                threatening.append(currSquare.clone())
            if self.hasEnemyPiece(piece, currSquare.goRight()):
                threatening.append(currSquare.goRight())

        # Caching
        if piece.getTeam() == "friendly":
            for square in threatening:
                if square not in self.whiteThreateningSquares:
                    self.whiteThreateningSquares[square] = {}
                self.whiteThreateningSquares[square][piece] = 0
        elif piece.getTeam() == "enemy":
            for square in threatening:
                if square not in self.blackThreateningSquares:
                    self.blackThreateningSquares[square] = {}
                self.blackThreateningSquares[square][piece] = 0
        else:
            raise Exception("What the fuck")
            

        return threatening

    def __str__(self):
        numRows = self.getDim()[0]
        numCols = self.getDim()[1]
        board = [["   |" for i in range(numCols)] for j in range(numRows)]

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
                    self.enemyPieces == b.enemyPieces and\
                        self.friendlyPieces == b.friendlyPieces

    def __hash__(self):
        li = []
        for letter in 'abcde':
            for number in range(5):
                coord = letter + str(number)
                s = Square(coord)
                if s in self.squarePiecesMapping:
                    piece = self.squarePiecesMapping[s]
                    hashed = Board.hashing1[piece.getHashMapping()]
                    li.append(hashed)
                else:
                    li.append("X")
        return "".join(li)

    def getPiece(self, coord):
        square = Square(coord)
        if square in self.squarePiecesMapping:
            return self.squarePiecesMapping[square]
        else:
            print("No such piece at", coord)

    def hasPiece(self, square):
        return square in self.squarePiecesMapping

    def evalPosition(self):
        whiteMaterial = self.whiteMaterial
        blackMaterial = self.blackMaterial
        materialDiff = whiteMaterial - blackMaterial
        whiteControls = len(self.whiteThreateningSquares)
        blackControls = len(self.blackThreateningSquares)
        controlDiff = whiteControls - blackControls
        return materialDiff + blackControls / 25

class Node:
    
    def __init__(self, board, type, alpha = -inf, beta = inf):
        self.alpha = alpha
        self.beta = beta
        self.board = board
        self.type = type # min or max
        self.value = inf if type == 'min' else -inf
        self.children = []
        self.bestChild = None
        self.bestMove = None

    def getAlpha(self):
        return self.alpha

    def getBeta(self):
        return self.beta

    def getBoard(self):
        return self.board

    def getType(self):
        return self.type

    def setValue(self, value, which):
        if which == "alpha":
            self.alpha = value
        else:
            self.beta = value

    def getParent(self):
        return self.parent

    def makeParentOf(self, child):
        self.children.append(child)
        child.parent = self

    def getChildren(self):
        return self.children

    def setBestChild(self, child, piece, coord):
        self.bestChild = child
        self.bestMove = (piece, coord)

    def getBestChild(self):
        return self.bestChild
    


class RandomMover:
    
    def __init__(self):
        self.type = "random"

    def makeMove(self, board):
        possibleMoves = board.getPossibleMoves()
        move = possibleMoves.get()
        randomPiece = move[-1][0]
        randomMove = move[-1][1]
        return board.movePiece(randomPiece, randomMove.getCoord())

class MyMover:

    def __init__(self, side):
        self.type = "smart"
        self.min_or_max = "min" if side == "black" else "max"

    def makeMove(self, board):
        t1 = time()
        n0 = Node(board, self.min_or_max)
        n0, eval = ab(n0, 0, 4)
        n1 = n0.getBestChild()
        print(time() - t1)
        return n1.getBoard()

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(node, depth, maxDepth):
    board = node.getBoard()
    turn = board.turn
    possibleMoves = board.getPossibleMoves()

    if possibleMoves.qsize() == 0:
        if turn == "white":
            which = "alpha"
            eval = -inf
        else:
            which = "beta"
            eval = inf
        node.setValue(eval, which)
        return node, eval
    
    if depth == maxDepth:
        # which = "alpha" if turn == "white" else "beta"
        eval = board.evalPosition()
        node.setValue(eval, "alpha")
        node.setValue(eval, "beta")
        return node, eval

    while possibleMoves.qsize() > 0:
        popped = possibleMoves.get()
        piece = popped[-1][0]
        square = popped[-1][1]
        if node.getAlpha() >= node.getBeta(): # Prune
            if node.getType() == "min":
                return node, node.getBeta()
            else:
                return node, node.getAlpha()

        newBoard = board.movePiece(piece, square.getCoord())
        newType = "min" if node.getType() == "max" else "max"
        newAlpha = node.getAlpha()
        newBeta = node.getBeta()
        newNode = Node(newBoard, newType, newAlpha, newBeta)
        node.makeParentOf(newNode)

        x, eval = ab(newNode, depth + 1, maxDepth)

        if node.getType() == "min":
            value = min(newNode.getAlpha(), newNode.getBeta(), node.getBeta())
            if newNode.getAlpha() < node.getBeta() or newNode.getBeta() < node.getBeta():
                node.setBestChild(newNode, piece, square.getCoord())
            node.setValue(value, "beta")
        else:
            value = max(newNode.getAlpha(), newNode.getBeta(), node.getAlpha())
            if newNode.getAlpha() > node.getAlpha() or newNode.getBeta() > node.getAlpha():
                node.setBestChild(newNode, piece, square.getCoord())
            node.setValue(value, "alpha")
    

    return node, 0

b0 = Board()
fn = b0.getPiece("b4")
en = b0.getPiece("b0")
b1 = b0.movePiece(fn, "c2")
b2 = b1.movePiece(en, "c2")
b = b2.getPiece('b3')
b3 = b2.movePiece(b, 'c2')
b5 = b3.movePiece(b3.getPiece('b1'), 'b2').movePiece(b3.getPiece('c2'), 'd1')
n0 = Node(b0, "max")

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def convertNum(i):
    d = {
        0:4,
        1:3,
        2:2,
        3:1,
        4:0
    }
    return d[i]



def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    config = sys.argv[1] #Takes in config.txt Optional
    fp = {}
    ep = {}
    for square_tup, piece_tup in gameboard.items():
        square = Square(square_tup[0] + str(square_tup[1]))
        piece_type = piece_tup[0].lower()
        team = "friendly" if piece_tup[1] == "White" else "enemy"
        if piece_type == 'king':
            piece = King(team)
        elif piece_type == 'queen':
            piece = Queen(team)
        elif piece_type == 'knight':
            piece = Knight(team)
        elif piece_type == 'rook':
            piece = Rook(team)
        elif piece_type == 'bishop':
            piece = Bishop(team)
        elif piece_type == 'pawn':
            piece = Pawn(team)
        if team == 'friendly':
            fp[piece] = square
        elif team == 'enemy':
            ep[piece] = square
    
    board = Board(ep, fp)
    node = Node(board, "max")
    n = ab(node, 0, 4)


    move = node.bestMove
    return move #Format to be returned (('a', 0), ('b', 3))

# test = {('a', 0) : ('Queen','White'), ('d', 10) : ('Knight',' Black'), ('g', 25) : ('Rook','White')}



ep = {King('enemy') : Square('e0'), Queen('enemy') : Square('d0'), Bishop('enemy') : Square('c0'), Rook('enemy') : Square('a0'), Knight('enemy') : Square('c3'),
Pawn('enemy') : Square('e1'), Pawn('enemy') : Square('d1'), Pawn('enemy') : Square('c1'), Pawn('enemy') : Square('b1'), Pawn('enemy') : Square('a1')}
fp = {King('friendly') : Square('e4'), Queen('friendly') : Square('d4'), Bishop('friendly') : Square('c4'),
Pawn('friendly') : Square('d3'), Pawn('friendly') : Square('e3'), Pawn('friendly') : Square('b2')}
# test = Board(ep, fp, turn = 'white')

def playRandom():

    rm = RandomMover()
    curr = b0

    while True:
        #break
        print(curr)
        move = input("What is your move?: ")
        fromSquare = move[:2]
        toSquare = move[2:]
        possibleMoves = curr.getPossibleMoves()
        try:
            piece = curr.squarePiecesMapping[Square(fromSquare)]
            newBoard = curr.movePiece(piece, toSquare)

            curr = newBoard
            print(curr)
            curr = rm.makeMove(curr)

        except:
            print_exception()

def play():
    curr = b0

    while True:
        #break
        print(curr)
        move = input("What is your move?: ")
        fromSquare = move[:2]
        toSquare = move[2:]
        possibleMoves = curr.getPossibleMoves()
        try:
            piece = curr.squarePiecesMapping[Square(fromSquare)]
            newBoard = curr.movePiece(piece, toSquare)

            curr = newBoard

        except:
            print_exception()

def playSmart(side):

    rm = MyMover(side)
    if side == 'white':
        curr = rm.makeMove(b0)
    else:
        curr = b0

    while True:
        #break
        print(curr)
        move = input("What is your move?: ")
        fromSquare = move[:2]
        toSquare = move[2:]
        possibleMoves = curr.getPossibleMoves()
        piece = curr.squarePiecesMapping[Square(fromSquare)]
        newBoard = curr.movePiece(piece, toSquare)

        curr = newBoard
        print(curr)
        curr = rm.makeMove(curr)

def vs():
    mm = MyMover("min")
    rm = RandomMover()
    print(b0)
    curr = b0.movePiece(b0.getPiece('a3'), 'a2')
    while curr.blackMaterial != 0 and curr.whiteMaterial != 0:
        print("Black's turn")
        print(curr)
        curr = mm.makeMove(curr)
        print()
        print("White's turn")
        print(curr)
        curr = rm.makeMove(curr)