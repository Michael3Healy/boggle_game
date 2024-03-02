from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle



class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_board_display(self):
        with self.client:
            resp = self.client.get('/')
            html = resp.get_data(as_text=True)

            # Returns correct status code and html, adds correct number of rows to board
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="col text-center fs-1">', html)
            self.assertIn('Guess: </label>', html)
            self.assertEqual(len(session['board']), 5)

    def test_valid_word(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"]]

            resp = self.client.get('/guess', query_string={'guess': 'cat'})
            
            # Returns 'ok' for valid guesses
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')

    def test_word_not_on_board(self):
        with self.client:
            # Request homepage so that board is made and saved in session
            self.client.get('/')
            resp = self.client.get('/guess', query_string={'guess': 'invalid'})

            # Returns 'not-on-board' for words that aren't on the board
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-on-board')

    def test_not_a_word(self):
        with self.client:

            self.client.get('/')
            resp = self.client.get('/guess', query_string={'guess': 'alsdkf'})

            # returns not-word for invalid words
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')

    def test_stat_updates(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['highScore'] = 0
                sess['timesPlayed'] = 0

            resp = self.client.post('/end-game', json={'score': 2})
        
            # Updates timesPlayed and highScore in session upon end of game
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['timesPlayed'], 1)
            self.assertEqual(session['highScore'], 2)

        

