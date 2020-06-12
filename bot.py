#!/usr/bin/python3

TOKEN = None

from multiprocessing import Process
from os import nice

from guild_client import GuildClient
from message_client import MessageClient
from role_cleanup_client import RoleCleanupClient

def launch_guild_client():
    g = GuildClient()
    g.run(TOKEN)

def launch_message_client():
    m = MessageClient()
    m.run(TOKEN)

def launch_role_cleanup_client():
    r = RoleCleanupClient()

    nice(19)

    r.run(TOKEN)

if __name__ == '__main__':
    guild_client_process = Process(
            target=launch_guild_client)

    role_cleanup_client_process = Process(
            target=launch_role_cleanup_client)

    guild_client_process.start()
    role_cleanup_client_process.start()
    
    launch_message_client()

