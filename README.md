# Connect-4
A Flask and MongoEngine based backend for the game Connect - 4

## Instructions for running the app:

### For sending requests to the deployed app:

The app is deployed at [obscure-spire-16178.herokuapp.com](obscure-spire-16178.herokuapp.com).<br><br>
**Postman settings:**
1. Header
Key - Content-Type
Value - application/json

2. Body
Write the data to be sent as 'raw'

**For starting the game**<br>
URL - [obscure-spire-16178.herokuapp.com/start](obscure-spire-16178.herokuapp.com/start)<br>
Request Type - GET <br>
Expected Input -  START<br>
* Note: Just the word 'START' is expected as raw data without any quotes or brackets

Expected Output - <br>
A JSON of the following structure:<br>
```
{
    "message" : "READY",
    "token" : <token>
}
```

**For playing the game**<br>
URL - [obscure-spire-16178.herokuapp.com/makemoves](obscure-spire-16178.herokuapp.com/makemoves)<br>
Request Type - GET
Expected Input -<br>
A JSON of the following structure:<br>
```
{
    "token" : <token>,
    "col" : <col>
}
```
* Note 1: token is the string returned by the start API. Copy the token and paste the value 
* Note 2: col is an integer ranging from 0-6 representing the move. Any other value would return a response "Invalid move" <br>

Expected Output - 
For each move, one of the following is returned:
1. If invalid move is made - "Invalid move!"
2. If yellow makes a move - "Yellow made a move"
3. If red makes a move - "Red made a move"
4. If yellow wins - "Yellow wins!"
5. If red wins - "Red wins!"

**For getting a list of moves made**<br>
URL - [obscure-spire-16178.herokuapp.com/getmoves](obscure-spire-16178.herokuapp.com/getmoves)<br>
Request Type - GET <br>
Expected Input -<br>
A JSON of the following structure:<br>
```
{
    "token" : <token>
}
```

Expected Output -<br>
A JSON of the following structure:<br>
```
[
    {
        "Col" : <col>,
        "Player" : <player>
    }
]
```
<br>
It returns a list of all the moves made by each player in the order of the moves made.

### For running the app locally:
```
pip3 install requirements.txt
flask run
```
#### The folder 'screenshots' contains the screenshots of testing the app on Postman

