# deploy at replit -> downloader comment cookies stuff in constructor
# token is in env variable
# dont forget keep alive



import discord
import os
import random
from gag9_downloader import Downloader

token = TOKEN_VAR
# intents = discord.Intents.all()
# client = discord.Client(intents=intents)
client = discord.Client()

global downloader
global downloading
global info_msg

#start
@client.event
async def on_ready():
    global downloader
    global downloading
    print("Working {}".format(client.user))
    downloading = False
    downloader = Downloader()

#citanie spravy
@client.event
async def on_message(message):
    global downloader
    global downloading

    #ignorovanie vlastnej spravy
    if message.author == client.user:
        return

    # $help
    if message.content.startswith("!help"):
        await message.channel.send("Commands:\n"
                                   "!get [n] - n is number of images \n"
                                   "!reset   - bot resets itself to top of a 9gag")
        return


    elif message.content.startswith("!get"):
        line = str(message.content)
        line = line.strip().split()
        if len(line) != 2  :
            await message.channel.send("Bad format !get")
            return

        if not line[1].isnumeric() :
            await message.channel.send("Bad format !get")
            return

        num_of_messages = int(line[1])
        channel = message.channel

        if num_of_messages <=0 :
            await message.channel.send("Bad format!get")
            return

        if downloading:
            await message.channel.send("Currently downloading")
            return

        downloading = True
        info_msg = await message.channel.send("Loaded 0 / " + str(num_of_messages))
        await downloader.upload_pictures(channel,num_of_messages,info_msg)
        await info_msg.delete()
        downloading = False



        return

    if message.content.startswith("!reset"):
        del downloader
        downloader = Downloader()
        await message.channel.send("Reset")
        pass
        return
    if message.content.startswith("!"):
        await message.channel.send("Dont know this command")

client.run(token)


