# Qwixx

Qwixx is a fast-paced dice game where players try to mark off as many numbers as possible in four different colored rows.
Each row consists of numbers that players attempt to cross off in sequence, trying to score the highest points.


## Game Rules

1. **Setup**: 
    - The game consists of a scoresheet with four rows, each a different color (red, yellow, green, blue).
    - Each row has numbers ranging from 2 to 12 (red and yellow) or from 12 to 2 (green and blue).

2. **Gameplay**:
    - The game is played with six dice: two white dice and one die for each color (red, yellow, green, blue).
    - On each turn, the active player rolls all six dice.
    - All players can use the sum of the two white dice to mark off a number in any row. This is the "common" action.
    - The active player can also choose to combine one of the white dice with one of the colored dice to mark off a number in the row corresponding to the color of the die.
    - If a player decides to not cross off any numbers, they accumulate a penalty.
    - Numbers must be marked off from left to right. You can skip numbers, but you cannot go back once a number is skipped.

3. **Locking a Row**:
    - If a player marks off at least five numbers in a row, they can lock that row by marking the last number (12 for red/yellow, 2 for green/blue).
    - As soon as a row is locked, the corresponding dice is removed from the game.
    - Once a row is locked, no other players can mark off numbers in that row after that turn.

4. **End of Game**:
    - The game ends when either two rows are locked or one player marks their fourth penalty.
    - Players then tally their points based on how many numbers they have marked in each row, minus penalties.

## Installation

**Clone the repository**:
```bash
git clone https://github.com/jenzah/qwixx.git
cd qwixx
```

## Usage

**To start the game, run the following command:**
```bash
python qwixx.py
```
