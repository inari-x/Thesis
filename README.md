# @inari/thesis/dbot

This Discord bot is desinged to assist users with various language processing tasks. Developed
as part of a thesis project, the bot leverages the discord.py library and Meta's powerful
Large Language Model Llama 2 to provide translation, completion and summarization services. 

### Requirements & Dependencies

* Python (discord.py, python-dotenv, openai)
* Windows with Ubuntu WSL (python3-virtualenv, python3-pip, curl, jq)
* CPU/GPU support (Follow according NVIDIA/AMD guides off-site, NVIDIA GPU reccommended)

### Installation Instructions

1. Clone the repository. For Windows users, set up a subsystem for Linux (WSL2+) 
    and clone the repository within.
2. Run `sudo apt-get install python3-virtualenv python3-pip curl jq`.
3. Navigate to the `./Thesis/dbot` folder, set up a virtual environment, and execute 
    `virtualenv bot`.
4. Activate the virtual environment by executing `source bot/bin/activate`.
5. Run `pip install discord.py && pip install python-dotenv && pip install openai`.
6. Create a `.env` file to store your Discord bot token.

The language model runs locally in the WSL system (`\\wsl.localhost\Ubuntu` via Explorer is the root to WSL).

### Start the model

Naviagate the folder it is located in, execute `/foo/bin/activate` and run:

1. `virtualenv llama`
2. `source llama/bin/activate`
3. `pip install "llama-cpp-python[server]"`
4. `python3 -m llama_cpp.server --model ../wizardlm-13b-v1.2.Q5_K_M.gguf`

Replace with the location and name of your `.gguf` file.

### Start the Discord bot

From the root, run `python3 bot.py`.

### Bot Commands
## Translate
Format message as:

`<source_language> <target_language> <message>`

EX: `german english how are you?`

## Summarize
Format message as:

`<message>`

EX: `In the vast expanse of the cosmos, where galaxies twirl in an eternal dance, and stars flicker like distant candles in the cosmic night, there exists a tapestry of wonders waiting to be unraveled. Nebulas, like celestial brushstrokes, paint the canvas of space with hues of vibrant gases, creating a spectacle that defies the imagination. Amidst this celestial symphony, planets of all shapes and sizes orbit their radiant suns, each telling a unique story of formation and evolution. Moons, silent companions to these worlds, cast their gentle light upon the cosmic drama, revealing mysteries that captivate the minds of astronomers and dreamers alike.
Traveling through the interstellar highways, comets and asteroids journey through the darkness, remnants of the early solar system's chaotic ballet. Their trajectories, a testament to the intricate gravitational choreography that shaped our cosmic neighborhood over eons of time.`


## Complete
Format message as:

`<message>`

`I am currently working in `

### Button accesiblity
## !button
There are three main button functions implemented. To access those funcitons use !buttons in the 
channel where the bot is implemented. The bot is going to answer with displaying three option 
buttons (Tranlsation, Summarization and Completions). Chose which function you want to use. 

## !reset
The reset function is going to reset the saved context for the user. Resetting the context 
provides a clean state for the user. 

## /botconfig
botconfig represents a category of commands dedicated to configuring the chatbot's settings. 
Users can customize the max_tokens (the maximum number of tokens the chatbot will use to generate 
a response. The longer the given text, the longer the waiting time for a response), complete_max_tokens (the maximum number of tokens the completion endpoint will return), and system_prompt (system prompt serves as the introduction or context-setting for the chatbot). These configuration settings empower users to personalize their experience, adding a layer of flexibility to the chatbot's functionality.

### Known Bugs

japanese translation does not function very well. 

### References
## Academic Papers
- Luo, Z., Xu, C., Zhao, P., Sun, Q.: WizardCoder: Empowering Code Large Language Models with Evol-Instruct, https://arxiv.org/pdf/2306.08568.pdf, (2023). https://doi.org/10.48550/arXiv.2306.08568. [25] (in thesis bibliography)
- Touvron, H., Martin, L., Stone, K., & Albert, P. (2023). "Llama 2: Open Foundation and Fine-Tuned Chat Models." [30] (in thesis bibliography)
- Ye, Q., Axmed, M., Pryzant, R., Khani, F.: Prompt Engineering a Prompt Engineer, https://arxiv.org/pdf/2311.05661.pdf, (2023).


## Libraries Used
- `discord.py`: [Documentation](https://discordpy.readthedocs.io/)
- `python-dotenv`: [GitHub Repository](https://github.com/theskumar/python-dotenv)
- `openai`: [OpenAI API Documentation](https://beta.openai.com/docs/)
- `llama-cpp-python`: [GitHub Repository](https://github.com/openai/llama-cpp-python)
- `Hugging Face Transformers`: [Hugging Face Transformers Documentation](https://huggingface.co/transformers/)
- `pytest`: [Documentation](https://docs.python.org/3/library/unittest.html)

--> more in requirements.txt

## Guides
- NVIDIA GPU Installation Guide: [NVIDIA Guide](https://developer.nvidia.com/cuda-downloads)
- AMD GPU Installation Guide: [AMD Guide](https://www.amd.com/en/support)
- WSL Installation: [Microsoft WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/install)
- Janek. "How to run a llama, alpaca, vicuna REST API for AI Discord bot",  https://www.youtube.com/@panjanek667, (2023).
- Janek. "Llama.cpp + CUDA",  https://www.youtube.com/@panjanek667, (2023)



