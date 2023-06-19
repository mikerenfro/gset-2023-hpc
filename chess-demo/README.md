# HPC Stockfish demo

## Installation

Requires
Python 3.7+ because of python-chess library,
MPI build of Stockfish from cluster branch of Stockfish GitHub repository,
Slurm in an HPC environment.

1. Run `pip install -r requirements.txt` to install python-chess and asciimatics
2. Edit `srun_stockfish.sh` to adjust `srun` parameters for your environment.
3. Edit `chess_demo.py` to adjust time limits, thread settings, etc.

## Running

Run `python chess_demo.py white_nodes white_threads_per_node black_nodes black_threads_per_node` (e.g., `python chess_demo.py 1 1 5 4`).
It should start two jobs via `srun` with different node and core counts,
one playing white and the other playing black.
You'll also see a white/green chessboard showing the piece positions,
and a running total of how many games have been won by white, black, or neither.
Hit Ctrl-C to cancel the jobs, the script, and get a final tally of the outcomes.
