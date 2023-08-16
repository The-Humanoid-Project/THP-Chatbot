echo "initializing bot"
rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml & rasa run actions
echo "closing bot"