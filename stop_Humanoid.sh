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

# Stopping THP-ChatBot WebApp
screen -X -S THP_WebApp quit
colorize_text ".:Stopping |THP-ChatBot| WebApp:." "36"
sleep 1
echo -n "Progress: "
for i in {1..25}; do
    colorize_progress_bar "$i" "36"
    sleep 0.1
    echo -ne "\e[1A\e[K"  # Move cursor up and clear the line
done
echo " Done!"
colorize_text ".:|THP-ChatBot| WebApp is Terminated!:. " "36"

sleep 1

# Stopping OCR-OPAC
screen -X -S THP_OCR quit
colorize_text ".:Stopping |OCR-OPAC| EndPoint:." "32"
sleep 1
echo -n "Progress: "
for i in {1..50}; do
    colorize_progress_bar "$i" "32"
    sleep 0.1
    echo -ne "\e[1A\e[K"
done
echo " Done!"
colorize_text ".:|OCR-OPAC| is Terminated!:. " "32"

sleep 1

# Stopping RASA
screen -X -S THP_RASA quit
colorize_text ".:Stopping |RASA| EndPoint:." "31"
sleep 1
echo -n "Progress: "
for i in {1..100}; do
    colorize_progress_bar "$i" "31"
    sleep 0.1
    echo -ne "\e[1A\e[K"
done
echo " Done!"
colorize_text ".:|RASA| is Terminated!:. " "31"

sleep 1
