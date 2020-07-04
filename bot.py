#!/usr/bin/python3

TOKEN = None

from multiprocessing import Process
from os import nice

from guild_client import GuildClient
from message_client import MessageClient
from member_update_client import MemberUpdateClient

def launch_guild_client():
    g = GuildClient()
    g.run(TOKEN)

def launch_message_client():
    m = MessageClient()
    m.run(TOKEN)

def launch_member_update_client():
    r = MemberUpdateClient()

    nice(19)

    r.run(TOKEN)

if __name__ == '__main__':
    guild_client_process = Process(
            target=launch_guild_client)

    message_client_process = Process(
            target=launch_message_client)

    guild_client_process.start()
    message_client_process.start()

    launch_member_update_client()

