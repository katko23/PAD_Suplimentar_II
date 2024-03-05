# PAD_Suplimentar_II

## Instruction
### Please be sure to make a user (use POST) , before GET the information or to update something using PUT.
### Also we can have some errors in case of an unknown id, or an wrong one.
### All the errors is presented in an HTML format.
### All the nodes is working for 100%, if you get one error it might be in case of a wrong id, or an non-existent one.
### For the POST method of the sql_mongo the id can exist already in db because at each run of the program, the algorithm for creating new IDs starts from 1. In this case, either repeat the attempt to register the user, or try to delete the user from the database. This bug is due to the id generator, which was designed at the end as an emergency one, for registering the 2phase commit, also this endpoint can be edited in case it is necessary to register a specific user, with a specific id in both databases.  
### For the nosql db , I planned the creation of this id from the beginning, so for a post in mongo it is necessary to access the endpoint with the indication of the id like /nosql/users/{id} where {id} can take an arbitrary value.

## information  
This Flask application is a web service that handles user information using both PostgreSQL and MongoDB databases. The application has several endpoints for retrieving, creating, and updating user data. Additionally, it implements a 2 Phase Commit mechanism for POST requests, ensuring that data modifications are consistent across both databases.

Here's a breakdown of the key components and features of the code:

### Flask Setup:

The Flask application is created using the Flask class.  
PostgreSQL is configured using SQLAlchemy (flask_sqlalchemy extension).  
MongoDB is configured using PyMongo (flask_pymongo extension).  
Redis is used for caching.  

### PostgreSQL Database:

The Users class is defined as a model for the PostgreSQL database. It represents a table with columns id_user, firstname, and lastname.  
### MongoDB Database:  
MongoDB is configured with a replica set (mongodb://mongo1:27017,mongo2:27018,mongo3:27019,mongo4:27020/pad?replicaSet=rs0).  
### Endpoints:  

/sql/users/<id>: GET and PUT methods to interact with user data in the PostgreSQL database.  
/sql/users:Post method to add some new users ( be sure to write the data in json body )
/nosql/users/<id>: GET, POST, and PUT methods to interact with user data in the MongoDB database.  ( be sure to write the data in json body for post and put)
/sql/users: POST method to create a user in the PostgreSQL database.  

### ID Generation:  

An IDGenerator class is defined to generate unique integer IDs for new users. Sort of itterator pattern. It's a class who take a value and increment it.

### 2 Phase Commit for POST Requests:  

A new endpoint /sql_mongo/users is created to handle POST requests with a 2 Phase Commit mechanism.  
The IDGenerator is used to generate a unique integer ID for the new user.  
The code implements a 2 Phase Commit with nested transactions (db.session.begin_nested()) for ensuring data consistency between PostgreSQL and MongoDB.    
In case of an error during the transaction, the system rolls back to maintain data integrity.  

### Error Handling:  

Errors during the transaction phases are caught, and appropriate error messages are returned in the response.  
HTTP status code 500 is used for internal server errors.  

### Caching:  

Redis is used for caching user data to reduce the load on the databases.  


## Docker
[dockerhub](https://hub.docker.com/repository/docker/katko/pad_suplimentary_2/general)

## Postman
[postman](https://www.postman.com/katko23/workspace/utm/collection/24315989-d6cd493a-c90b-40e1-922b-0974b9accf56?action=share&creator=24315989)
