#!/bin/bash

function colorize_text() {
    local text="$1"
    local color="$2"
    echo -e "\e[1;${color}m${text}\e[0m"
}

function colorize_progress_bar() {
    local progress="$1"
    local color="$2"
    local bar_length=50
    local filled_length=$((progress * bar_length / 100))
    local empty_length=$((bar_length - filled_length))
    
    local filled_bar="$(printf '%0.s█' $(seq 1 "$filled_length"))"
    local empty_bar="$(printf ' ' $(seq 1 "$empty_length"))"
    
    echo -e "\e[1;${color}m[${filled_bar}${empty_bar}]\e[0m"
}

sleep 1

# Starting RASA
screen -dmS THP_RASA
screen -S THP_RASA -X stuff "./run_chatbot_endpoint.sh\n"
colorize_text ".:Starting |RASA| EndPoint:." "31"
sleep 1
echo -n "Progress: "
for i in {1..100}; do
    colorize_progress_bar "$i" "31"
    sleep 0.1
    echo -ne "\e[1A\e[K"  # Move cursor up and clear the line
done
echo " Done!"
colorize_text ".:|RASA| is up and running!:. " "31"

sleep 1

# Starting OCR-OPAC
screen -dmS THP_OCR
screen -S THP_OCR -X stuff "./run_ocr_endpoint.sh\n"
colorize_text ".:Starting |OCR-OPAC| EndPoint:." "32"
sleep 1
echo -n "Progress: "
for i in {1..50}; do
    colorize_progress_bar "$i" "32"
    sleep 0.1
    echo -ne "\e[1A\e[K"
done
echo " Done!"
colorize_text ".:|OCR-OPAC| is up and running!:. " "32"

sleep 1

# Starting THP-ChatBot WebApp
screen -dmS THP_WebApp
screen -S THP_WebApp -X stuff "./run_app_frontend.sh\n"
colorize_text ".:Starting |THP-ChatBot| WebApp:." "36"
sleep 1
echo -n "Progress: "
for i in {1..25}; do
    colorize_progress_bar "$i" "36"
    sleep 0.1
    echo -ne "\e[1A\e[K"
done
echo " Done!"
colorize_text ".:|THP-ChatBot| WebApp is up and running!:. " "36"

sleep 1
