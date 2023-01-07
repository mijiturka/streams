#/bin/bash
firefox -p twitch-mayonesia https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=$(cat client_id)&redirect_uri=http://localhost&scope=chat%3Aread+chat%3Aedit
