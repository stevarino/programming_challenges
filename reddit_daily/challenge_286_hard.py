# -*- coding: utf-8 -*-
"""Python 3 solution to Reddit Daily Challenge #286 [Hard] Rush Hour Solver

https://www.reddit.com/r/dailyprogrammer/comments/56bh88/20161007_challenge_286_hard_rush_hour_solver/

Runs against an arbitrary size puzzle (can be rectangular) with arbitrarily
sized cars (must be continous though). A car of length 1 is assumed to be 
horizontal.

Easy UML:
    A Puzzle has many PuzzleStates.
    A Puzzle has one winner (PuzzleState)
    A PuzzleState has many Moves
    A PuzzleState has many PuzzlePieces
    A PuzzlePiece has a single Position
    
Original Description:

The game of Rush Hour is a puzzle game wherein the player has to slide the 
cars from their original position to allow the escape car to exit the board. 
Rush Hour is similar to other sliding puzzles, but with a twist: each piece 
moves along only one direction, instead of moving both horizontally and 
vertically. This makes individual moves easier to understand, and sequences 
easier to visualize. This is basically how cars move - forwards or backwards.

Rush Hour includes a 6x6 playing board with an exit opening along on edge, 
a red escape car, and several blocking cars (of dimensions 2x1) and several 
blocking trucks (of dimensions 3x1 ). The goal is to slide the red car (the 
escape vehicle) through the exit opening in the edge of the grid. To play, 
shift the cars and trucks up and down, left and right, until the path is 
cleared to slide the escape vehicle out the exit. You may not lift pieces off 
the grid. Pieces may only move forward and back, not sideways

In this challenge you'll be given a starting layout, then you have to show 
how to move the cars to allow the red escape car to exit the board.

"""

from collections import namedtuple, deque
from copy import deepcopy

Position = namedtuple('Position', 'y x') 

class Move(object):
    '''A mutable move object for a defined piece.'''
    def __init__(self, piece, scalar):
        '''Constructor!'''
        self.piece = piece
        self.scalar = scalar
    
    def __str__(self):
        return "{} {:+}".format(self.piece, self.scalar)

class Puzzle(object):
    def __init__(self, input):
        '''Constructor! Initializes state.'''
        self.stateset = set()
        self.states = deque()
        self.winner = None
        
        self.states.append(PuzzleState(input))
        self.stateset.add(str(self.states[0]))
        
    def solve(self):
        '''Solve the puzzle, saving the winning state into self.winner (if 
        applicable).'''
        while self.states:
            state = self.states.popleft()
            if state.pieces['R'].get_new_pos(1) == state.goal:
                # required as we just get R to the edge, not the exit
                state.moves[-1].scalar += 1
                self.winner = state
                return
            child_states = state.get_child_states()
            for cs in child_states:
                id = str(cs)
                if id not in self.stateset:
                    self.stateset.add(id)
                    self.states.append(cs)
                    
    def display(self):
        '''Print the winner.'''
        print()
        if self.winner is None:
            print("No winning moves found.")
        else:
            for move in self.winner.moves:
                print(move)
        
