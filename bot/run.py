#Imports
import discord
from bot.commands import CasesCMD, HelpCMD
from bot.daemons import UpdateStatus
from bot import getPreferences, log

registered_commands = []


def main():
    client = discord.Client()
    registered_commands.append(CasesCMD("cases"))
    registered_commands.append(HelpCMD("help"))


    @client.event
    async def on_message(message):
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
        UpdateStatus(client)
    if getPreferences()['bot_token'] == '':
        print("Please configure a bot token inside of the preferences.json file")
        exit(0)
    client.run(getPreferences()['bot_token'])


if __name__ == "__main__":
    main()
