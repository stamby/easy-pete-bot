import discord
import re

from dbl import DBLClient
from os import getenv
from requests import post

from base_client import BaseClient

class BotsOnDiscordHandler:
    def __init__(self):
        self.url = None
        
        self.headers = {
                'Authorization': getenv('TOKEN_BOTS_ON_DISCORD')
        }

    async def set_id(self, id_):
        self.url = 'https://bots.ondiscord.xyz/bot-api/bots/%d/guilds' \
                % id_

    async def post_guild_count(self):
        post(self.url, headers=self.headers)

class GuildClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self, 'Guild Client')

        self.top_gg = DBLClient(
                self,
                getenv('TOKEN_TOP_GG'),
                webhook_path='/dblwebhook',
                webhook_auth='password',
                webhook_port=5000)

        self.bots_on_discord = BotsOnDiscordHandler()

    async def on_ready(self):
        print("'%s' has connected to Discord!" \
                % self.name)

        await self.top_gg.post_guild_count()

        await self.bots_on_discord.set_id(self.user.id)

        await self.bots_on_discord.post_guild_count()

    async def on_guild_join(self, guild):
        print(
                'Joined \'%s\' (%d): %d members, %d channels.' \
                        % (
                            guild,
                            guild.id,
                            len(guild.members),
                            len(guild.channels
                        )))

        c = self.db.cursor()

        c.execute(
                'insert into servers (s_id) values (%s)',
                (guild.id,))

        self.db.commit()

        await self.top_gg.post_guild_count()

        await self.bots_on_discord.post_guild_count()

        # Send help to owners, this might fail if the server is too big
        if guild.owner:
            try:
                await guild.owner.send(
                        embed=discord.Embed(
                            colour=discord.Colour.gold(),
                            description='''
Hello, I was just invited to your server.

This is just to let you know the basics of this bot.

1) The commands _.help_ and _.admin_ offer a short summary of all the bot's features. _.Help_ will only show those features which have been activated. There is also the guide which lists every feature the bot has: https://stamby.github.io/easy-pete
2) Everything can be set up by the use of two commands: _.enable_ and _.set._ These are all you'll need to use to make the most out of this bot. They are explained in _.admin._
3) Should you need any help, you can always turn to our support server and a human being will gladly get back to you: https://discord.gg/shvcbR2
4) An invite link in case you'd like to use it: https://discord.com/oauth2/authorize?client_id=700307494580256768&permissions=268561408&scope=bot

Have fun!
                        '''))

            except:
                print(
                        'Attempted to message server owner for %s (%d): no success.' \
                                % (
                                    guild.owner.id,
                                    guild.id))

    async def on_guild_remove(self, guild):
        print(
                'Leaving \'%s\' (%d).' \
                        % (
                            guild,
                            guild.id
                        ))

        c = self.db.cursor()

        c.execute(
                'delete from servers where s_id = %s',
                (guild.id,))

        self.db.commit()

        await self.top_gg.post_guild_count()

        await self.bots_on_discord.post_guild_count()
