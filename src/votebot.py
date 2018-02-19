import discord
import datetime
from votecore import VoteUnit

client = discord.Client()
VoteUnit.gCLIENT = client
vote = None


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    global vote
    if message.content.startswith("投票"):
        tmp = message.content.split(" ")
        if len(tmp) < 2:
            m = "usage: 投票 投票内容1,2,3...."
            await client.send_message(message.channel, m)
        else:
            vote = VoteUnit(message.channel, tmp[1])
            await vote.dispTitle()
            await vote.mainLoop()

    if message.content.startswith("終了"):
        print("keika")
        if vote is not None:
            vote.endVote()

# token にDiscordのデベロッパサイトで取得したトークンを入れてください
client.run("")
