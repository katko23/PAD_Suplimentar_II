import uuid

from flask_socketio import SocketIO
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from redis import Redis
import pickle

app = Flask(__name__)
# Configure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://killercoseru:SCFt4ja2ougp@ep-holy-surf-a2elkdep.eu-central-1.aws.neon.tech/pad'
db = SQLAlchemy(app)
socketio = SocketIO(app)
# Configure Redis
redis = Redis(host='cache', port=6379, db=0)

# Define Users model for PostgreSQL
class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))

@app.route('/sql/users/<id>', methods=['GET', 'POST', 'PUT'])
def sql_user(id):
    if request.method == 'GET':
        # Try to get user from cache
        user = pickle.loads(redis.get(id)) if redis.get(id) else None
        if user is None:
            # If not in cache, get user from database
            user = Users.query.get(id)
            # Store user in cache
            redis.set(id, pickle.dumps(user))
        return {'firstname': user.firstname, 'lastname': user.lastname}
    elif request.method == 'POST':
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        new_user = Users(id=id, firstname=firstname, lastname=lastname)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Users created successfully'}
    elif request.method == 'PUT':
        user = Users.query.get(id)
        user.firstname = request.json['firstname']
        user.lastname = request.json['lastname']
        db.session.commit()
        # Update user in cache
        redis.set(id, pickle.dumps(user))
        return {'message': 'Users updated successfully'}


import random

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://mongo1:27017,mongo2:27018,mongo3:27019,mongo4:27020/pad?replicaSet=rs0"
mongo = PyMongo(app)

@app.route('/nosql/users/<id>', methods=['GET', 'POST', 'PUT'])
def nosql_user(id):
    if request.method == 'GET':
        # Try to get user from cache
        user = pickle.loads(redis.get(id)) if redis.get(id) else None
        if user is None:
            # If not in cache, get user from database
            user = mongo.db.users.find_one({'_id': id})
            # Store user in cache
            redis.set(id, pickle.dumps(user))
        return {'firstname': user['firstname'], 'lastname': user['lastname']}
    elif request.method == 'POST':
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        mongo.db.users.insert_one({'_id': id, 'firstname': firstname, 'lastname': lastname})
        return {'message': 'Users created successfully', 'id': id}
    elif request.method == 'PUT':
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        mongo.db.users.update_one({'_id': id}, {'$set': {'firstname': firstname, 'lastname': lastname}})
        # Update user in cache
        user = mongo.db.users.find_one({'_id': id})
        redis.set(id, pickle.dumps(user))
        return {'message': 'Users updated successfully'}


@app.route('/sql/users', methods=['POST'])
def sql_user_p():
    if request.method == 'POST':
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        new_user = Users( firstname=firstname, lastname=lastname)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Users created successfully'}


# Define a shared variable for 2 Phase Commit
two_phase_commit_data = {}

class IDGenerator:
    def __init__(self):
        self.counter = 1  # Start with an initial value

    def generate_id(self):
        new_id = self.counter
        self.counter += 1
        return new_id

id_generator = IDGenerator()

@app.route('/sql_mongo/users', methods=['POST'])
def sql_mongo_user():
    if request.method == 'POST':
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        new_user_id = id_generator.generate_id()
        # Phase 1: Prepare - Begin Transaction
        try:
            with db.session.begin_nested():
                # Create user in PostgreSQL
                new_user_postgresql = Users(id_user=new_user_id, firstname=firstname, lastname=lastname)
                db.session.add(new_user_postgresql)
            # Create user in MongoDB
            new_user_mongo = {'_id': new_user_id, 'firstname': firstname, 'lastname': lastname}
            mongo.db.users.insert_one(new_user_mongo)
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error during Phase 1 - Prepare', 'error': str(e), "id":new_user_id}, 500

        # Phase 2: Commit - Finalize Transaction
        try:
            db.session.commit()
            two_phase_commit_data.pop('new_user_id', None)  # Clear the data after successful commit
            return {'message': 'Users created successfully in both databases'}
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error during Phase 2 - Commit', 'error': str(e)}, 500

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
