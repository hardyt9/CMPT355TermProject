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
1. konaneAI.py is fully executable in the command line 
2. The agent takes two arguments - filename, and colour
    - filename provides a game-board state that the agent is to use in the current game
    - colour provides the initial colour that the agent will use in play
3. Play with the agent either:
    a. by invoking the program directly using the provided arguments
    b. by utilizing the provided driver.pl function to have two agents play against one-another
        -driver.pl takes two agent programs as arguments 
    
