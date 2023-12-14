from setting import *

""" DO NOT EDIT
.______   ____    ____  _______   ______    __       __  ___  __  
|   _  \  \   \  /   / |   ____| /  __  \  |  |     |  |/  / |  | 
|  |_)  |  \   \/   /  |  |__   |  |  |  | |  |     |  '  /  |  | 
|   _  <    \_    _/   |   __|  |  |  |  | |  |     |    <   |  | 
|  |_)  |     |  |     |  |____ |  `--'  | |  `----.|  .  \  |  | 
|______/      |__|     |_______| \______/  |_______||__|\__\ |__| 

This code is owned by byeolki
you may be penalized if you copy the code without permission
If you do not receive a response, please contact 'byeolki0130@gmail.com'
"""

client = commands.AutoShardedBot(command_prefix=prefix, intents=discord.Intents.all(), help_command=None)
token = TOKEN

async def checkCode(msg: discord.Interaction):
    if len(msg.message.content.split(" ")) > 1:
        code = msg.message.content.split(" ")[1]
        if code == client.user.discriminator:
            return 1

@client.event
async def on_ready():
    await cogs_load()
    await client.tree.sync()
    print('대충 봇 켜진 듯?')

async def cogs_load():
    CogsFiles = [file[:-3] for file in os.listdir(fr'/root/BYEOLKI/{bot_name}/Cogs') if file.endswith(".py")]

    for file in CogsFiles:
        await client.load_extension(f"Cogs.{file}")

client.run(token)