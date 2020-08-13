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
CORS(app, resources={r"/*": {"origins": "*"}})

'''
    Uncomment the following line to initialize the datbase
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
+++++++++++++++++++++++++++++++++ GET /drinks  +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


@app.route('/drinks', methods=["GET"])
def get_public_drinks():
    try:
        drinks = Drink.query.all()
    except BaseException:
        abort(401)
    finally:
        return json.dumps({"success": True, "drinks": [
                          drink.short() for drink in drinks]})


'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++ GET /drinks-detail   +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

# Add permissions once route works


@app.route('/drinks-detail', methods=["GET"])
@check_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
    except BaseException:
        abort(401)
    finally:
        return json.dumps({"success": True, "drinks": [
                          drink.long() for drink in drinks]})


'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++ Post /drinks   +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
    except BaseException:
        abort(401)
    finally:
        return jsonify({"success": True, "drinks": new_drink.long()})


'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++ PATCH /drinks/<int:drink_id>   +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
    except BaseException:
        abort(401)
    finally:
        drink = [Drink.query.filter(Drink.id == drink_id).one_or_none()]
        return json.dumps({"success": True, "drinks": [
                          drink.short() for drink in drink]})


'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++ DELETE /drinks/<int:drink_id>   +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@check_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        Drink.query.get(drink_id).delete()
        db.session.commit()
    except BaseException:
        abort(401)
    finally:
        return jsonify({"success": True, "delete": drink_id})


'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++  ERROR HANDLING  +++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found."
    }), 404


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized."
    }), 401
