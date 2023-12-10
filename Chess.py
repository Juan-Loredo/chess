"""
Name: Juan Loredo
GitHub: Juan-Loredo
Date: 12/10/2023
Description:  The code initializes a chess game, allows players to make moves, checks for check conditions,
and prints the chessboard after each move.
The game continues until manually interrupted or terminated.

"""

WHITE = "white"
BLACK = "black"


class Pawn:
    def __init__(self, color, symbol, direction):
        self.color = color
        self.symbol = symbol
        self.direction = direction


class Rook:
    def __init__(self, color, symbol, direction):
        self.color = color
        self.symbol = symbol
        self.direction = direction


class Knight:
    def __init__(self, color, symbol, direction):
        self.color = color
        self.symbol = symbol
        self.direction = direction


class Bishop:
    def __init__(self, color, symbol, direction):
        self.color = color
        self.symbol = symbol
        self.direction = direction


class Queen:
    def __init__(self, color, symbol, direction):
        self.color = color
        self.symbol = symbol
        self.direction = direction


class King:
    def __init__(self, color, symbol, direction):
        self.color = color
        self.symbol = symbol
        self.direction = direction


class Game:
    """Class representing a chess game."""

    def __init__(self):
        """
        Initialize a new chess game.

        Attributes:
        - playersturn: Current player's turn (either "black" or "white").
        - message: A message string for displaying prompts.
        - gameboard: Dictionary representing the chessboard.
        """
        self.playersturn = BLACK
        self.message = "this is where prompts will go"
        self.gameboard = {}
        self.placePieces()
        print("chess program. enter moves in algebraic notation separated by space")
        self.main()

    def placepieces(self, uniDict=None):
        """
        Place chess pieces on the initial chessboard.

        White pieces are placed at the bottom (row 1), and black pieces are placed at the top (row 6).
        """
        for i in range(0, 8):
            self.gameboard[(i, 1)] = Pawn(WHITE, uniDict[WHITE][Pawn], 1)
            self.gameboard[(i, 6)] = Pawn(BLACK, uniDict[BLACK][Pawn], -1)

        placers = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for i in range(0, 8):
            self.gameboard[(i, 0)] = placers[i](WHITE, uniDict[WHITE][placers[i]])
            self.gameboard[((7 - i), 7)] = placers[i](BLACK, uniDict[BLACK][placers[i]])
        placers.reverse()

    def main(self):
        """
        Main loop for executing the chess game.

        This loop allows players to make moves and updates the game state accordingly.
        """
        while True:
            self.printBoard()
            print(self.message)
            self.message = ""
            startpos, endpos = self.parseInput()
            try:
                target = self.gameboard[startpos]
            except:
                self.message = "could not find piece; index probably out of range"
                target = None

            if target:
                print("found " + str(target))
                if target.Color != self.playersturn:
                    self.message = "you aren't allowed to move that piece this turn"
                    continue
                if target.isValid(startpos, endpos, target.Color, self.gameboard):
                    self.message = "that is a valid move"
                    self.gameboard[endpos] = self.gameboard[startpos]
                    del self.gameboard[startpos]
                    self.isCheck()
                    if self.playersturn == BLACK:
                        self.playersturn = WHITE
                    else:
                        self.playersturn = BLACK
                else:
                    self.message = "invalid move" + str(target.availableMoves(startpos[0], startpos[1], self.gameboard))
                    print(target.availableMoves(startpos[0], startpos[1], self.gameboard))
            else:
                self.message = "there is no piece in that space"

    def isCheck(self):
        """
        Check if the current player is in check.

        This method identifies the kings on the board and checks if any opponent's pieces can attack them.
        """
        king = King
        kingDict = {}
        pieceDict = {BLACK: [], WHITE: []}
        for position, piece in self.gameboard.items():
            if type(piece) == King:
                kingDict[piece.Color] = position
            print(piece)
            pieceDict[piece.Color].append((piece, position))
        # white
        if self.canSeeKing(kingDict[WHITE], pieceDict[BLACK]):
            self.message = "White player is in check"
        if self.canSeeKing(kingDict[BLACK], pieceDict[WHITE]):
            self.message = "Black player is in check"

    def canSeeKing(self, kingpos, piecelist):
        """
        Check if any pieces in the given list can attack the king.

        Args:
        - kingpos: Position of the king on the board.
        - piecelist: List of tuples representing pieces and their positions.

        Returns:
        - True if any piece in piecelist can attack the king; otherwise, False.
        """
        for piece, position in piecelist:
            if piece.isValid(position, kingpos, piece.Color, self.gameboard):
                return True

    def parseInput(self):
        """
        Parse user input for chess moves.

        Returns:
        - Tuple representing the starting and ending positions of the move.
        """
        try:
            a, b = input().split()
            a = ((ord(a[0]) - 97), int(a[1]) - 1)
            b = (ord(b[0]) - 97, int(b[1]) - 1)
            print(a, b)
            return (a, b)
        except:
            print("error decoding input. please try again")
            return ((-1, -1), (-1, -1))

    def printBoard(self):
        """Print the current state of the chessboard."""
        print("  1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
        for i in range(0, 8):
            print("-" * 32)
            print(chr(i + 97), end="|")
            for j in range(0, 8):
                item = self.gameboard.get((i, j), " ")
                print(str(item) + ' |', end=" ")
            print()
        print("-" * 32)
