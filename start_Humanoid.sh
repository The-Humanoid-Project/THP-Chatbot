screen -dmS THP_RASA
screen -S THP_RASA -X stuff "./run_chatbot_endpoint.sh\n"

screen -dmS THP_OCR
screen -S THP_OCR -X stuff "./run_ocr_endpoint.sh\n"

screen -dmS THP_WebApp
screen -S THP_WebApp -X stuff "./run_app_frontend.sh\n"