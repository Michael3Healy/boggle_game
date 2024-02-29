from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'boggleisgood'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def display_board():
    board = boggle_game.make_board()
    session['board'] = board

    return render_template('board.html', board=board)

@app.route('/guess', methods=['POST'])
def receive_guess():
    guess = request.form.get('guess')
    return render_template('/test.html')



