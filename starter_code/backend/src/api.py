import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import asyncio
from flask_cors import CORS
from functools import wraps

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

async def wait_for_db(request):
    data = await request()
    return data


def get_auth_token():
    if 'Authorization' not in request.headers:
        abort(401)

    auth_header_full = request.headers['Authorization']
    auth_header_split = auth_header_full.split(" ")

    if len(auth_header_split) != 2:
        abort(401)

    if auth_header_split[0].lower() != 'bearer':
        abort(401)

    header_token = auth_header_split[1]

    return header_token


def check_auth(routef):
    @wraps(routef)
    def wrapper(*args1, **args2):
        token = get_auth_token()
        return routef(token, *args1, **args2)
    return wrapper


# ROUTES
@app.route('/headers', methods=["GET"])
@check_auth
def headers(token):
    return 'not implemented'


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=["GET"])
def get_public_drinks():
    try:
        drinks = wait_for_db(Drink.query.all())
        response_object = json.dumps({"success": True, "drinks": drinks})
    except:
        abort(401)
    finally:
        return response_object
        # return json.dumps({"success": True, "drinks": drinks})


    # try:
    #     drinks = Drink.query.all()
    #     return str({"success": True, "drinks": drinks})
    # except Error as e:
    #     print("Error:")
    #     print(e)
    #     abort(401)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


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


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
