import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://student:student@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_question = {
            'question': 'New Question',
            'answer': 'Answer',
            'category': '1',
            'difficulty': 2
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_returned_requesting_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        data = response.json

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_category_questions(self):
        response = self.client().get('/categories/1/questions')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_404_returned_requesting_invalid_category(self):
        response = self.client().get('/categories/1000/questions')
        data = response.json
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_405_if_question_creation_is_not_allowed(self):
        response = self.client().post('/questions/100', json=self.new_question)
        data = response.json
        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'method not allowed')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()