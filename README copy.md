<<<<<<< HEAD
# 2PhaseCommit
2 Phase Commit using Python 3
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

1. Run command: python server.py
2. Now the server is up
3. vim ClientSetUp.py, change proxy_id to ip of server you just set up  
    ```
      proxy_id = <server_ip>
    ```
4. Run ServerDbSetup.sh in current work directory
  ```
    chmod a+x ServerDbSetup.sh
    ./ServerDbSetup.sh
  ```
5. vim fabfile.py, set env.host to server ip and all client ip
    ```
      env.hosts = [<server_ip>, <client1_ip>, ..., <clientN_ip>] 
    ```
6. vim fabfile.py, define server/client roles
   ```
       env.roledefs.update({
       'server': [<server_ip>],
       'client': [<client1_ip>, ..., <clientN_ip>]
       }) 
    ```
7. Run command `fab setup` to put the python files to clients and create tables in sqlite.
8. Now everything is up and running! Start your exploration!

## Code Structure

###### The project use built-in library xmlrpclib as an interface for server-client communication. Each machine, both server and multiple clients, has an independent database where key value and process status are logged. SQLite is introduced as the its advantage of being light-weight and easy installation. For better streamlining, fabric command-line tool is also injected in the project, simplifying the execution of python files in distributed machines.

1. Server.py
   - log: keep track of operation conducted on info table
   - get: fetch key value
   - put: update key value
   - delete: delete key 
   - main: create server and set up port for incoming events, register above functions
   
2. client.py
   - log: keep track of status on info table
   - get: fetch key value from distant server, if no value is received, delete(update) key in info table
   - put: update key value in both server info and client info table
   - delete: delete key in both server info and client info table

3. ClientSetUp.py
   - fetch local ip address and store it in `client_add`, which is imported later by client.py
   - build connection to server 
   - connect to local db `ex` and receive the cursor

4. DbSetUp.sh
   - create log and info table if not exist

5. fabfile.py
   - configure server/client address and appoint roles
   - identify login key and ssh_configure file
   - setup: distribute file mention above to separate client machines
   - getKey: run get function of client.py
   - putKey: run put function of client.py
   
## Error Handling
   - Log Table:
     There are four states: 1 for getkey request received; 2 for getkey request completed; 3 for put/del request received; 4         for put/del requeset completed. Every successful operation should have two records in log table: either a pair of (1, 2) or      (3, 4). For instance, if a [put] request is sent, server is designed to check log table in order to detect any uncompleted      processes. A missing record of state 4 indicates unsuccessful/uncompleted communication, consequently puts the system           on hold.

   - check data validation before inserting/deleting. Keep in mind return value could be None.
   - Make the best use of try-catch block. Wrap the code that fires up remote procedure call around try-catch blocks. This is useful to traceroute issues.


## License

Produced by Yongjun


>>>>>>> Create README.md
