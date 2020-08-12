import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from flask import jsonify

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))


# Database Path
# sqlite:////Users/tylerproctor/Desktop/Files to Back
# up/CodeEd/Udacity_Projects/Section_1/Project1/Udacity_Fyurr_App_Project/projects/Coffee_Shop_Site_Repo/Udacity_Coffee-Shop-Site/starter_code/backend/src/database/database.db

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def cprint(string1, string2):
    print("=========================")
    print("")
    print(string1)
    print("")
    print(string2)
    print("")
    print("=========================")


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    print("Dropping database and recreating")
    db.drop_all()
    db.create_all()


'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''


class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string,
    # 'parts':number}]
    recipe = Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''

    def short(self):
        recipe_formatted = str(self.recipe).replace("'", "\"")
        short_recipe = [{'color': r['color'], 'parts': r['parts']}
                        for r in json.loads(recipe_formatted)]
        response_object = {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(recipe_formatted)
        }
        return response_object

    '''
    long()
        long form representation of the Drink model
    '''

    def long(self):
        recipe_formatted = str(self.recipe).replace("'", "\"")
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(recipe_formatted)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
        # return json.dumps({"id": self.id, "title": self.title, "recipe":
        # self.recipe}.short())


# Example repr


# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(1000), nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     address = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.String(120), nullable=False)
#     image_link = db.Column(db.String(1000), nullable=True)
#     facebook_link = db.Column(db.String(500), nullable=True)
#     website = db.Column(db.String(500), nullable=True)
#     seeking_talent = db.Column(db.Boolean(), default=True, nullable=True)
#     shows = db.relationship('Show', backref='Venue', lazy=True)

#     def __repr__(self):
# return '"id": {self.id}, "name": {self.name}, "city": {self.city},
# "state": {self.state}, "address": {self.address}, "phone": {self.phone},
# "image_link": {self.image_link}, "facebook_link":
# {self.facebook_link}'.format(self=self);
