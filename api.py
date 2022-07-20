from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# test if it works
@app.route("/")
def index():
    return "it works!"
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#          user CRUD             #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    columns = ['username', 'email']
    col_values = []
    for c in columns:
        if c in request.values:
            col_values.append(request.values[c])
        else:
            col_values.append(None)
    new_user = User(*col_values)
    
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'successfully create new user'},200


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    result_json = users_schema.jsonify(result)

    return result_json

# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)

    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    columns = ['username', 'email']
    for c in columns:
        if c in request.values:
            setattr(user, c, request.values[c])

    db.session.commit()
    return {'message': 'successfully update user'}, 200


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return {'message': 'successfully delete user'}, 200


if __name__ == '__main__':
    app.run(debug=True)