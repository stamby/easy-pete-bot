#!/usr/bin/python3

from multiprocessing import Process
from os import getenv

from guild_client import GuildClient
from message_client import MessageClient

def launch_guild_client():
    g = GuildClient()

    g.run(getenv('TOKEN'))

def launch_message_client():
    m = MessageClient()

    m.run(getenv('TOKEN'))

if __name__ == '__main__':
    guild_client_process = Process(
            target=launch_guild_client)

    guild_client_process.start()

    launch_message_client()
    guild_client_process.join()

