
=======
# Two-phases-commit

The second project in Distributed Computing: Two phases commit.

The first project is implemented in function in global scope, so I have to register all put, get, del functions for xmlrpc interface.
Later after referring to some other students' work, I realized that a better way to build the system is through Class. For better organization,
I implemented the system in Object-oriented programming.

Another improvement is how the record is logged. In first project, the activities of both coordinator and replica are logged in SQLite tables.
This will create unnecessary overhead of database connection and insert/update request. In addition, database has the potentiality to crash,
which is bound to jeopardize the availability of logging information. Thereofore, in the second project, I use text file to keep track of coordinator/replica status.

## Installation
##### Have to make sure the following tools available in both server and client machines.

1. sqlite3
2. python
3. fabric

##### Have Fabric ready to streamline client processes.
In this project, fabfile will be run on server machine for simplicity.


## Environment Setup

1. Run command: python participant.py [port_num] [id]
2. Now the participant is up
3. Run command: python Leader.py

## NOTE
I used 5001 and 5002 ports for 2 participants. So Leader has 2 of them with below code line.

participant_add = ["http://localhost:5001", "http://localhost:5002"]

## Code Structure

###### The project use built-in library xmlrpclib as an interface for server-client communication.
Each machine, both server and multiple clients, has an independent database where key value and process status are logged.
SQLite is introduced as the its advantage of being light-weight and easy installation.

1. Leader.py
   - log: keep track of operation conducted on info table
   - get: fetch key value
   - put: update key value
   - delete: delete key
   - main: create server and set up port for incoming events, register above functions

2. Participant.py
   - log: keep track of status on info table
   - get: fetch key value from distant server, if no value is received, delete(update) key in info table
   - put: update key value in both server info and client info table
   - delete: delete key in both server info and client info table
