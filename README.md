# PyKnight

![python](https://img.shields.io/badge/python-3.13-blue) ![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5.6-green)

![pyknight](assets/brand/name400.png)

A customizable chess game I made in Python as a solo hobby project.

The goal of this project was to design & implement a complete chess game without using external chess libraries.

![preview1](assets/images/image1.png)

## Features

### Pygame UI
- Two boards for both perspectives
- Interactive controls
- Multiple piece sets
- Multiple board palettes

### Engine
- Legal move validation for all pieces
- Check, checkmate, stalemate
- Pawn promotion
- Castling
- En passant
- Undoing moves
- Save & load functionality

## How to Run
1. Click on **Code**, then **Download ZIP** on this repository.
2. Extract the ZIP file to a folder.
3. If you don't have Pygame installed:
    - Open a terminal and navigate into the extracted folder: `cd extracted/folder/path`
    - Install the required packages: `pip install -r requirements.txt`
4. Open the folder and run `main.py`.
    - Alternatively, run `main.pyw` to run the game without terminal (only on Windows).

## How to Run (Alternative)
1. Clone the repository: `git clone https://github.com/Leshiro/py-knight`
2. Navigate into the project folder: `cd py-knight`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the game: `python main.py`

## Built With
- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)

## Might Add Later
- Remove global state variables & switch to `State` class object
- Split save/load functions to separate file
- Piece points indicator
- Better window scaling, window resizing, top panel, minimize option
- Bot match
- Online matchmaking
- User accounts, elo system etc.
