import discord
import psycopg2

from tokens import DB_NAME, DB_USER, DB_PASSWORD

class BaseClient(discord.Client):
    def __init__(self, name):
        discord.Client.__init__(self)

        self.name = name

        print("Creating a database connection for client '%s'..." \
                % name)

        self.db = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD)

        print(
                "Starting '%s'..." \
                        % name)

    async def on_connect(self):
        print("'%s' is connecting to Discord..." \
                % self.name)

    async def on_disconnect(self):
        print("'%s' has disconnected from Discord.'" \
                % self.name)

    async def on_resumed(self):
        print("'%s' has reconnected to Discord.'" \
                % self.name)

