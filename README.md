# @inari/thesis/dbot
## Sep 13, 2023 - v0.0.2

## Install

clone the repository
Windows: setup a subsystem for linux like WSL and clone the repository in there. 

run sudo apt-get install python3-virtualenv python3-pip curl jq
naviagate in dbot folder and setup virtual environment
(virtualenv bot)
activate the virtual environment (source bot/bin/activate)

run: pip install discord.py && pip install python-dotenv && pip install openai

Create a .env file for storing your Token (discord bot token)

# Running Bot
python3 bot.py

The model itself runs locally in wsl system. (`\\wsl.localhost\Ubuntu` via explorer is root to WSL)
to start: naviagate the folder it is located in, start your virtual environment. I called it llama (source llama/bin/activate)

and then run:  python3 -m llama_cpp.server --model ../wizardlm-13b-v1.2.Q5_K_M.gguf 
(If you are using the same model as me)

## Bot Commands
### Translate
Format message as:

`<source_language> <target_language> <message>`

EX: german english how are you?