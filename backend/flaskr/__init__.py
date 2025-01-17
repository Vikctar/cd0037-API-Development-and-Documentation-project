import random

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



database_name = 'trivia'
database_path = f'postgresql://student:student@localhost:5432/{database_name}'

db = SQLAlchemy()

from .models import Category, Question

def setup_db(app, database_path=database_path):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def get_categories():
        categories = [category.format() for category in Category.query.all()]
        results = {}
        for item in categories:
            results.update({str(item['id']): item['type']})
        return jsonify({
            'success': True,
            'categories': results
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + 10
        questions = [question.format() for question in Question.query.order_by(Question.category).all()][start:end]
        categories = [category.format() for category in Category.query.all()]
        results = {}
        for item in categories:
            results.update({str(item['id']): item['type']})
        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
            'categories': results
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id: int):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'deleted_id': question_id,
                'message': 'Question deleted'
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def new_question():
        data = request.json
        question_text = data.get('question')
        answer_text = data.get('answer')
        category = data.get('category')
        difficulty = data.get('difficulty')

        try:
            question = Question(question=question_text, answer=answer_text, category=category, difficulty=difficulty)
            question.insert()
            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search():
        data = request.json
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + 10
        search_term = data.get('searchTerm', None)
        if search_term:
            results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            questions = [question.format() for question in results][start:end]
            if len(questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(results)
            })
        abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id: int):
        questions = [question.format() for question in Question.query.filter_by(category=category_id).all()]
        current_category = Category.query.get(category_id)
        if len(questions) == 0 or current_category is None:
            abort(404)
        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': current_category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def quiz_questions():
        data = request.json
        print(data)

        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')
        category_type = quiz_category.get("type")
        category = Category.query.filter_by(type=category_type).first()

        questions = [question.format() for question in Question.query.filter_by(category=category.id).all()]
        filtered_questions = list(filter(lambda q: q['id'] not in previous_questions, questions))

        if not filtered_questions:
            return jsonify({
                'success': False,
                'question': False
            })
        question = filtered_questions[random.randint(0, len(filtered_questions) - 1)]

        return jsonify({
            'success': True,
            'question': question
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unable to process request'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app


# from . import models
