import discord
import psycopg2

class BaseClient(discord.Client):
    def __init__(self, name, load_status=False):
        discord.Client.__init__(self)

        self.name = name
        self.load_status = load_status

        print("Creating a database connection for client '%s'..." \
                % name)

        self.db = psycopg2.connect(
                dbname='postgres',
                user='bot',
                password='HardPete69')

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

