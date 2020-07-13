import discord
import os
import random
import re
import sys

from base_client import BaseClient

import credentials

import commands.about
import commands.admin
import commands.disable
import commands.enable
import commands.help
import commands.iam
import commands.meme
import commands.prune
import commands.set
import commands.someone
import commands.song

class MessageClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self, 'Message Client')

        self.mention = None

        self.invite_regex = re.compile(
                'discord((app)?\.com/invite\/[^ ]|\.gg\/[^ ])')

        self.mass_mention_regex = re.compile(
                '(<@![0-9]+>.*?){4,}')

        self.profanity_regex = re.compile(
                '[Ss][Uu][Cc][CcKk][Ee][Rr]|([Ss][Uu][Cc][Kk].*[Dd]|d)[Ii][Cc][Kk]|[Dd][Ii][Cc][Kk][Hh][Ee][Aa][Dd]|[Ff][Uu][Cc][CcKk]|[Ff][Aa][Gg]{2}[Oo][Tt]|[Nn][Ii][Gg]{2}([Aa]|[Ee][Rr])|[Rr][Ee][Tt][Aa][Rr][Dd]|[Ii][Dd][Ii][Oo][Tt]|[Ss][Tt][Uu][Pp][Ii][Dd]|(^|[^a-z])[Aa][Ss]{2}|(^|[^a-z])[Aa][Rr][Ss][Ee]|(^|[^a-z])[Aa][Nn][Uu][Ss]|(^|[^a-z])[Cc][Oo][Cc][CcKk]|[Dd][Aa][RrMm][Nn]|[Cc][Uu][Nn][Tt]|[Cc][Rr][Aa][Pp]|[Bb][Uu][Gg]{2}[Ee][Rr]|[Bb][Ii][Tt][Cc][Hh]|[Bb][Uu][Ll]{2}[Ss][Hh][Ii][Tt]|[Pp][Rr][Ii][Cc][Kk]|[Pp][Uu][Nn]{1,2}[Aa][Nn][IiYy]|[Pp][Uu][Ss]{2}[Yy]|[Ss][Nn][Aa][Tt][Cc][Hh]|[Ss][Hh][Aa][Gg]|[Hh][Oo][Ee]|[Ww][Hh][Oo][Rr][Ee]')

    async def on_ready(self):
        print("'%s' has connected to Discord!" \
                % self.name)

        self.mention = '<@!%d>' % self.user.id

        c = self.db.cursor()

        c.execute(
                'select status from bot')

        status = c.fetchone()

        if status:
            await self.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.listening,
                        name=status[0]))

            print("Status loaded from database: '%s'." \
                    % status[0])

        c.close()

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        # Check for profanity
        if self.profanity_regex.search(message.content):
            c = self.db.cursor()

            c.execute(
                        '''
select filter_profanity, filter_action from servers where s_id = %s
                        ''',
                        (message.guild.id,))

            filter_profanity, filter_action = c.fetchone()

            if not filter_profanity or not filter_action:
                return

            warning = filter_action == 1 or filter_action == 2
            deleting = filter_action == 2 or filter_action == 3

            if warning:
                await message.channel.send(
                        random.choice((
                            '''
<@!%d>, our server has been set up to discourage the use of swearing. Please be nice.
                            ''',
                            '''
<@!%d>: Please adhere to our server's Victorian values by avoiding undisguised, foul language.
                            ''',
                            '''
<@!%d>, we like all kinds of debauchery here but not swear words! Please avoid using them.
                            ''',
                            '''
Please make sure you don't use any swear words, <@!%d>.
                            ''',
                            '''
<@!%d>: There is one thing you might not know about swear words on this server: We don't use them.
                            ''')) \
                                    % message.author.id)

            if deleting:
                await message.delete()

        elif self.mass_mention_regex.search(message.content):
            c = self.db.cursor()

            c.execute(
                    '''
select filter_mass_mention, filter_action from servers where s_id = %s
                    ''',
                    (message.guild.id,))

            filter_mass_mention, filter_action = c.fetchone()

            if not filter_mass_mention or not filter_action:
                return

            warning = filter_action == 1 or filter_action == 2
            deleting = filter_action == 2 or filter_action == 3

            if warning:
                await message.channel.send(
                        random.choice((
                            '''
<@!%d>: Up to three mentions may be sent per message.
                            ''',
                            '''
<@!%d>: Please don't mention more than three times at one message.
                            ''',
                            '''
<@!%d>, there should be no need to mention that many times in one message. If it is important, please message each person privately instead.
                            ''',
                            '''
Mass mentions are discouraged, <@!%d>.
                            ''',
                            '''
Please don't send so many mentions, <@!%d>.
                            ''')) \
                                    % message.author.id)

            if deleting:
                await message.delete()

        elif self.invite_regex.search(message.content):
            c = self.db.cursor()

            c.execute(
                    '''
select filter_invite, filter_action from servers where s_id = %s
                    ''',
                    (message.guild.id,))

            filter_invite, filter_action = c.fetchone()

            if not filter_invite or not filter_action:
                return

            warning = filter_action == 1 or filter_action == 2
            deleting = filter_action == 2 or filter_action == 3

            if warning:
                await message.channel.send(
                        random.choice((
                            "Please don't advertise your server here, <@!%d>.",
                            'Server invites are discouraged, <@!%d>.')) \
                                    % message.author.id)

            if deleting:
                await message.delete()

        elif message.content.startswith('.'):
            if re.match(
                    '^\.[Hh][Ee][Ll][Pp]( |$)',
                    message.content):
                # `.help'
                await commands.help.run(message, self.db)

            elif re.match(
                    '^\.[Aa][Dd][Mm][Ii][Nn]( |$)',
                    message.content):
                # `.admin'
                await commands.admin.run(message, self.db)

            elif re.match(
                    '^\.[Mm][Ee][Mm][Ee]( |$)',
                    message.content):
                # `.meme'
                await commands.meme.run(message, self.db, credentials)

            elif re.match(
                    '^\.[Ss][Oo][Nn][Gg]( |$)',
                    message.content):
                # `.song'
                await commands.song.run(message, self.db, credentials)

            elif re.match(
                    '^\.[Ii][Aa][Mm]([Nn][Oo][Tt])?( |$)',
                    message.content):
                # `.iam' and `.iamnot'
                await commands.iam.run(
                        message,
                        self.db,
                        self.user.id,
                        credentials)

            elif re.match(
                    '^\.[Pp][Rr][Uu][Nn][Ee]( |$)',
                    message.content):
                # `.prune'
                await commands.prune.run(message, self.db)

            elif re.match(
                    '^\.[Ee][Nn][Aa][Bb][Ll][Ee]( |$)',
                    message.content):
                # `.enable'
                await commands.enable.run(message, self.db)

            elif re.match(
                    '^\.[Dd][Ii][Ss][Aa][Bb][Ll][Ee]( |$)',
                    message.content):
                # `.disable'
                await commands.disable.run(message, self.db)


            elif re.match(
                    '^\.[Ss][Ee][Tt]( |$)',
                    message.content):
                # `.set'
                await commands.set.run(message, self.db)

            elif re.match(
                    '^\.[Aa][Bb][Oo][Uu][Tt]( |$)',
                    message.content):
                # `.about'
                await commands.about.run(message, credentials)

            if message.author.id == credentials.OWNER_ID:
                if message.content.startswith('.update '):
                    c.execute(
                            '''
select s_id, c_updates from servers where c_updates is not null
                            ''')

                    while True:
                        s_id_and_c_updates = c.fetchone()

                        if not s_id_and_c_updates:
                            break

                        channel = self.get_guild(
                                s_id_and_c_updates[0]).get_channel(
                                        s_id_and_c_updates[1])

                        await channel.send(
                                embed=discord.Embed(
                                    title='ANNOUNCEMENT',
                                    colour=discord.Colour.gold(),
                                    description=message.content[8:]))

                elif message.content.startswith('.status'):
                    c = self.db.cursor()

                    status = message.content[8:]

                    if status == '':
                        status = None

                    c.execute(
                            'update bot set status = %s',
                            (status,))

                    self.db.commit()

                    await self.change_presence(
                            activity=discord.Activity(
                                type=discord.ActivityType.listening,
                                name=status))

                    if status:
                        print(
                                'Status set to \'%s\'.' % status)
                    else:
                        print(
                                'Status cleared.')

                elif message.content == '.stop':
                    print(
                            'Stop requested through "%s" (%d), stopping.' \
                                    % (
                                        message.guild,
                                        message.guild.id))

                    self.db.close()
                    await self.close()

        elif re.match(
                '@[Ss][Oo][Mm][Ee][Oo][Nn][Ee]',
                message.content):
            # `@someone'
            await commands.someone.run(message, self.db)

        elif message.content == self.mention:
            await message.channel.send(
                    random.choice((
                        '<@!%d>: What is your command?',
                        '<@!%d>: Yes?',
                        '<@!%d>: I\'m listening.',
                        'Do you need anything, <@!%d>?',
                        'How may I help you, <@!%d>?',
                        'Ready when you are, <@!%d>.')) \
                                % message.author.id)

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
            # `.song' command
            c = self.db.cursor()

            if payload.emoji.name == '👍':
                c.execute(
                        'update songs set yes = yes + 1 where url = %s',
                        (message.content,))

            elif payload.emoji.name == '👎':
                c.execute(
                        'update songs set no = no + 1 where url = %s',
                        (message.content,))

            else:
                return

            self.db.commit()

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
            # `.song' command
            c = self.db.cursor()

            if payload.emoji.name == '👍':
                c.execute(
                        'update songs set yes = yes - 1 where url = %s',
                        (message.content,))

            elif payload.emoji.name == '👎':
                c.execute(
                        'update songs set no = no - 1 where url = %s',
                        (message.content,))

            else:
                return

            self.db.commit()
