import discord
import time
import asyncio

messages = joined = 0
bad_words = ["bad", "stop"]


# reading token from token.txt

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

# Bot login
client = discord.Client()


# read messages
@client.event
async def on_message(message):
    global messages
    messages += 1

    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)

    if message.content == "#help":
        embed = discord.Embed(title="Help on BOT", description="Commands")
        embed.add_field(name="#hello",value="Greets the user")
        embed.add_field(name="#users", value="Prints number of user")
        await message.channel.send(content=None, embed=embed)

    valid_users = ["Anup#0197"]
    id = client.get_guild(748870113041580043)
    channels = ["commands"]  # channel list
    identifyCommand = '#'
    print(message.content.lower())

    if message.content.startswith(identifyCommand):
        if str(message.channel) in channels and str(message.author) in valid_users:  # only read channels in the list
            if message.content.lower().find("#hello") != -1:
                await message.channel.send("Hii")
            elif message.content == "#users":
                await message.channel.send(f"Now, we have {id.member_count} members")
        else:
            print(f"user: {message.author} tried to do command {message.content}, in channel {message.channel}")


# If a member join a server
@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:  # reading every channel a member joins
        if str(channel) == "general":
            await client.send_message(f"Welcome to the server {member.mention}")

# if member change nick name
async  def on_member_update(before, after):
    n =  after.nick
    if n:
        if n.lower().count("anup")>0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="Stop!! you can't do that")


async def update_status():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}. Messages: {messages}, Members Joined: {joined}\n")

                messages = 0
                joined = 0

                await asyncio.sleep(5)
        except Exception as e:
            print(e)


# background task run
client.loop.create_task(update_status())

client.run(token)
