import discord
import re

from dbl import DBLClient
from os import getenv
from requests import post

from base_client import BaseClient

class BotHandler:
    def __init__(self, bot, token):
        self.url = None
        self.bot = bot

        self.headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
        }

    async def post_guild_count(self):
        json_ = {
                'guildCount': len(self.bot.guilds)
        }

        post(self.url, headers=self.headers, json=json_)

class DiscordBotsHandler(BotHandler):
    async def set_url(self):
        self.url = 'https://discord.bots.gg/api/v1/bots/%d/stats' \
                % self.bot.user.id

class BotsOnDiscordHandler(BotHandler):
    async def set_url(self):
        self.url = 'https://bots.ondiscord.xyz/bot-api/bots/%d/guilds' \
                % self.bot.user.id

class GuildClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(
                self, 'Guild Client')

        self.top_gg = DBLClient(
                self,
                getenv('TOKEN_TOP_GG'),
                webhook_path='/dblwebhook',
                webhook_auth='password',
                webhook_port=5000)

        self.bots_on_discord = BotsOnDiscordHandler(
                self, getenv('TOKEN_BOTS_ON_DISCORD'))

        self.discord_bots = DiscordBotsHandler(
                self, getenv('TOKEN_DISCORD_BOTS'))

    async def on_ready(self):
        print("'%s' has connected to Discord!" \
                % self.name)

        await self.bots_on_discord.set_url()
        await self.discord_bots.set_url()

        await self.announce()

    async def on_guild_join(self, guild):
        print(
                'Joined \'%s\' (%d).' \
                        % (
                            guild,
                            guild.id
                        ))

        c = self.db.cursor()

        c.execute(
                'insert into servers (s_id) values (%s)',
                (guild.id,))

        self.db.commit()

        await self.announce()

        # Send help to the owner, this might fail if the server is too big
        if guild.owner:
            try:
                await guild.owner.send(
                        embed=discord.Embed(
                            colour=discord.Colour.gold(),
                            description='''
Hello, I was just invited to your server.

This is just to let you know the basics of this bot.

1) The commands _.help_ and _.admin_ offer a short summary of all the bot's features. _.Help_ will only show those features that have been activated. There is also the guide, which lists every feature the bot has: https://stamby.github.io/easy-pete-bot
2) Everything can be set up by the use of two commands: _.enable_ and _.set._ These are all you'll need to use to make the most out of this bot. They are explained in _.admin._
3) Should you need any help, you can always turn to our support server and a human being will get back to you: https://discord.gg/shvcbR2
4) An invite link in case you'd like to use it: https://discord.com/oauth2/authorize?client_id=700307494580256768&permissions=268561408&scope=bot

We hope you have fun with the bot!
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

        await self.announce()

    async def announce(self):
        try:
            await self.bots_on_discord.post_guild_count()
        except:
            print('Could not submit data to Bots on Discord.')
        try:
            await self.discord_bots.post_guild_count()
        except:
            print('Could not submit data to Discord Bots.')
        try:
            await self.top_gg.post_guild_count()
        except:
            print('Could not submit data to Top GG.')
