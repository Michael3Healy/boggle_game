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
            with self.client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"]]

            resp = self.client.get('/guess', query_string={'guess': 'cat'})
            
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')

    def test_word_not_on_board(self):
        with self.client:
            # Request homepage so that board is made and saved in session
            self.client.get('/')
            resp = self.client.get('/guess', query_string={'guess': 'invalid'})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-on-board')

    def test_not_a_word(self):
        with self.client:

            self.client.get('/')
            resp = self.client.get('/guess', query_string={'guess': 'alsdkf'})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')

        

