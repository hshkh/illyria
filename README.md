# Illyria: An Artificially Intelligent Two-Player Game Engine

Project supervisor: [Prof. Frederic Fol Leymarie](http://www.folleymarie.com/)

## About
Developing an artificially intelligent program that can play optimally in a game of English draughts.

## Algorithms
- Standard Minimax Algorithm
- Minimax Algorithm with Alpha-Beta Pruning

## Running the game
1. Install `pygame` package using `pip`,
    ```
    $ pip3 install pygame 
    ```

2. Navigate to `illyria/` and run `main.py`.

3. **Command Line Arguments:** To spectate a game between two instances of the computer,
    ```
    $ python main.py -g s
    ```
    or to play,
    ```
    $ python main.py -g p
    ```
    Note: you will need Python 3.
