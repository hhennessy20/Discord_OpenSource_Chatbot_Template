import discord_opensource_chatbot

#Enter the name(s) you'd like to use to call your bot with
names = ["NAME", "NAME_2", "NAME_N"]

#Enter the name you gave your model
model_name = "llama3.1"

#Enter your Discord bot's key here after setting it up here: https://discord.com/developers/applications
discord_key = 'DISCORD_KEY'

#Set this to protect others from deleting your bot's memory. To reset your bot's memory, enter "/[model name]purge[purge_code if specified]". Default is no code.
purge_code = ""

discord_opensource_chatbot.run_bot(names, model_name, discord_key, purge_code)
