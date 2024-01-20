# The Humanoid Project Chatbot

## Installation Process

Install conda to set a particular python version for the code base following this [site](https://docs.anaconda.com/anaconda/install/linux/)

After installation, create a virtual environment with python version == 3.9.13 using the command: \
`conda create -n $CONDA_ENV_NAME python=3.9.13`

Activate this environment and switch to the directory to create a python3 environment using the command: \
`python3 -m venv ./venv`

Therefore, we are creating two virtual environments:
- Conda environment - to set the desired python version (this can be skipped if you can downgrade/upgrade to the required version)
- Python3 virtual environment - to create an environment for all the packages installed via pip package manager

**To activate the virtual environment**: `source ./venv/bin/activate`

Thereafter, install all python packages using the command `pip3 install -r requirements.txt`

**Train the Rasa Model** : `rasa train` \
**Fire-up the Action server** : `rasa run actions` \
**Test the chatbot model via terminal** : `rasa shell & rasa run actions`

## Debugging Conflicts

- **PyAudio installation error involving wheel build and portaudio.h** \
This might happen because of a few uninstalled dependencies on your Linux. Run the following to install all PyAudio dependencies: `$ sudo apt install portaudio19-dev python3-pyaudio`

## How to setup this branch ###########

`npm install` to install all the node modules in the frontend directory \
`pip install requirements.txt` to install all Rasa and yolo dependencies \
`pip install ocr_reqs.txt` to install all OCR and flask dependencies \

`npm run dev` in frontend directory to start the React app \
`./humanoid.sh` in root directory to start the Rasa server \
`python3 ocr_flask.py` to start the flask server for OCR endpoint \


