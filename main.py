
import random, time, copy
from termcolor import cprint
from os import system


def get_num_of_bombs(numofbombs):
    if numofbombs < 0 or numofbombs > 81:
        numofbombs = input('Number of bombs must be between 0 and 81 \n How many bombs do you want?')
        try:
            numofbombs = int(numofbombs)
        except ValueError:
            numofbombs = -1
        numofbombs = get_num_of_bombs(numofbombs)
    return numofbombs


def clear():
    system('cls')


def reset(numofbombs):
    print('''MAIN MENU\r\n=========\r\n\r\n-> for instructions type I\r\n-> to start playing type P''')
    choice = input('type here:').upper()

    if choice == 'I':
        clear()

        print(open('instructions.txt', 'r').read())
        input('press [enter]when ready to play')

    elif choice != 'P':
        clear()
        reset(numofbombs)

    # The solution grid.
    b = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for n in range(0, numofbombs):
        place_bomb(b)
    for r in range(0, 9):
        for c in range(0, 9):
            value = l(r, c, b)
            if value == '*':
                updateValues(r, c, b)
    k = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    printBoard(k)
    starttime = time.time()
    play(b, k, starttime, numofbombs)


def place_bomb(b):
    r = random.randint(0, 8)
    c = random.randint(0, 8)
    currentrow = b[r]
    if not currentrow[c] == '*':
        currentrow[c] = '*'
    else:
        place_bomb(b)


def updateValues(rn, c, b):
    if rn - 1 > -1:
        r = b[rn - 1]

        if c - 1 > -1:
            if not r[c - 1] == '*':
                r[c - 1] += 1

        if not r[c] == '*':
            r[c] += 1

        if 9 > c + 1:
            if not r[c + 1] == '*':
                r[c + 1] += 1

    # Same row.
    r = b[rn]

    if c - 1 > -1:
        if not r[c - 1] == '*':
            r[c - 1] += 1

    if 9 > c + 1:
        if not r[c + 1] == '*':
            r[c + 1] += 1

    # Row below.
    if 9 > rn + 1:
        r = b[rn + 1]

        if c - 1 > -1:
            if not r[c - 1] == '*':
                r[c - 1] += 1

        if not r[c] == '*':
            r[c] += 1

        if 9 > c + 1:
            if not r[c + 1] == '*':
                r[c + 1] += 1


def l(r, c, b):
    row = b[r]
    c = row[c]
    return c


def printBoard(k):
    clear()
    print('    A   B   C   D   E   F   G   H   I')
    print('  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
    for r in range(0, 9):
        print(r, '║', l(r, 0, k), '║', l(r, 1, k), '║', l(r, 2, k), '║', l(r, 3, k), '║', l(r, 4, k), '║', l(r, 5, k), '║',
          l(r, 6, k), '║', l(r, 7, k), '║', l(r, 8, k), '║')
    if not r == 8:
        print('  ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
    print('  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝')


def play(b, k, starttime, numofbombs):
    c, r = choose(b, k, starttime)
    v = l(r, c, b)
    if v == '*':
        printBoard(b)
        cprint('you lose', 'red')
        print('Time: ' + str(round(time.time() - starttime)) + 's')
        playagain = input('Play again? (Y/N): ').lower()
        if playagain == 'y':
            clear()
            reset(numofbombs)
        else:
            quit()
    k[r][c] = v
    if v == 0:
        checkZeros(k, b, r, c)
    printBoard(k)
    squaresLeft = 0
    for x in range(0, 9):
        row = k[x]
        squaresLeft += row.count(' ')
        squaresLeft += row.count('⚐')
    if squaresLeft == numofbombs:
        cprint('You win!', 'green')
        print('Time: ' + str(round(time.time() - starttime)) + 's')
        playAgain = input('Play again? (Y/N): ')
        playAgain = playAgain.lower()
        if playAgain == 'y':
            clear()
            reset(numofbombs)
        else:
            quit()
    play(b, k, starttime, numofbombs)


def choose(b, k, starttime):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    while True:
        chosen = input('Choose a square (eg. E4) or place a marker (eg. mE4): ').lower()
        if len(chosen) == 3 and chosen[0] == 'm' and chosen[1] in letters and chosen[2] in numbers:
            c, r = (ord(chosen[1])) - 97, int(chosen[2])
            marker(r, c, k)
            play(b, k, starttime, numofbombs)
            break
        elif len(chosen) == 2 and chosen[0] in letters and chosen[1] in numbers:
            choose.n_invalid_guesses = 0
            return (ord(chosen[0])) - 97, int(chosen[1])
        else:
            choose.n_invalid_guesses += 1
            if choose.n_invalid_guesses == 10:
                quit()
            return choose(b, k, starttime)


choose.n_invalid_guesses = 0


def marker(r, c, k):
    k[r][c] = '⚐'
    printBoard(k)


def checkZeros(k, b, r, c):
    oldGrid = copy.deepcopy(k)
    zeroProcedure(r, c, k, b)
    if oldGrid == k:
        return
    while True:
        oldGrid = copy.deepcopy(k)
        for x in range(9):
            for y in range(9):
                if l(x, y, k) == 0:
                    zeroProcedure(x, y, k, b)
        if oldGrid == k:
            return


def zeroProcedure(r, c, k, b):
    # Row above
    if r - 1 > -1:
        row = k[r - 1]
        if c - 1 > -1:
            row[c - 1] = l(r - 1, c - 1, b)
        row[c] = l(r - 1, c, b)
        if 9 > c + 1:
            row[c + 1] = l(r - 1, c + 1, b)
        row = k[r-1]
        if c-1 > -1:
            row[c-1] = l(r-1, c-1, b)
        row[c] = l(r-1, c, b)
        if 9 > c+1:
            row[c+1] = l(r-1, c+1, b)
    # Same row
    row = k[r]
    if c - 1 > -1:
        row[c - 1] = l(r, c - 1, b)
    if 9 > c + 1:
        row[c + 1] = l(r, c + 1, b)
    # Row below
    if 9 > r + 1:
        row = k[r + 1]
        if c - 1 > -1: row[c - 1] = l(r + 1, c - 1, b)
        row[c] = l(r + 1, c, b)
        if 9 > c + 1: row[c + 1] = l(r + 1, c + 1, b)


cprint('Welcome to mine sweeper!\r\n=======================', 'blue')
cprint('By Alex', 'blue')

# numofbombs = input('How many bombs do you want?')
# numofbombs = int(numofbombs)
numofbombs = get_num_of_bombs(-1)

reset(numofbombs)


# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
#print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#print_hi('PyCharm')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

