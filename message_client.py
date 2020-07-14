import discord
import re

from base_client import BaseClient

import credentials

import commands.about
import commands.admin
import commands.disable
import commands.enable
import commands.help
import commands.iam
import commands.meme
import commands.mention
import commands.prune
import commands.set
import commands.someone
import commands.song

import filters.invite
import filters.mass_mention
import filters.profanity

import reactions.song

import status

class MessageClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self, 'Message Client')

        self.mention = None

    async def on_ready(self):
        print("'%s' has connected to Discord!" \
                % self.name)

        self.mention = '<@!%d>' % self.user.id

        await status.load(self)

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if filters.profanity.regex.search(message.content):
            filters.profanity.run(message, self.db)

        elif filters.mass_mention.regex.search(message.content):
            filters.mass_mention.run(message, self.db)

        elif filters.invite.regex.search(message.content):
            filters.invite.run(message, self.db)

        elif message.content.startswith('.'):
            if commands.help.regex.match(message.content):
                commands.help.run(message, self.db)

            elif commands.admin.regex.match(message.content):
                commands.admin.run(message, self.db)

            elif commands.meme.regex.match(message.content):
                commands.meme.run(message, self.db, credentials)

            elif commands.song.regex.match(message.content):
                commands.song.run(message, self.db, credentials)

            elif commands.iam.regex.match(message.content):
                commands.iam.run(
                        message,
                        self.db,
                        self.user.id,
                        credentials)

            elif commands.prune.regex.match(message.content):
                commands.prune.run(message, self.db)

            elif commands.enable.regex.match(message.content):
                commands.enable.run(message, self.db)

            elif commands.disable.regex.match(message.content):
                commands.disable.run(message, self.db)

            elif commands.set.regex.match(message.content):
                commands.set.run(message, self.db)

            elif commands.about.regex.match(message.content):
                commands.about.run(message, credentials)

            if message.author.id == credentials.OWNER_ID:
                if message.content.startswith('.update '):
                    commands.update.run(message, self)

                elif message.content.startswith('.status'):
                    await status.change(message, self)

                elif message.content == '.stop':
                    print(
                            'Stop requested through "%s" (%d), stopping.' \
                                    % (
                                        message.guild,
                                        message.guild.id
                                    ))

                    self.db.close()
                    await self.close()

        elif commands.someone.regex.match(message.content):
            commands.someone.run(message, self.db)

        elif message.content == self.mention:
            commands.mention.run(message)

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id \
                or payload.emoji.name not in ('👍', '👎'):
            return

        message = await self.get_channel(
                payload.channel_id).fetch_message(
                        payload.message_id)

        if message.author.id != self.user.id:
            return

        if message.content.startswith(
                'http'):
            reactions.song.add(
                    message,
                    payload,
                    self.db)

    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.user.id \
                or payload.emoji.name not in ('👍', '👎'):
            return

        message = await self.get_channel(
                payload.channel_id).fetch_message(
                        payload.message_id)

        if message.author.id != self.user.id:
            return

        if message.content.startswith(
                'http'):
            reactions.song.remove(
                    message,
                    payload,
                    self.db)

