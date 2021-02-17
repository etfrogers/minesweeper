
import random, time, copy
from termcolor import cprint
from os import system
from string import ascii_uppercase


def get_grid_size():
    n_of_columns = input('How many columns do you want?')
    n_of_rows = input('How many rows do you want?')
    try:
        n_of_columns = int(n_of_columns)
    except ValueError:
        n_of_columns = 0
    try:
        n_of_rows = int(n_of_rows)
    except ValueError:
        n_of_rows = 0
    if n_of_rows < 1 or n_of_rows > 99 or n_of_columns < 1 or n_of_columns > 26:
        return get_grid_size()
    else:
        return n_of_rows, n_of_columns


def get_num_of_bombs():
    grid_size = n_cols * n_rows
    numofbombs = input('Number of bombs must be between 0 and ' + str(grid_size) + '\n How many bombs do you want?')
    if numofbombs == 'q':
        quit()
    try:
        numofbombs = int(numofbombs)
    except ValueError:
        numofbombs = -1
    if numofbombs < 0 or numofbombs > grid_size:
        return get_num_of_bombs()
    else:
        return numofbombs


def clear():
    pass
    # system('cls')


def reset(numofbombs):
    print('''MAIN MENU\r\n=========\r\n\r\n-> for instructions type I\r\n-> to start playing type P''')
    choice = input('type here:').upper()
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
        reset(numofbombs)

    # The solution grid.
    # b = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    b = [[0] * n_cols] * n_rows
    for n in range(0, numofbombs):
        place_bomb(b)
    for r in range(0, n_rows):
        for c in range(0, n_cols):
            value = l(r, c, b)
            if value == '*':
                updateValues(r, c, b)
    k = [[' '] * n_cols] * n_rows
         # , ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         # [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         # [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         # [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         # [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    printBoard(k)
    starttime = time.time()
    play(b, k, starttime, numofbombs)


def place_bomb(b):
    r = random.randint(0, n_rows-1)
    c = random.randint(0, n_cols-1)
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

        if n_cols > c + 1:
            if not r[c + 1] == '*':
                r[c + 1] += 1

    # Same row.
    r = b[rn]

    if c - 1 > -1:
        if not r[c - 1] == '*':
            r[c - 1] += 1

    if n_cols > c + 1:
        if not r[c + 1] == '*':
            r[c + 1] += 1

    # Row below.
    if n_rows > rn + 1:
        r = b[rn + 1]

        if c - 1 > -1:
            if not r[c - 1] == '*':
                r[c - 1] += 1

        if not r[c] == '*':
            r[c] += 1

        if n_cols > c + 1:
            if not r[c + 1] == '*':
                r[c + 1] += 1


def l(r, c, b):
    row = b[r]
    c = row[c]
    return c


def printBoard(k):   # , n_cols, n_rows):
    clear()
    header = ascii_uppercase[0:n_cols]
    print('     ' + '   '.join(header))
    print('   ╔══'+'═╦══' * (n_cols-1)+'═╗')
    for r in range(0, n_rows):
        entries = [str(l(r, i, k)) for i in (range(n_cols))]
        if r < 10:
            spacing = ' '
        else:
            spacing = ''
        print(spacing + str(r), '║', ' ║ '.join(entries), '║')
        if not r == n_rows -1:
            print('   ╠══'+'═╬══' * (n_cols-1)+'═╣')
    print('   ╚══'+'═╩══' * (n_cols -1) +'═╝')


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
    for x in range(0, n_rows):
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
        if chosen == 'q':
            quit()
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
        for x in range(n_rows):
            for y in range(n_cols):
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
        if n_cols > c + 1:
            row[c + 1] = l(r - 1, c + 1, b)
        row = k[r-1]
        if c-1 > -1:
            row[c-1] = l(r-1, c-1, b)
        row[c] = l(r-1, c, b)
        if n_cols > c+1:
            row[c+1] = l(r-1, c+1, b)
    # Same row
    row = k[r]
    if c - 1 > -1:
        row[c - 1] = l(r, c - 1, b)
    if n_cols > c + 1:
        row[c + 1] = l(r, c + 1, b)
    # Row below
    if n_rows > r + 1:
        row = k[r + 1]
        if c - 1 > -1: row[c - 1] = l(r + 1, c - 1, b)
        row[c] = l(r + 1, c, b)
        if n_cols > c + 1: row[c + 1] = l(r + 1, c + 1, b)


cprint('Welcome to mine sweeper!\r\n=======================', 'blue')
cprint('By Alex', 'blue')

n_rows, n_cols = get_grid_size()
numofbombs = get_num_of_bombs()
reset(numofbombs)



