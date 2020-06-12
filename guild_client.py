import re
from dbl import DBLClient
from requests import post

from base_client import BaseClient

TOKEN_TOP_GG = None

TOKEN_BOTS_ON_DISCORD = None

class BotsOnDiscordHandler:
    def __init__(self):
        self.url = None
        
        self.headers = {
                'Authorization': TOKEN_BOTS_ON_DISCORD
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
                TOKEN_TOP_GG,
                webhook_path='/dblwebhook',
                webhook_auth='password',
                webhook_port=5000)

        self.bots_on_discord = BotsOnDiscordHandler()

    async def on_ready(self):
        print("'%s' has connected to Discord!" \
                % self.name)

        await self.top_gg.post_guild_count()

        print("Server count sent to 'top.gg'.")

        await self.bots_on_discord.set_id(self.user.id)

        await self.bots_on_discord.post_guild_count()

        print("Server count sent to 'bots.ondiscord.xyz'.")

    async def on_member_join(self, member):
        c = self.db.cursor()

        c.execute(
                'select c_greeting, welcome from servers where s_id = %s',
                (member.guild.id,))

        c_greeting, welcome = c.fetchone()

        if c_greeting:
            await member.guild.get_channel(c_greeting).send(
                    re.sub(
                        '@@[Uu][Ss][Ee][Rr]@@',
                        '<@!%d>' % member.id,
                        welcome))

    async def on_member_remove(self, member):
        c = self.db.cursor()

        c.execute(
                'select c_greeting, farewell from servers where s_id = %s',
                (member.guild.id,))

        c_greeting, farewell = c.fetchone()

        if c_greeting:
            await member.guild.get_channel(c_greeting).send(
                    re.sub(
                        '@@[Uu][Ss][Ee][Rr]@@',
                        '<@!%d>' % member.id,
                        farewell))

    async def on_guild_join(self, guild):
        print(
                'Joined \'%s\' (%d): %d members, %d channels.' \
                        % (
                            guild,
                            guild.id,
                            len(guild.members),
                            len(guild.channels)))

        c = self.db.cursor()

        c.execute(
                'insert into servers (s_id, s_owner_id) values (%s, %s)',
                (guild.id, guild.owner.id))

        self.db.commit()

        await self.top_gg.post_guild_count()

        print("Server count sent to 'top.gg'.")

        await self.bots_on_discord.post_guild_count()

        print("Server count sent to 'bots.ondiscord.xyz'.")

    async def on_guild_remove(self, guild):
        print(
                'Leaving \'%s\' (%d).' \
                        % (
                            guild,
                            guild.id))

        c = self.db.cursor()

        c.execute(
                'delete from servers where s_id = %s',
                (guild.id,))

        self.db.commit()

        await self.top_gg.post_guild_count()

        print("Server count sent to 'top.gg'.")

        await self.bots_on_discord.post_guild_count()

        print("Server count sent to 'bots.ondiscord.xyz'.")
