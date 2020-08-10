#Imports
import os, discord, threading
from bot.commands import CasesCMD, HelpCMD, SymptomsCMD, AdviceCMD
from bot.daemons import UpdateStatus, UpdateTopGG
from bot import log

registered_commands = []


def main():
    client = discord.Client()
    registered_commands.append(CasesCMD("cases"))
    registered_commands.append(HelpCMD("help"))
    registered_commands.append(SymptomsCMD("symptoms"))
    registered_commands.append(AdviceCMD("advice"))


    @client.event
    async def on_message(message):
        log("Message sent " + message.content)
        if ' ' in message.content:
            split_msg = str(message.content).split(' ')
            for i in range(len(split_msg)):
                if '' in split_msg:
                    split_msg.remove('')
        else:
            split_msg = [message.content]

        if 'c;' == split_msg[0][0:2].lower():
            command = str(split_msg[0][2:])
            args = ""
            for a in split_msg[1:]:
                args += a + " "

            ran = False
            for cmd in registered_commands:
                if cmd.command == command:
                    ran = True
                    await cmd.run(message, args)
            if not ran:
                await message.channel.send(content="Did you mean *`c;help`* ?")

    @client.event
    async def on_ready():
        log("Bot ready")
        UpdateStatus(client)
        UpdateTopGG(client)
    if os.environ['BOT_TOKEN'] == '':
        print("Please configure a bot token in your .env file")
        exit(0)
    client.run(os.environ['BOT_TOKEN'])
