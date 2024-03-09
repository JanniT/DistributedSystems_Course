# Assignment 2

The task in this assignment was to create a distributed system using Remote Procedure Calls (RPC). The app is ran and used in the terminal.
There's the client- and server sides which communicate with each other through the RPC's. 

## How to run the assignment 2
Locate yourself in the /Assignment2 folder & open two terminals and run:
- ```$ python server.py``` on the other and
- ```$ python client.py```

## Basic features
Client:
- Ask the user for input & send it to server
- There's topic, text, and timestamp for the note
- If the topic already exists on the XML, the data will be appended to the same structure
- If not, a new XML entry will be made (= new topic is created outside other topic structures)
- Get the contents of the XML database based on given topic

Server: 
- Process the client's input
- Save data on a local database mock (XML)
- Handle multiple client requests at once

## Additional features
Client: 
- Name search terms to lookup data on wikipedia
- Append the data to an existing topic

Server: 
- Query wikipedia for user submitted articles
- Add relevant information to user submitted topic
- The server should give a link to a wikipedia article found
