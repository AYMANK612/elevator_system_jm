# elevator_system_jm

## Overview

The Elevator Control System is designed to manage and control elevators in a building through a set of RESTful APIs. 
It allows you to request elevators, check their directions, and determine the next destination floor.

## Installation

To set up and run this project , follow these steps:

1. git Clone this GitHub repository.
2. Install Poetry (if not already installed): pip install poetry
3. Install project dependencies using Poetry:poetry install
4. Activate the virtual environment: poetry shell
5. Run database migrations to create the necessary tables: python manage.py makemigrations
6. migrate: python manage.py migrate
7. Run project: python manage.py runserver
8. Access the API at http://127.0.0.1:8000/elevator/

I have used poetry as as dependency manager, you can also install the dependencies manually.
pip install django
pip install djangorestframework
pip install psycopg2



#Database 
In this project i haved used a PostgreSQL database to store elevator information and requests.
(can also use the default SQLlite for testing by commenting the postgres 
info in settings file  and uncommenting the default SQLlite INFO ) 
The main models used are:
Elevator: Stores information about each elevator, including its current floor, working status, and direction.
E_Request: Represents elevator requests, including the floor number and timestamps.



#Postman Collection
For convenience, i have include a Postman collection with pre-defined requests to interact with the APIs. 
You can directly import the collection into Postman and use it to test the endpoints.

APIs included:

1.Initialize Elevators:
  URL: http://127.0.0.1:8000/initialize/
  Method: POST
  Description: Initializes the specified number of elevators.
  Example Payload:{
      "number_of_elevators": 3
  }

2.Request an Elevator at Any Floor:
  URL: http://127.0.0.1:8000/request/
  Method: POST
  Description: Request an elevator to a specified floor and also saves the request to the database.
  Example Payload:{
    "from_floor": 5
}
3.Fetch All Requests for a Given Elevator:
  URL: http://127.0.0.1:8000/getall_requests/
  Method: GET
  Description: Retrieve all requests for a specific elevator or all requests if no elevator ID is provided.
  
4.Fetch Requests for a Specific Elevator:
  URL: http://127.0.0.1:8000/getall_requests/<int:elevator_id>/
  Method: GET
  Description: Retrieve requests for a specific elevator by providing the elevator's ID in the URL.
  
5.Toggle Elevator Maintenance Status:
  URL: http://127.0.0.1:8000/maintanaince_toggle/
  Method: PUT
  Description: Mark an elevator as "not working" or "working" for maintenance purposes.
  Example Payload:{
    "elevator_id": 2
}

6.Toggle Elevator Door:
  URL: http://127.0.0.1:8000/door_toggle/
  Method: PUT
  Description: Open or close the door of a specific elevator.
  Example Payload:{
    "elevator_id": 1
}

7.Get Elevator Direction:
  URL: http://127.0.0.1:8000/direction/
  Method: GET
  Description: Retrieve the direction (up or down) in which an elevator is currently moving.
  Example URL: 'http://127.0.0.1:8000/direction/?elevator_id=3'

8.Get Next Elevator Destination:
  URL: http://127.0.0.1:8000/destination/
  Method: GET
  Description: Retrieve the next destination floor for a specific elevator.
  Example URL: http://127.0.0.1:8000/destination/?elevator_id=2

