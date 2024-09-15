# Discord_OpenSource_Chatbot_Template
A simple ollama chatbot and template to create and run it, created as a personal project by hhennessy20 and shnabbydoodle.

You'll need to have Python and the discord library, as well as asyncio and requests. Use "pip install [package-name]" for these.

This can be done in a virtual environment using the venv command, documentation for which can be found here:
https://docs.python.org/3/library/venv.html

In addition, you'll need to download and set up an ollama model:
https://github.com/ollama/ollama/tree/main

To create a simple ollama model using llama3.1, you can enter the following command:
>ollama run llama3.1

This will download the llama3.1 model library, which takes up about 5 gigabytes.

Once you have downloaded llama3.1, you can create your own model with its own personality and name using a modelfile. To do so, create a .txt file with the following format:

>FROM [model library name]
>
>SYSTEM [context message. Basically, describe how you want your bot to act and any information it needs to function.]

Then, you'll need the following command to generate your model in ollama:
>ollama create choose-a-model-name -f <location of the file e.g. ./Modelfile>

Ollama will remember any models you make, and if you decide to change your model's context, simply calling the above command again will overwrite your model with the new modelfile.

You'll also need to set up a bot on Discord's Application page here:
https://discord.com/developers/applications

Once created, on the bot's page under Privileged Gateway Intents, you'll need to enable SERVER MEMBERS INTENT and MESSAGE CONTENT INTENT.

Then, under the OAuth2 tab, within OAuth2 URL Generator, select "bot", which will open a list of further permissions. Select "Read Messages/View Channels", "Send Messages", and "Read Message History".

With these options checked, copy the generated link and invite the bot to your server of choice.

Once the bot is added to a server, copy the Discord Key from the Developer Portal and the OpenAI key into the template file. Add the names you'd like your bot to be called with to the names array, the name of your model, and an optional password for its memory reset command.

Run the template file, and your bot should come online!
