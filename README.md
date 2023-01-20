# The Humanoid Project Chatbot

## Installation Process

Install conda to set a particular python version for the code base following this [site](https://docs.anaconda.com/anaconda/install/linux/)

After installation, create a virtual environment with python version == 3.9 using the command `conda create -n $PYTHON_ENV_NAME python=3.9`

Activate this environment and switch to the directory to create a python3 environment using the command `python3 -m venv ./venv`

To activate the virtual environment, `source ./venv/bin/activate`

Thereafter, install all python packages using the command `pip3 install -r requirements.txt`

## Debugging Conflicts

- **PyAudio installation error involving wheel build and portaudio.h** \\
This might happen because of a few uninstalled dependencies in your Linux. Run the following to install all PyAudio dependencies `$ sudo apt install portaudio19-dev python3-pyaudio`

