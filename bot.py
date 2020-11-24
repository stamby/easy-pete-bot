#!/usr/bin/python3

from discord import Intents
from multiprocessing import Process
from os import getenv

from guild_client import GuildClient
from message_client import MessageClient

intents = Intents()
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True

def launch_guild_client():
    g = GuildClient(intents)

    g.run(getenv('TOKEN'))

def launch_message_client():
    m = MessageClient(intents)

    m.run(getenv('TOKEN'))

if __name__ == '__main__':
    guild_client_process = Process(
            target=launch_guild_client)

    guild_client_process.start()

    launch_message_client()
    guild_client_process.join()

