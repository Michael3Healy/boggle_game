from flask import Flask, request, render_template, redirect, session, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'boggleisgood'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def display_board():
    '''Home page displaying board, score, and timer. Retrieves/initializes highScore and timesPlayed in session'''
    
    board = boggle_game.make_board()
    session['board'] = board
    session['highScore'] = session.get('highScore', 0)
    session['timesPlayed'] = session.get('timesPlayed', 0)

    return render_template('board.html', board=board)


@app.route('/guess')
def receive_guess():
    '''Receives post request containing guess from user and returns if it is a valid word'''
    
    guess = request.args['guess']
    board = session['board']
    word_validity = boggle_game.check_valid_word(board, guess)
    return jsonify({'result': word_validity})

@app.route('/end-game', methods=['POST'])
def recieve_scores():
    '''Receives post request containing game score, updates timesPlayed and highScore in session.'''

    score = request.json['score']
    session['timesPlayed'] = session.get('timesPlayed') + 1
    high_score = session.get('highScore')
    best_score = max(score, high_score)
    session['highScore'] = best_score

    return jsonify({'highScore': best_score})








