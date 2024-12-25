# Author: hhennessy20 and Shnabbydoodle
# 2/14/2024
# Copyright MMXXIV :)
# please dont steal!!!
# no copyright infringement intended!!!

import discord
from openai import OpenAI
import asyncio
import random
import requests
import json
import os

#Saves memory to json
def save_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

#Opens json with memory if it exists
def load_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

#Returns a channel with the specified server and channel name if exists
async def get_channel(discord_client, server_name, channel_name):
    for guild in discord_client.guilds:
        if guild.name == server_name:
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel) and channel.name == channel_name:
                    return channel
    return None

#Returns true if any name is in message
def name_in_message(names, message):
    name_in_message = False
    for name in names:
        if name.upper() in message.upper():
            name_in_message = True
    return name_in_message

def too_many_bots(message_is_bot):
    counter = 0
    for message in message_is_bot[-4:]:
        if message[0] and not message[1]:
            counter += 1
    # Debug line to print the counter
    # print(counter)
    if counter > 2:
        return True
    return False

# Main command for running bot
def run_bot(names, model_name, discord_key, purge_code = ""):
    # Creates the array of messages the bot will receive and initialize its personality
    messages = load_from_json(model_name + ".json")
    message_is_bot = []
    #messages.append({"role": "system", "content": context_message})

    # Defines the intents your bot will use
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    # Creates a new Discord client with the specified intents
    discord_client = discord.Client(intents=intents)

    # Event that runs when the bot is ready
    @discord_client.event
    async def on_ready():
        print('Logged in as')
        print(discord_client.user.name)
        print(discord_client.user.id)
        print('------')

        # Fetch all members to ensure the member cache is populated
        for guild in discord_client.guilds:
            async for member in guild.fetch_members():
                pass

            
    # Event that runs whenever a message is sent in a channel the bot can see
    @discord_client.event
    async def on_message(message):

        #Reset memory command
        if ("/" + model_name + "purge") in message.content:
            if message.content == "/" + model_name + "purge" + purge_code:
                messages.clear()
                save_to_json(model_name + ".json", messages)
                async with message.channel.typing():
                    await asyncio.sleep(random.randint(0,500)/100)
                    await message.channel.send(discord_client.user.name + " reset.")
            else:
                async with message.channel.typing():
                    await asyncio.sleep(random.randint(0,500)/100)
                    await message.channel.send("Enter proper purge code to reset " + discord_client.user.name + ".")

        # Checks if the message contains name
        elif (name_in_message(names, message.content) and message.author != discord_client.user):

            # Debug line to print all messages received by the bot
            # print(message.content)

            # Checks if message is bot
            if message.author.bot and message.author == discord_client.user:
                message_is_bot.append([True, True])
            elif message.author.bot:
                message_is_bot.append([True, False])
            else:
                message_is_bot.append([False, False])

            if message.author.bot and too_many_bots(message_is_bot):
                return
            
            # Gets name or nickname of user to append to bot message
            username = message.author.name
            if (message.channel.type is not (discord.ChannelType.private or discord.ChannelType.group)) and message.author.nick is not None:
                username = message.author.nick

            # Simulates a few seconds of bot reading your message
            await asyncio.sleep(random.randint(0,500)/100)

            # Bot will appear to be typing while it generates your message
            async with message.channel.typing():
                # Sends your message to ollama and gets response
                messages.append({"role": "user", "content": username + " says: " + message.content})
                payload = {"model": model_name,"stream": False,"messages": messages}
                response_json = requests.post('http://localhost:11434/api/chat', json=payload)
                response = response_json.json()['message']['content']

                # Adds response to bot context so it remembers
                messages.append({"role": "assistant", "content": response})

                #Update memory file
                save_to_json(model_name + ".json", messages)
                
                # Simulates the bot typing your message, slightly longer depending on the length of the message
                await asyncio.sleep(.01 * len(response))
                await message.channel.send(response)

    # Runs the bot with your Discord token
    discord_client.run(discord_key)
