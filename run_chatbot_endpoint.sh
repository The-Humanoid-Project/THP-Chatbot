echo "initializing bot"
source py_venv_chatbot/bin/activate
rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml & rasa run actions
echo "closing bot"