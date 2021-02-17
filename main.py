
import copy
import random
import time
from os import system
from string import ascii_uppercase

from termcolor import cprint

N_COLS = N_ROWS = 0


def get_grid_size():
    n_of_columns = input('-> How many columns do you want?')
    n_of_rows = input('-> How many rows do you want?')
    n_of_columns = integer_or_negative(n_of_columns)
    n_of_rows = integer_or_negative(n_of_rows)
    if n_of_rows < 1 or n_of_rows > 100 or n_of_columns < 1 or n_of_columns > 26:
        return get_grid_size()
    else:
        return n_of_rows, n_of_columns


def get_num_of_bombs():
    grid_size = N_COLS * N_ROWS
    numofbombs = input('-> Number of bombs must be between 0 and ' + str(grid_size) + '\n-> How many bombs do you want?')
    if numofbombs == 'q':
        quit()
    numofbombs = integer_or_negative(numofbombs)
    if numofbombs < 0 or numofbombs > grid_size:
        return get_num_of_bombs()
    else:
        return numofbombs


def integer_or_negative(int_string):
    try:
        int_string = int(int_string)
    except ValueError:
        int_string = -1
    return int_string


def clear():
    pass
    # system('cls')


def reset():
    print('MAIN MENU\r\n=========')
    print('''\r\n-> for instructions type I\r\n-> to start playing type P''')
    choice = input('type here:').upper()
    global N_ROWS, N_COLS
    N_ROWS, N_COLS = get_grid_size()
    n_bombs = get_num_of_bombs()
    if choice == 'Q':
        quit()
    if choice == 'I':
        clear()
        print(open('instructions.txt', 'r').read())
        ready = input('press [enter]when ready to play').lower()
        if ready == 'q':
            quit()
    elif choice != 'P':
        clear()
        reset()
    # The solution grid.
    b = [([0] * N_COLS).copy() for _ in range(N_ROWS)]
    for n in range(0, n_bombs):
        place_bomb(b)
    for r in range(0, N_ROWS):
        for c in range(0, N_COLS):
            value = l(r, c, b)
            if value == '*':
                updateValues(r, c, b)
    k = [([' '] * N_COLS).copy() for _ in range(N_ROWS)]
    printBoard(k)
    starttime = time.time()
    play(b, k, starttime, n_bombs)
    return n_bombs, N_COLS, N_ROWS


def place_bomb(b):
    r = random.randint(0, N_ROWS - 1)
    c = random.randint(0, N_COLS - 1)
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

        if N_COLS > c + 1:
            if not r[c + 1] == '*':
                r[c + 1] += 1

    # Same row.
    r = b[rn]

    if c - 1 > -1:
        if not r[c - 1] == '*':
            r[c - 1] += 1

    if N_COLS > c + 1:
        if not r[c + 1] == '*':
            r[c + 1] += 1

    # Row below.
    if N_ROWS > rn + 1:
        r = b[rn + 1]

        if c - 1 > -1:
            if not r[c - 1] == '*':
                r[c - 1] += 1

        if not r[c] == '*':
            r[c] += 1

        if N_COLS > c + 1:
            if not r[c + 1] == '*':
                r[c + 1] += 1


def l(r, c, b):
    row = b[r]
    c = row[c]
    return c


def printBoard(k):   # , n_cols, n_rows):
    clear()
    header = ascii_uppercase[0:N_COLS]
    print('     ' + '   '.join(header))
    print('   ╔══' +'═╦══' * (N_COLS - 1) + '═╗')
    for r in range(0, N_ROWS):
        entries = [str(l(r, i, k)) for i in (range(N_COLS))]
        if r < 10:
            spacing = ' '
        else:
            spacing = ''
        print(spacing + str(r), '║', ' ║ '.join(entries), '║')
        if not r == N_ROWS - 1:
            print('   ╠══' +'═╬══' * (N_COLS - 1) + '═╣')
    print('   ╚══' +'═╩══' * (N_COLS - 1) + '═╝')


def play(b, k, starttime, n_bombs):
    c, r = choose(b, k, starttime, n_bombs)
    v = l(r, c, b)
    if v == '*':
        printBoard(b)
        cprint('you lose', 'red')
        print('Time: ' + str(round(time.time() - starttime)) + 's')
        playagain = input('Play again? (Y/N): ').lower()
        if playagain == 'y':
            clear()
            reset()
        else:
            quit()
    k[r][c] = v
    if v == 0:
        checkZeros(k, b, r, c)
    printBoard(k)
    squaresLeft = 0
    for x in range(0, N_ROWS):
        row = k[x]
        squaresLeft += row.count(' ')
        squaresLeft += row.count('⚐')
    if squaresLeft == n_bombs:
        cprint('You win!', 'green')
        print('Time: ' + str(round(time.time() - starttime)) + 's')
        playAgain = input('Play again? (Y/N): ')
        playAgain = playAgain.lower()
        if playAgain == 'y':
            clear()
            reset()
        else:
            quit()
    play(b, k, starttime, n_bombs)


def choose(b, k, starttime, n_bombs):
    n_in_key = 0
    letters = ascii_uppercase[0:N_COLS]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    while True:
        chosen = input('Choose a square (eg. E4) or place a marker (eg. #E4): ').upper()
        if chosen == 'Q':
            quit()
        if len(chosen) >= 1 and chosen[0] == '#':
            mark = True
            chosen = chosen[1:]
        else:
            mark = False

        invalid = False
        row = -1
        col = -1
        if len(chosen) >= 1 and chosen[0] in letters:
            col_label = chosen[0]
            col = letters.index(col_label)
            row_label = chosen[1:]
            row = integer_or_negative(row_label)
        else:
            invalid = True

        if invalid or row < 0 or row >= N_ROWS:
            choose.n_invalid_guesses += 1
            if choose.n_invalid_guesses == 10:
                quit()
            return choose(b, k, starttime, n_bombs)
        choose.n_invalid_guesses = 0
        if mark:
            marker(row, col, k)
            play(b, k, starttime, n_bombs)
        return col, row


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
        for x in range(N_ROWS):
            for y in range(N_COLS):
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
        if N_COLS > c + 1:
            row[c + 1] = l(r - 1, c + 1, b)
        row = k[r-1]
        if c-1 > -1:
            row[c-1] = l(r-1, c-1, b)
        row[c] = l(r-1, c, b)
        if N_COLS > c+1:
            row[c+1] = l(r-1, c+1, b)
    # Same row
    row = k[r]
    if c - 1 > -1:
        row[c - 1] = l(r, c - 1, b)
    if N_COLS > c + 1:
        row[c + 1] = l(r, c + 1, b)
    # Row below
    if N_ROWS > r + 1:
        row = k[r + 1]
        if c - 1 > -1: row[c - 1] = l(r + 1, c - 1, b)
        row[c] = l(r + 1, c, b)
        if N_COLS > c + 1: row[c + 1] = l(r + 1, c + 1, b)


cprint('Welcome to mine sweeper!\r\n=======================', 'blue')
cprint('By Alex', 'blue')

reset()



