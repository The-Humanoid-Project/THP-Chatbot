cd frontend/
npm run dev
cd ..
./run_chatbot_endpoint.sh &
PID_RASA=$!
sleep 10
./run_ocr_endpoint.sh
kill $PID_RASA