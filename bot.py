#!/usr/bin/python3

from discord import Intents
from multiprocessing import Process
from os import getenv

from guild_client import GuildClient
from message_client import MessageClient

def launch_guild_client():
    intents = Intents()

    intents.guilds = True

    g = GuildClient(intents)

    g.run(getenv('TOKEN'))

def launch_message_client():
    intents = Intents()

    intents.messages = True
    intents.members = True
    intents.reactions = True

    m = MessageClient(intents)

    m.run(getenv('TOKEN'))

if __name__ == '__main__':
    guild_client_process = Process(
            target=launch_guild_client)

    guild_client_process.start()

    launch_message_client()
    guild_client_process.join()

