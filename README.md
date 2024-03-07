# Konane Playing AI Agent

This repository contains an implementation of a Konane playing AI agent. Konane is a strategy board game.

## Introduction
Konane is a two-player game played on a rectangular grid. The objective of the game is to "leap-frog" over your opponent's pieces, similar to a checkers game. However, the twist is that unlike regular checkers, the winning player is not the one with the most pieces but the one who doesn't run out of legal moves.

## Features
- **Minimax Algorithm**: The AI agent uses the Minimax algorithm along with Alpha-Beta Pruning to search for the optimal move.
- **Heuristic Evaluation**: A custom heuristic function serves to evaluate the game state and determine a desirable move.
- **Alpha-Beta Pruning**: Due to additional time constraints in the game, Alpha-Beta Pruning serves to improve efficiency in decision-making.

## Installation
1. Clone repository to local machine:
    ```bash
    git clone (repository)
    ```

2. Install dependencies:
    - IDE
    - Python
    - pip

## Using the agent 
1. konaneAI.py is fully executable in the command line without compiling
    - a shebang line is included in the first line of the code to invoke the Python interpreter
3. The agent takes two arguments - filename, and colour
    - filename is the game-board state that the agent is to use in the current game
    - colour is the initial colour that the agent will use in play
4. Play with the agent either:
    - by invoking the program directly using the provided arguments
    - by utilizing the provided driver.pl function to have two agents play against one-another
        -driver.pl takes two agent programs as arguments and must have knmv present as well
    
## Included in this directory
There are two files total:
1. konaneAITeam8.py - the playing agent to be used as mentioned above
2. readme.txt - a file specifying the directory structure and instructions on using the agent

## Not included in this directory
1. drivercheck.pl - takes two agents as arguments that will play against one-another using a freshly created game
2. knmv - used within drivercheck.pl to check game status and validity of moves