class PuzzleState(object):
    def __init__(self, input):
        '''Constructo!'''
        self.pieces = dict()
        self.goal = None
        self.width = 0
        self.height = 0
        self.moves = list()
        self.parse(input)
        
        assert self.goal is not None, "Goal was not found in puzzle."
        assert 'R' in self.pieces, 'Red car not found in puzzle.'
        
    def parse(self, input):
        '''Convert a string into a puzzle state.'''
        lines = list(map(lambda l: l.strip(), input.strip().split('\n')))
        self.height = len(lines)
        prev = '.'
        for i, line in enumerate(lines):
            width = len(line.replace('>', ''))
            if self.width == 0:
                self.width = width
            else:
                assert  self.width == width, "Unequal widths."
            for j, char in enumerate(line):
                if char == '.':
                    pass
                elif char == '>':
                    self.goal = (i, j)
                elif char not in self.pieces:
                    self.pieces[char] = PuzzlePiece(char, Position(i, j), 1)
                else:
                    self.pieces[char].size += 1
                    self.pieces[char].is_horiz = (char == prev)
                prev = char
        
    def get_position_contents(self, pos):
        '''Returns the piece at the given position, or None.'''
        for k, piece in self.pieces.items():
            if (piece.pos.x <= pos.x <= piece.end.x 
              and piece.pos.y <= pos.y <= piece.end.y):
                return piece
        return None
        
    def get_child_states(self):
        '''Returns a list of child states possible.'''
        states = []
        max_moves = max(self.width, self.height)
        for k, piece in self.pieces.items():
            for direction in (-1,1):
                offset = direction
                is_valid = True
                while is_valid:
                    pos = piece.get_new_pos(offset)
                    is_valid = self.is_valid_pos(pos)
                    if is_valid:
                        states.append(self.make_state(Move(k, offset)))
                    offset += direction
        return states
            
    def is_valid_pos(self, pos):
        '''See's if a position is a valid move (in-bounds and empty).'''
        if 0 <= pos.y < self.height and 0 <= pos.x < self.width:
            if self.get_position_contents(pos) is None:
                return True
        return False
        
    def make_state(self, move):
        state = deepcopy(self)
        state.move_piece(move)
        return state
        
    def move_piece(self, move):
        '''Document and perform a move'''
        self.moves.append(move)
        piece = self.pieces[move.piece]
        piece.move(move.scalar)
    
    def __str__(self):
        '''Converts to string - used for state tracking.'''
        state = []
        for key in sorted(self.pieces.keys()):
            piece = self.pieces[key]
            state.append("{}({},{},{})".format(key, piece.pos.y, 
                piece.pos.x, 0 if piece.is_horiz else 1))
        return ":".join(state)
        
class PuzzlePiece(object):
    def __init__(self, label='_', pos=Position(0,0), size=1, is_horiz=True):
        '''Constructor!'''
        self.label = label
        self.pos = pos
        self.size = size
        self.is_horiz = is_horiz
        
    @property
    def end(self):
        '''Returns the end position of the piece.'''
        y, x = self.pos
        if self.is_horiz:
            x += self.size - 1
        else:
            y += self.size - 1
        return Position(y, x)
    
    def get_new_pos(self, scalar):
        '''Returns the important position from a given move amount'''
        y, x = self.pos
        if scalar > 0:
            y, x = self.end
        if self.is_horiz:
            x += scalar
        else:
            y += scalar
        return Position(y, x)
        
    def move(self, scalar):
        '''Move the piece the given move amount.'''
        y, x = self.pos
        if self.is_horiz:
            x += scalar
        else:
            y += scalar
        self.pos = Position(y, x)
        
    def __str__(self):
        '''Convert to string.'''
        return "{} {} {} {}".format(    
            self.label, self.pos, self.size, self.is_horiz)

def main(puzzle):
    import time
    start = time.time()
    p = Puzzle(puzzle)
    p.solve()
    p.display()
    print("\nSeconds: {:.3f}, Moves: {}".format(
        time.time() - start, len(p.winner.moves)))
    
if __name__ == "__main__":
    puzzle1 = '''GAA..Y
                 G.V..Y
                 RRV..Y>
                 ..VZZZ
                 ....B.
                 WWW.B.'''
    # 5.503s - 17 moves
    
    puzzle2 = '''TTTAU.
                 ...AU.
                 RR..UB>
                 CDDFFB
                 CEEG.H
                 VVVG.H'''
    # 2.697 - 7 moves
                 
    puzzle3 = '''QQQWEU
                TYYWEU
                T.RREU>
                IIO...
                .PO.AA
                .PSSDD'''
    # 142.212 - 49 moves
    
    
    puzzle4 = '''..ABBC
                ..A..C
                ..ARRC>
                ...EFF
                GHHE..
                G..EII'''
    # 59.128 - 33 moves

    puzzle5 = '''..............
                 GGGGGGW.......
                 RRB...........>
                 ..B...........'''
    # 0.198 - 4 moves (single-width cars are assumed horizontal)
    
    main(puzzle5)
