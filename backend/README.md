# Backend - Trivia API

## API Reference

### Endpoints

#### GET /categories

- Description:
    - Returns a dictionary of categories
- Sample: `curl http://localhost:5000/categories`

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### GET /questions

- Description:
    - Returns a list of question objects and categories, success value, and total number of books
    - Results are paginated in groups of 10.
    - Send an optional request argument, page with int values starting from 1.
- Sample: `curl http://localhost:5000/questions?page=1`

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```

#### DELETE /questions/{question_id}

- Description:
    - Deletes the question of the given ID if it exists.
    - Return the ID of the deleted question, success value and a message
- Sample `curl -X DELETE http://localhost:5000/questions/1`

```
{
  "success": true,
  "deleted_id": 1,
  "message": "Question deleted"
}
```

#### POST /questions

- Description:
    - Creates a new question using the request payload.
    - Returns the new question object and a success value
-
Sample `curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d {"question: "New Question", "answer": "Answer", "cateogry": "1", "difficulty": 2}`
```
{
    "success": true,
    "question": {
        "id": 1,
        "question": "New Question",
        "answer": "Answer",
        "category": "1",
        "difficulty": 2
    }
}
```
#### POST /questions/search
- Description:
  - Search for questions that contain a particular search term
  - The search term is contained in the request body
  - Returns any question for whom the search term is a substring of the question, total questions and a success value
- Sample `curl -X POST http://localhost:5000/questions/search -H "Content-Type: application/json" -d {"searchTerm": "penicillin"}`
```
{
    "questions": [
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

#### GET /categories/{category_id}/questions
- Description:
  - Fetch list of questions that belong to the given category identified by the category id
- Sample `curl http://localhost:5000/categories/4/questions`
```
{
    "currentCategory": "Science",
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "totalQuestions": 3
}
```

#### POST /quizzes
- Description:
  - Given two request params, previous questions and category, this endpoint returns a random
  - question which is not a previous question (the user has not answered it before) and is based on the given category
- Sample `curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d {"previous_questions": [1, 4], "quiz_category": 6}`
```
{
    "question": {
        "id": 1,
        "question": "Who won the world cup in 2006",
        "answer": "Italy",
        "difficulty": 2,
        "category": 6
    }
}
```

### Error Handling
Errors returned by the API use the following JSON structure
```
{
    "success": false,
    "code": <numeric error code>,
    "message": <descriptive error message>
}
```
The API returns five error types when requests fail
- 400: Bad request
- 404: Resource not found
- 405: Method not allowed
- 422: Unable to process request
- 500: Internal server error

--------------------
### End API Reference
--------------------

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in
   the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This
   keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for
   your platform can be found in
   the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by
   navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle
  requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL
  database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests
  from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data.
The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats
already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or
you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint
   should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and
   difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search
   term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous
   question parameters and return a random questions within the given category, if provided, and that is not one of the
   previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the
response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the
  category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
