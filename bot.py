# original source code found on : https://www.askpython.com/python/examples/python-discord-bot
#importing required modules
import os
import discord
import requests
import json
import random
import re

intents = discord.Intents().all()
client = discord.Client(intents=intents)

rfc_2119_keywords=["MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY","OPTIONAL",
"DOIT", "NE DOIT PAS", "DEVRAIT", "NE DEVRAIT PAS", "PEUT", "REQUIS", "OPTIONNEL",
"DOIS", "NE DOIS PAS", "DEVRAIS", "NE DEVRAIS PAS", "PEUX",
"DEVEZ", "NE DEVEZ PAS", "DEVREZ", "NE DEVREZ PAS", "POUVEZ"] #fr

reactions= ["😫","😩","🤬","🤯","😡","🤮", "😿"]
#first event :logging in
@client.event
async def on_ready():
  print("successful login as {0.user}".format(client))


def fix_message(og_msg):
    fixed_msg = og_msg
    for word in rfc_2119_keywords:
        compiled = re.compile(re.escape(word), re.IGNORECASE)
        fixed_msg = compiled.sub(word.upper(), fixed_msg)
    return fixed_msg

#second event: sending message
@client.event
async def on_message(message):
    violation_found = False
    #check who sent the message
    if message.author == client.user:
        return
    msg = message.content
    msg = msg.replace("n't", " not")
    msg = msg.replace("N't", " Not")
    msg = msg.replace("n'T", " noT")
    msg = msg.replace("N'T", " NOT")
    for keyword in rfc_2119_keywords:
        if (keyword in msg.upper() and keyword not in msg):
            violation_found = True

    if violation_found:
        await message.add_reaction(random.choice(reactions))
        await message.channel.send(f"{message.author.mention} Your message is not compliant with RFC 2119 (see : https://datatracker.ietf.org/doc/html/rfc2119). You SHOULD have written :```{fix_message(msg)}```")
        violation_found = False

token = os.environ.get("token")
#getting the secret token (please use something else than a hardcoded variable.)
client.run(token)
