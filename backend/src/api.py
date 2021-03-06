import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json
    {
        "success": True,
        "drinks": drinks
    }
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_public_drinks():
    all_drinks = Drink.query.all()
    drinks = []

    if len(all_drinks) == 0:
        return jsonify({
            "status": 200,
            "success": True,
            "drinks": drinks
        }), 200

    for each_drink in all_drinks:
        short_info = each_drink.short()
        drinks.append(short_info)

    return jsonify({
        "status": 200,
        "success": True,
        "drinks": drinks
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {
        "success": True,
        "drinks": drinks
    }
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    all_drinks = Drink.query.all()

    drinks = []
    for each_drink in all_drinks:
        long_detail = each_drink.long()
        drinks.append(long_detail)

    return jsonify({
        "status": 200,
        "success": True,
        "drinks": drinks
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {
        "success": True,
        "drinks": drink
    }
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    data = request.get_json()
    if 'title' not in data:
        abort(422)
    if 'recipe' not in data:
        abort(422)

    new_title = data.get('title')
    new_recipe = data.get('recipe')

    if new_title is None:
        abort(400)
    if new_recipe is None:
        abort(400)
    print(new_recipe)

    # recipeJSON = getJSONListFromObject(recipe)

    try:
        new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        new_drink.insert()
        drink = new_drink.long()

        return jsonify({
            "status": 200,
            "success": True,
            "drinks": drink
        }), 200
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {
        "success": True,
        "drinks": drink
    }
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt, id):
    update_drink = Drink.query.get(id)
    if update_drink is None:
        abort(404)

    data = request.get_json()
    if "title" in data:
        update_drink.title = data.get('title')

    if "recipe" in data:
        recipe = data.get('recipe')
        update_drink.recipe = recipe

    try:
        update_drink.update()
        drink = []
        drink.append(update_drink.long())
        return jsonify({
            "status": 200,
            "success": True,
            "drinks": drink
        }), 200
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json
    {
        "success": True,
        "delete": id
    }
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, id):
    delete_drink = Drink.query.get(id)
    if delete_drink is None:
        abort(404)

    id = delete_drink.id
    try:
        delete_drink.delete()
        return jsonify({
            "status": 200,
            "success": True,
            "delete": id
        }), 200
    except Exception:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def processAuthError(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code

    return jsonify({
                    "success": False,
                    "error": status_code,
                    "message": message
                    }), status_code
