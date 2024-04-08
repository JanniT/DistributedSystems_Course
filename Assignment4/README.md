# Assignment 4

The task in this assignment was to create a multi-user chat system that uses socket technology. The system consists of a sesrver and several clients.

## How to run the assignment 4
Locate yourself in the /Assignment2 folder & open two terminals and run:
- ```$ python server.py``` on the other and
- ```$ python client.py``` on the other terminal

## Basic features
Client: 
- Set nickname
- Connect to the server by IP address
- Send text messages to other connected clients
- Chat supports several channels & private messages
- Shows messages from other clients
- Client is able to disconnect from the server

Server: 
- Handles several clients connections
- Transmits messages between clients