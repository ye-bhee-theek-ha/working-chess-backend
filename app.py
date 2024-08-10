from flask import Flask, request, jsonify
import chess
from src.minimax import Minimax
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    return "hello world"
@app.route('/next_move', methods=['POST'])
def next_move():
    data = request.json
    fen = data.get('fen')
    difficulty = data.get('difficulty', 2)

    if not fen:
        return jsonify({'error': 'FEN string is required'}), 400

    try:
        board = chess.Board(fen)
    except ValueError:
        return jsonify({'error': 'Invalid FEN string'}), 400

    move, new_board, time = Minimax.main(board, difficulty, 15)

    if move is None:
        return jsonify({'error': 'Game over'}), 400

    return jsonify({'move': str(move), 'new_fen': new_board.fen(), 'time': str(time)})

if __name__ == '__main__':
    app.run(debug=True)
    