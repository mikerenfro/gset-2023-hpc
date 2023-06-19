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
    board = []
    for row in fen.split('/'):
        brow = []
        for c in row:
            if c == ' ':
                break
            elif c in '12345678':
                brow.extend( [' '] * int(c) )
            else:
                brow.append(c)
            # elif c == 'p':
            #     brow.append( 'bp' )
            # elif c == 'P':
            #     brow.append( 'wp' )
            # elif c > 'Z':
            #     brow.append( 'b'+c.upper() )
            # else:
            #     brow.append( 'w'+c )

        board.append( brow )
    return board

def array_to_asciimatic(array, screen,
                        board_x_offset=0,
                        board_y_offset=0):
    black_square=screen.COLOUR_GREEN
    black_piece=screen.COLOUR_BLACK # but bold
    white_square=screen.COLOUR_WHITE
    white_piece=screen.COLOUR_WHITE # but bold
    bold = screen.A_BOLD
    normal = screen.A_NORMAL
    # pprint(array)
    for row in range(0, 8):
        for col in range(0, 8):
            if (col%2==0 and row%2!=0) or (col%2==1 and row%2==0):
                # white square
                square_color = white_square
            else:
                # black square
                square_color = black_square
            piece = array[row][col]
            if piece in string.ascii_lowercase:
                # black piece
                piece_color=black_piece
                piece_attr = normal
            else:
                # white_piece or blank
                piece_color=white_piece
                piece_attr = bold
            screen.print_at(text=piece, x=col+board_x_offset, y=row+board_y_offset, colour=piece_color, attr=piece_attr, bg=square_color)
    return

outcomes = {
    'white': 0,
    'black': 0,
    None: 0,
}

def main(white_time=0.001, black_time=0.001):
    # engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\mwr\Downloads\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    white_engine = chess.engine.SimpleEngine.popen_uci(["./srun_stockfish.sh",
                                                        "1", "1"])
    black_engine = chess.engine.SimpleEngine.popen_uci(["./srun_stockfish.sh",
                                                        "1", "96"])
    black_engine.configure({"Threads": 96})

    win_stats = 'White wins: {0}, Black wins: {1}, Other: {2}'.format(outcomes['white'], outcomes['black'], outcomes[None])
    whose_turn = 'white'
    while True:
        with ManagedScreen() as screen:
            screen.clear()

            # Visual testing code here
            # fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            # board = fen_to_board(fen)
            # while True:
            #     board_to_asciimatic(board, screen, board_x_offset=2, board_y_offset=1)
            #     screen.refresh()

            # Real code here
            board = chess.Board()
            while not board.is_game_over():
                if whose_turn == 'white':
                    result = white_engine.play(board, chess.engine.Limit(time=white_time, depth=5))
                    whose_turn = 'black'
                else:
                    result = black_engine.play(board, chess.engine.Limit(time=black_time, depth=5))
                    whose_turn = 'white'
                board.push(result.move)
                screen.clear_buffer(screen.COLOUR_BLACK, screen.A_NORMAL, screen.COLOUR_BLACK)
                screen.print_at(win_stats, x=0, y=15, colour=screen.COLOUR_RED, bg=screen.COLOUR_BLACK)
                array = fen_to_array(board.fen())
                array_to_asciimatic(array, screen, board_x_offset=3, board_y_offset=3)
                screen.refresh()

        outcome = board.outcome()
        if outcome.winner == chess.WHITE:
            outcomes['white'] += 1
        elif outcome.winner == chess.BLACK:
            outcomes['black'] += 1
        elif outcome.winner == None:
            outcomes[None] += 1
        win_stats = 'White wins: {0}, Black wins: {1}, Other: {2}'.format(outcomes['white'], outcomes['black'], outcomes[None])
        #print(win_stats)

if __name__ == "__main__":
    ( white_time, black_time ) = ( 0.001, 0.001 )
    try:
        main(white_time, black_time)
    except KeyboardInterrupt:
        print('Interrupted')
        total_games = outcomes['white']+outcomes['black']+outcomes[None]
        wdl = 'White W/D/L percentages ({0} games): {1:.1f}/{2:.1f}/{3:.1f}'.format(total_games,100*outcomes['white']/total_games,100*outcomes['black']/total_games,100*outcomes[None]/total_games)
        print(wdl)
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)

