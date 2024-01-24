echo "Starting Frontend..."
npm run dev
sleep 5

if [ $? -eq 0 ]; then
    echo "Starting Rasa Backend..."
    ./run_chatbot_endpoint.sh
    if [ $? -eq 0 ]; then
        echo "Starting OCR Endpoint..."
        ./run_ocr_endpoint.sh
    else
        echo "Error: Rasa Backend failed to start."
    fi
else
    echo "Error: Frontend failed to start."
fi
