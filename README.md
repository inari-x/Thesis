# @inari/thesis/dbot

This Discord bot is desinged to assist users with various language processing tasks. Developed
as part of a thesis project, the bot leverages the Discord.py library and Meta's powerful
language model LLaMA2 to provide translation, completion and summarization services. 

## Requirements & Dependencies

* Python (Discord.py, python-dotenv, openai)
* Windows with Ubuntu WSL (python3-virtualenv, python3-pip, curl, jq)
* CPU/GPU support (Follow according NVIDIA/AMD guides off-site, NVIDIA GPU reccommended)

## Installation Instructions

1. Clone the repository. For Windows users, set up a subsystem for Linux (WSL) 
    and clone the repository within.
2. Run `sudo apt-get install python3-virtualenv python3-pip curl jq`.
3. Navigate to the `./Thesis/dbot` folder, set up a virtual environment, and execute 
    `virtualenv bot`.
4. Activate the virtual environment by executing `source bot/bin/activate`.
5. Run `pip install discord.py && pip install python-dotenv && pip install openai`.
6. Create a `.env` file to store your Discord bot token.

The language model runs locally in the WSL system (`\\wsl.localhost\Ubuntu` via Explorer is the root to WSL).

## Start the model

Naviagate the folder it is located in, execute `/foo/bin/activate` and run:

1. `virtualenv llama`
2. `source llama/bin/activate`
3. `pip install "llama-cpp-python[server]"`
4. `python3 -m llama_cpp.server --model ../wizardlm-13b-v1.2.Q5_K_M.gguf`

Replace with the location and name of your `.gguf` file.

## Start the Discord bot

From the root, run `python3 bot.py`.

## Bot Commands
### Translate
Format message as:

`<source_language> <target_language> <message>`

EX: `german english how are you?`

### Summarize
Format message as:

`<message>`

EX: `In the vast expanse of the cosmos, where galaxies twirl in an eternal dance, and stars flicker like distant candles in the cosmic night, there exists a tapestry of wonders waiting to be unraveled. Nebulas, like celestial brushstrokes, paint the canvas of space with hues of vibrant gases, creating a spectacle that defies the imagination. Amidst this celestial symphony, planets of all shapes and sizes orbit their radiant suns, each telling a unique story of formation and evolution. Moons, silent companions to these worlds, cast their gentle light upon the cosmic drama, revealing mysteries that captivate the minds of astronomers and dreamers alike.
Traveling through the interstellar highways, comets and asteroids journey through the darkness, remnants of the early solar system's chaotic ballet. Their trajectories, a testament to the intricate gravitational choreography that shaped our cosmic neighborhood over eons of time.`


### Complete
Format message as:

`<message>`

`I am currently working in `

## Known Bugs

japanese translation

## Feature Roadmap

