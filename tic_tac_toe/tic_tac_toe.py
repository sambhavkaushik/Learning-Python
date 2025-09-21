import math

# ------------------------
# Tic Tac Toe with AI
# ------------------------
# Player: X
# Computer (AI): O
# Minimax algorithm for AI

board = [" " for _ in range(9)]  # 3x3 board stored in 1D list

def print_board():
    print("\n")
    for row in [board[i:i+3] for i in range(0, 9, 3)]:
        print("| " + " | ".join(row) + " |")
    print("\n")

def available_moves():
    return [i for i, spot in enumerate(board) if spot == " "]

def winner(b, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]            # diagonals
    ]
    return any(all(b[i] == player for i in combo) for combo in win_conditions)

def is_draw():
    return " " not in board

def minimax(b, depth, is_maximizing):
    if winner(b, "O"):  # AI wins
        return 1
    elif winner(b, "X"):  # Player wins
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves():
            b[move] = "O"
            score = minimax(b, depth+1, False)
            b[move] = " "
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves():
            b[move] = "X"
            score = minimax(b, depth+1, True)
            b[move] = " "
            best_score = min(best_score, score)
        return best_score

def ai_move():
    best_score = -math.inf
    best_move = None
    for move in available_moves():
        board[move] = "O"
        score = minimax(board, 0, False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move] = "O"

def play():
    print("Welcome to Tic Tac Toe! (You = X, Computer = O)")
    print_board()

    while True:
        # Player move
        try:
            move = int(input("Choose your move (1-9): ")) - 1
            if move not in available_moves():
                print("Invalid move. Try again.")
                continue
        except ValueError:
            print("Enter a number between 1 and 9.")
            continue

        board[move] = "X"
        print_board()

        if winner(board, "X"):
            print("🎉 You win!")
            break
        elif is_draw():
            print("It's a draw!")
            break

        # AI move
        print("Computer is thinking...")
        ai_move()
        print_board()

        if winner(board, "O"):
            print("💻 Computer wins!")
            break
        elif is_draw():
            print("It's a draw!")
            break

if __name__ == "__main__":
    play()
