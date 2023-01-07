# Set-up
```
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

# Authentication
1. create a twitch app with redirect url at http://localhost
2. place client_id in a file at `./client_id`
3. start server twitch will redirect auth token to:
```
(venv)$ python3 auth_server.py
```
4. open the twitch authentication page with a firefox profile called `twitch-mayonesia`:
```
$ bash auth_request.sh
```
go through authentication flow in browser. the server will print the token to logs.
5. place token in a file at `./token`

# Connecting to chat
```
(venv)$ python3 bot.py
```
