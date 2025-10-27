from flask import Flask, render_template, request, jsonify
import random
import os
from dotenv import load_dotenv

load_dotenv()  # in case you use API keys later

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

def check_winner(board):
    combos = [(0,1,2),(3,4,5),(6,7,8),
              (0,3,6),(1,4,7),(2,5,8),
              (0,4,8),(2,4,6)]
    for a,b,c in combos:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def ai_move(board, ai_symbol, difficulty):
    empty = [i for i, v in enumerate(board) if v == '']
    if not empty:
        return board

    if difficulty == 'easy':
        move = random.choice(empty)

    elif difficulty == 'medium':
        # Try to win, else random
        for i in empty:
            test = board[:]
            test[i] = ai_symbol
            if check_winner(test) == ai_symbol:
                move = i
                break
        else:
            move = random.choice(empty)

    else:  # hard - block opponent or win
        opponent = 'O' if ai_symbol == 'X' else 'X'
        # Try to win
        for i in empty:
            test = board[:]
            test[i] = ai_symbol
            if check_winner(test) == ai_symbol:
                move = i
                break
        else:
            # Try to block
            for i in empty:
                test = board[:]
                test[i] = opponent
                if check_winner(test) == opponent:
                    move = i
                    break
            else:
                move = random.choice(empty)

    board[move] = ai_symbol
    return board

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    player_symbol = data['player_symbol']
    ai_symbol = data['ai_symbol']
    difficulty = data['difficulty']

    # Player already made their move in board array
    winner = check_winner(board)
    if winner:
        return jsonify({'board': board, 'winner': winner})

    # AI move
    board = ai_move(board, ai_symbol, difficulty)
    winner = check_winner(board)
    draw = all(cell != '' for cell in board) and not winner

    return jsonify({'board': board, 'winner': winner, 'draw': draw})

if __name__ == '__main__':
    app.run(debug=True)
