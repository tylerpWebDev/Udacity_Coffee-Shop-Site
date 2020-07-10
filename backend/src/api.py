import os  
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import asyncio
from flask_cors import CORS
from functools import wraps

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, check_auth


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



def cprint(string1, string2):
    print("=========================")
    print("")
    print(string1)
    print(string2)
    print("")
    print("=========================")



# ROUTES
@app.route('/headers', methods=["GET"])
@check_auth('get:drinks')
def headers(token):
    return 'token'


'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++ GET /drinks - Completed  +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


@app.route('/drinks', methods=["GET"])
@check_auth('get:drinks')
def get_public_drinks(payload):
    try:
        drinks = Drink.query.all()
    except:
        abort(401)
    finally:
        return json.dumps({"success": True, "drinks": [drink.short() for drink in drinks]})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++ GET /drinks-detail - WIP  +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

# Add permissions once route works


@app.route('/drinks-detail', methods=["GET"])
@check_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
    except:
        abort(401)
    finally:
        return json.dumps({"success": True, "drinks": [drink.long() for drink in drinks]})





'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''



@app.route('/drinks', methods=["POST"])
@check_auth('post:drinks')
def create_new_drink(payload):
    req_body = json.loads(request.data.decode("utf-8"))
    cprint("post new drink: req-body", req_body)

    new_drink = Drink(
        title=req_body["title"],
        recipe=str(req_body["recipe"])
        )
    try:
        new_drink.insert()
    except:
        abort(401)
    finally: 
        return jsonify({"success": True, "drinks": new_drink.long()})



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

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@check_auth('patch:drinks')
def update_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        req_data = json.loads(request.data.decode("utf-8"))
        drink.title = req_data["title"]
        drink.recipe = str(req_data["recipe"])
        drink.update()
    except:
        abort(401)
    finally:
        drink = [Drink.query.filter(Drink.id == drink_id).one_or_none()]
        return json.dumps({"success": True, "drinks": [drink.short() for drink in drink]})


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


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@check_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        Drink.query.get(drink_id).delete()
        db.session.commit()
    except:
        abort(401)
    finally:
        return jsonify({"success": True, "delete": drink_id})


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
