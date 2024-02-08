# Konane Playing AI Agent

This repository contains an implementation of a Konane playing AI agent. Konane is a strategy board game.

## Introduction
Konane is a two-player game played on a rectangular grid. The objective of the game is to "leap-frog" over your opponent's pieces, similar to a checkers game. However, the twist is that unlike regular checkers, the winning player is not the one with the most pieces but the one who doesn't run out of legal moves.

## Features
- **Minimax Algorithm**: The AI agent uses the Minimax algorithm along with Alpha-Beta Pruning to search for the most optimal move.
- **Heuristic Evaluation**: A custom heuristic function serves to evaluate the game state and determine a desirable move.
- **Alpha-Beta Pruning**: Due to additional time constraints in the game, Alpha-Beta Pruning serves to improve efficiency in decision-making.
- **Graphical Interface**: A graphical user interface (GUI) is implemented to allow users to play against the AI.

## Installation
1. Clone repository to local machine:
    ```bash
    git clone (repository)
    ```

2. Install dependencies:
    - IDE
    - Python
    - pip

3. Run program 
    run make to create executable named konane
    ./konane to create instance of game play
    
This project is a group effot based off of elments learned in our CMPT 355 - AI course, should be fun!