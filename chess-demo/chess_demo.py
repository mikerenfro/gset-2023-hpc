#!/usr/bin/env python3
import asciimatics
from asciimatics.screen import ManagedScreen
import chess
import chess.engine
import os
from pprint import pprint
import string
import sys
import time

def fen_to_array(fen):
    """
    Convert Forsyth–Edwards Notation  of a chess board into a list of lists
    of characters. https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation

    FEN uses algebraic notation (pawn = "P", knight = "N", bishop = "B",
    rook = "R", queen = "Q" and king = "K"), with uppercase for white and
    lowercase for black. Empty squares are denoted with a number 1-8.
    Each rank of the board is separated by a slash.

    There are other fields after the board state for whose turn it is,
    what castling options are available, etc., but those aren't relevant
    to this function.

    Starting board string:
    rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

    Parameters: fen (string), the FEN notation of a board state.
    Returns: board, a list of lists of single characters of piece positions.
    """
    board = []
    for row in fen.split('/'):
        # Each row/rank in the board is separated by a / -- last row will
        # also contain the extra data about the game state.
        brow = []
        for c in row:
            if c == ' ':
                # If we hit a space, it's after we've gone past the board
                # state on the last row. Break out of the loop and go on.
                break
            elif c in '12345678':
                # If we have a number, append that many spaces into the row
                # data.
                brow.extend( [' '] * int(c) )
            else:
                # Otherwise, keep the character as-is.
                brow.append(c)
        board.append(brow)  # Append this row to the board
    return board  # Done with rows, return the whole board.

def array_to_asciimatic(array, screen,
                        board_x_offset=0,
                        board_y_offset=0):
    """
    Take a list of lists of characters (usually from fen_to_array()) and
    print them to an asciimatic screen.

    Parameters: array (list of lists of single characters), representing
                board state.
                screen (an asciimatic ManagedScreen)
                board_x_offset (horizontal offset of the board on the screen)
                board_y_offset (vertical offset of the board on the screen)
    Returns: nothing
    """
    # Green/white board with black/bold-white (brighter) pieces is good enough
    # contrast on a normal black terminal window.
    black_square=screen.COLOUR_GREEN
    black_piece=screen.COLOUR_BLACK
    white_square=screen.COLOUR_WHITE
    white_piece=screen.COLOUR_WHITE  # but bold
    bold = screen.A_BOLD
    normal = screen.A_NORMAL
    # pprint(array)
    for row in range(0, 8):
        for col in range(0, 8):
            # Determine the color square we're on for background color
            if (col%2 == row%2):
                # We're on a white square
                square_color = white_square
            else:
                # We're on a black square
                square_color = black_square

            # Determine which color piece we are for character color
            piece = array[row][col]
            if piece in string.ascii_lowercase:
                # This is a black piece
                piece_color = black_piece
                piece_attr = normal
            else:
                # This is either a white_piece or blank
                piece_color = white_piece
                piece_attr = bold

            # Print with appropriate colors and attributes
            screen.print_at(text=piece, x=col+board_x_offset,
                            y=row+board_y_offset, colour=piece_color,
                            attr=piece_attr, bg=square_color)
    return

outcomes = {
    'white': 0,
    'black': 0,
    None: 0,
}

def main(white_time=0.001, black_time=0.001,
         white_nodes=1, white_threads=1,
         black_nodes=1, black_threads=96):
    # engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\mwr\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    white_engine = chess.engine.SimpleEngine.popen_uci(["./srun_stockfish.sh",
                                                        str(white_nodes),
                                                        str(white_threads)])
    black_engine = chess.engine.SimpleEngine.popen_uci(["./srun_stockfish.sh",
                                                        str(black_nodes),
                                                        str(black_threads)])
    white_limit = chess.engine.Limit(time=white_time, depth=5)
    white_engine.configure({"Threads": white_threads})
    black_limit = chess.engine.Limit(time=black_time, depth=5)
    black_engine.configure({"Threads": black_threads})

    win_stats_format = 'White wins: {0}, Black wins: {1}, Other: {2}'
    win_stats = win_stats_format.format(outcomes['white'], outcomes['black'],
                                        outcomes[None])
    while True:
        with ManagedScreen() as screen:
            screen.clear()

            # Visual testing code here
            # fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            # board = fen_to_board(fen)
            # while True:
            #     board_to_asciimatic(board, screen, board_x_offset=2,
            #                         board_y_offset=1)
            #     screen.refresh()

            # Real code here
            # Make a new board for a new game
            board = chess.Board()
            whose_turn = 'white'
            while not board.is_game_over():
                if whose_turn == 'white':
                    result = white_engine.play(board, white_limit)
                    whose_turn = 'black'
                else:
                    result = black_engine.play(board, black_limit)
                    whose_turn = 'white'
                board.push(result.move)
                screen.clear_buffer(screen.COLOUR_BLACK, screen.A_NORMAL,
                                    screen.COLOUR_BLACK)
                screen.print_at(win_stats, x=0, y=15,
                                colour=screen.COLOUR_RED,
                                bg=screen.COLOUR_BLACK)
                array = fen_to_array(board.fen())
                array_to_asciimatic(array, screen,
                                    board_x_offset=3, board_y_offset=3)
                screen.refresh()

        outcome = board.outcome()
        if outcome.winner == chess.WHITE:
            outcomes['white'] += 1
        elif outcome.winner == chess.BLACK:
            outcomes['black'] += 1
        elif outcome.winner == None:
            outcomes[None] += 1
        win_stats = win_stats = win_stats_format.format(outcomes['white'],
                                                        outcomes['black'],
                                                        outcomes[None])
        #print(win_stats)

if __name__ == "__main__":
    ( white_time, black_time ) = ( 0.1, 0.1 )
    white_nodes = sys.argv[1]
    white_threads = sys.argv[2]
    black_nodes = sys.argv[3]
    black_threads = sys.argv[4]
    try:
        main(white_time, black_time,
             white_nodes, white_threads,
             black_nodes, black_threads)
    except KeyboardInterrupt:
        print('Interrupted')
        total_games = outcomes['white']+outcomes['black']+outcomes[None]
        wdl_format = 'White W/D/L percentages ({0} games): {1:.1f}/{2:.1f}/{3:.1f}'
        wdl = wdl_format.format(total_games,100*outcomes['white']/total_games,
                                100*outcomes['black']/total_games,
                                100*outcomes[None]/total_games)
        print(wdl)
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
