# PAD_Suplimentar_II


## information  
This Flask application is a web service that handles user information using both PostgreSQL and MongoDB databases. The application has several endpoints for retrieving, creating, and updating user data. Additionally, it implements a 2 Phase Commit mechanism for POST requests, ensuring that data modifications are consistent across both databases.

Here's a breakdown of the key components and features of the code:

Flask Setup:

The Flask application is created using the Flask class.
PostgreSQL is configured using SQLAlchemy (flask_sqlalchemy extension).
MongoDB is configured using PyMongo (flask_pymongo extension).
Redis is used for caching.
PostgreSQL Database:

The Users class is defined as a model for the PostgreSQL database. It represents a table with columns id_user, firstname, and lastname.
MongoDB Database:

MongoDB is configured with a replica set (mongodb://mongo1:27017,mongo2:27018,mongo3:27019,mongo4:27020/pad?replicaSet=rs0).
Endpoints:

/sql/users/<id>: GET, POST, and PUT methods to interact with user data in the PostgreSQL database.
/nosql/users/<id>: GET, POST, and PUT methods to interact with user data in the MongoDB database.
/sql/users: POST method to create a user in the PostgreSQL database.
ID Generation:

An IDGenerator class is defined to generate unique integer IDs for new users.
2 Phase Commit for POST Requests:

A new endpoint /sql_mongo/users is created to handle POST requests with a 2 Phase Commit mechanism.
The IDGenerator is used to generate a unique integer ID for the new user.
The code implements a 2 Phase Commit with nested transactions (db.session.begin_nested()) for ensuring data consistency between PostgreSQL and MongoDB.
In case of an error during the transaction, the system rolls back to maintain data integrity.
Error Handling:

Errors during the transaction phases are caught, and appropriate error messages are returned in the response.
HTTP status code 500 is used for internal server errors.
Caching:

Redis is used for caching user data to reduce the load on the databases.
WebSocket Support:

SocketIO is configured, indicating potential support for WebSocket communication.

## Docker
[dockerhub](https://hub.docker.com/repository/docker/katko/pad_suplimentary_2/general)

## Postman
[postman](https://www.postman.com/katko23/workspace/utm/collection/24315989-d6cd493a-c90b-40e1-922b-0974b9accf56?action=share&creator=24315989)
