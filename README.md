# @inari/thesis/dbot
## Nov 2, 2023 - v0.0.3

## Requirements & Dependencies

* Python (Discord.py, python-dotenv, openai)
* Windows with Ubuntu WSL (python3-virtualenv, python3-pip, curl, jq)
* CPU/GPU support (Follow according NVIDIA/AMD guides off-site)

## Installation Instructions

Clone the repository
Windows: setup a subsystem for linux like WSL and clone the repository in there. 

1) Run `sudo apt-get install python3-virtualenv python3-pip curl jq`
2) Naviagate in dbot folder and setup virtual environment and run `virtualenv bot`
3) Activate the virtual environment `source bot/bin/activate`

Run: `pip install discord.py && pip install python-dotenv && pip install openai`

Create a `.env` file for storing your Token (discord bot token)

The model itself runs locally in wsl system. (`\\wsl.localhost\Ubuntu` via explorer is root to WSL)

## Start the model server

Naviagate the folder it is located in, execute `/foo/bin/activate` and run:

`virtualenv llama`
`source llama/bin/activate`
`pip install "llama-cpp-python[server]"`
`python3 -m llama_cpp.server --model ../wizardlm-13b-v1.2.Q5_K_M.gguf`

Replace with the location and name of your `.gguf` file.

## Start the Discord bot

From the root, run `python3 bot.py`.



## Bot Commands
### Translate
Format message as:

`<source_language> <target_language> <message>`

EX: german english how are you?