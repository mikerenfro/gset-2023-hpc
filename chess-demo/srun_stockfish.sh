#!/bin/bash
srun --nodes=$1 --cpus-per-task=$2 ./stockfish
