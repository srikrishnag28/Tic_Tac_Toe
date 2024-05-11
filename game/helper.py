def checkWin(board):
    if board['0'] == board['1'] and board['1'] == board['2'] and board['0'] != '':
        return board['0']
    if board['3'] == board['4'] and board['4'] == board['5'] and board['3'] != '':
        return board['3']
    if board['6'] == board['7'] and board['7'] == board['8'] and board['6'] != '':
        return board['6']
    if board['0'] == board['3'] and board['3'] == board['6'] and board['0'] != '':
        return board['0']
    if board['1'] == board['4'] and board['4'] == board['7'] and board['1'] != '':
        return board['1']
    if board['2'] == board['5'] and board['5'] == board['8'] and board['2'] != '':
        return board['2']
    if board['0'] == board['4'] and board['4'] == board['8'] and board['0'] != '':
        return board['0']
    if board['2'] == board['4'] and board['4'] == board['6'] and board['2'] != '':
        return board['2']
    return None


def checkDraw(board):
    for letter in board:
        if board[letter] == "":
            return False
    return True
