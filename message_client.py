from datetime import datetime
import discord
import os
import random
import re
import sys

from base_client import BaseClient

class Credentials:
    BOT_NAME = 'Easy Pete'
    BOT_NAME_REGEX = '[Pp][Ee][Tt][Ee]'
    MEME_DIR_ALL_AUDIENCES = '/home/bot/meme/stock/all_audiences'
    MEME_DIR_OVER_EIGHTEEN = '/home/bot/meme/stock/over_eighteen'
    MEME_SUBMISSIONS = '/home/bot/meme/submissions'
    OWNER_ID = 144086385668653056

class MessageClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self, 'Message Client')

    async def on_ready(self):
        print("'%s' has connected to Discord!" \
                % self.name)

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

    async def get_all_fields(self):
        c = self.db.cursor()

        c.execute('''
select column_name from information_schema.columns where table_name = 'servers'
and column_name != 'id' and column_name != 'added_on'
                ''')

        fields_tuple = c.fetchall()

        c.close()

        fields = []
        for field in fields_tuple:
            fields.append(field[0])

        return fields

    async def get_c_fields(self):
        c = self.db.cursor()

        c.execute('''
select column_name from information_schema.columns where table_name = 'servers'
and column_name like 'c_%'
                ''')

        c_fields_tuple = c.fetchall()

        c.close()

        c_fields = []
        for field in c_fields_tuple:
            c_fields.append(field[0])

        return c_fields

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if message.content.startswith('.'):
            c = self.db.cursor()

            if message.content == '.help':
                c.execute(
                        'select c_iam, c_meme, c_song, someone from servers where s_id = %s',
                        (message.guild.id,))

                c_iam, c_meme, c_song, someone = c.fetchone()

                description = ''

                if c_iam:
                    description += '''
**.iam** (role name): Assign yourself a role. If the role doesn't exist, it may be created depending on settings.

**.iamnot** (role name): Remove a role from your user. If no users have the role anymore, the role may be removed depending on settings.
'''

                if c_meme:
                    description += '''
**.meme**: Send a random meme, straight from our repositories. Submit a meme by writing _.meme submit._
'''

                if c_song:
                    description += '''
**.song**: Send a good song for your happy ears. 

Optionally:
**.song search** (artist and/or title)
**.song genre** (music genre)
**.song add** (Youtube URL)
**.song all**
'''

                if someone:
                    description += '''
**@someone**: Randomly mention someone on the server.
'''

                description += '''
**.admin**: More commands for admins. It shows help on how to manage the bot's features.

**.links**: Show the links to invite the bot to a new server and to contact the devs in case there is an issue, or if you would like to suggest an improvement.
'''

                if not c_iam or not c_meme or not c_song or not someone:
                    description += '''
More commands can be enabled. Admins may add them by use of _.enable_ and _.set,_ described in _.admin._
'''

                await message.channel.send(
                        embed=discord.Embed(
                            title='ALL COMMANDS',
                            colour=discord.Colour.gold(),
                            description=description))

            elif message.content == '.admin':
                permissions = message.channel.permissions_for(
                        message.author)

                if not permissions.manage_channels \
                        and not permissions.manage_messages \
                        and not permissions.manage_guild:
                    await message.channel.send(
                            'The _.admin_ message is directed towards people who have _Manage Channels, Manage Messages_ or _Manage Server_ permission.')
                    return

                await message.channel.send(
                        embed=discord.Embed(
                            title='FOR ADMINS ONLY',
                            colour=discord.Colour.gold(),
                            description='''
**.prune** (amount) or **.prune** (user) (amount): Requires _Manage Messages_ permission. Delete messages from a channel, starting by the latest. If a user precedes the amount, delete messages from that user only.
Example: _.prune @a user I don't like 100_

**SETTING UP THE BOT**

**.enable** or **.disable** (commands): Requires _Manage Channels_ permission. Enable or disable one or more commands for the current channel. Valid commands:
**greeting**: To send greeting messages to this channel.
**iam**: To reply to _.iam_ and _.iamnot_ on this channel.
**song**: Likewise for _.song._
**meme**: Likewise for _.meme._
**updates**: Updates about the bot.
All of them are disabled by default. Note that this means that they will not work, unless enabled.
Example: _.enable greeting iam_

**.set** (property) (value) or **.set**: Requires _Manage Server_ permission. Define properties that change the way the bot behaves. If no property is given, show current values. Valid properties:
**welcome**: A greeting for when a user joins. Writing _@@USER@@_ in it will mention the user in question.
Example: _.set welcome Welcome, @@USER@@!_ (default)
**farewell**: Likewise when someone leaves.
Example: _.set farewell @@USER@@ has left the server._ (default)
**max\_deletions**: The maximum amount of messages that _.prune_ may delete. The default value is 10.
Example: _.set max\_deletions 100_
**role\_create**: Whether _.iam_ should create a non-existing role. If disabled, it has no effect. Value should be _true_ or _false._ Default value: _false._
Example: _.set role\_create false_
**role\_cleanup**: Whether the bot should remove any unused roles. Value should be _true_ or _false._ Default value: _false._
**someone**: Whether _@someone_ is allowed. Value should be _true_ or _false._ Default value: _true._
**meme\_filter**: Filter memes sent by _.meme._ Value should be _true_ or _false._ Default value: _true._

To report an issue, please run _.links._
                    '''))

            elif message.content.startswith('.meme'):
                # Check whether it is enabled for this channel
                c.execute(
                        'select c_meme, meme_filter from servers where s_id = %s',
                        (message.guild.id,))

                c_meme, meme_filter = c.fetchone()

                if not c_meme:
                    await message.channel.send(
                            'To enable this command, type _.enable meme._')
                    return

                if message.channel.id != c_meme:
                    await message.channel.send(
                            'Memes go in <#%d>.' \
                                    % c_meme)
                    return

                # Parse the message
                trailing_space, command, extra_chars = re.findall(
                        '^\.meme( *)((?:submit$)?)(.*)',
                        message.content)[0]

                if extra_chars != '':
                    if trailing_space == '':
                        # Ignore non-command
                        return
                    
                    await message.channel.send(
                            'The only valid option to the _.meme_ command is the word _submit._')
                    return

                if command == 'submit':
                    if len(message.attachments) == 0:
                        await message.channel.send(
                                'A submission requires an attachment. Please try again.')
                        return

                    if len(message.attachments) != 1:
                        await message.channel.send(
                                'Only one attachment allowed per submission.')
                        return

                    if not message.attachments[0].height:
                        await message.channel.send(
                                'A valid attachment must be either an image or video.')
                        return

                    if message.attachments[0].size > 8388608:
                        await message.channel.send(
                                'The size of the attachment needs not to exceed 8 MB.')
                        return

                    with open(
                            os.path.join(
                                Credentials.MEME_SUBMISSIONS,
                                '%d_%s' \
                                    % (
                                        message.attachments[0].id,
                                        message.attachments[0].filename)),
                            'wb') as f:
                        await message.attachments[0].save(f)

                    await message.channel.send(
                            'Submitted for review.')

                else:
                    if not meme_filter and not message.channel.nsfw:
                        # Channel was not marked as NSFW, therefore
                        # force filtering
                        meme_filter = 1

                    if meme_filter:
                        dir_ = Credentials.MEME_DIR_ALL_AUDIENCES

                    else:
                        dir_ = random.choice((
                            Credentials.MEME_DIR_ALL_AUDIENCES,
                            Credentials.MEME_DIR_OVER_EIGHTEEN))

                    file_ = random.choice(
                            os.listdir(dir_))

                    with open(
                            os.path.join(dir_, file_),
                            'rb') as f:
                        await message.channel.send(
                                file=discord.File(
                                    fp=f,
                                    filename=file_))

            elif message.content.startswith('.song'):
                # Check whether it is enabled for this channel
                c.execute(
                        'select c_song from servers where s_id = %s',
                        (message.guild.id,))

                c_song = c.fetchone()[0]

                if not c_song:
                    await message.channel.send(
                            'Please enable this command by means of _.enable song._')
                    return

                if message.channel.id != c_song:
                    await message.channel.send(
                            'Songs will be sent on <#%d>.' \
                                    % c_song)
                    return

                # Parse the message
                trailing_space, command, extra_chars = re.findall(
                        '^\.song( *)((?:all$|add +(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]+$|search .+|genre(?: .+|$))?)(.*)',
                        message.content)[0]

                if trailing_space == '' and command == '':
                    if extra_chars != '':
                        # Ignore non-command
                        return

                    # No command is being provided, therefore send a random song from the DB
                    c.execute(
                            'select count(*) from songs')

                    c.execute(
                            'select url from songs where id = %s',
                            (random.randrange(1, c.fetchone()[0]),))

                    await message.channel.send(
                            c.fetchone()[0])

                elif command == 'all':
                    c.execute(
                            '''
select '<li><strong>' || artist || '</strong>, "' ||
title || '" <em>(' || genre || ')</em></li>'
from songs order by genre, artist, title
                            ''')

                    file_ = '/tmp/discord_bot_all_songs_%d.html' \
                            % random.randrange(65536)

                    print(
                            'All songs requested by %s (%d) on "%s" (%d), fetching songs.' \
                                    % (
                                        message.author,
                                        message.author.id,
                                        message.guild,
                                        message.guild.id))

                    with open(file_, 'w', encoding='utf-8') as f:
                        f.write(
                                '<html><head><title>%s</title></head><body><h1>%s\'S SONGS</h1><ul>' \
                                        % (
                                            Credentials.BOT_NAME,
                                            Credentials.BOT_NAME.upper()))

                        while True:
                            line = c.fetchone()

                            if not line:
                                break

                            f.write(line[0])

                        f.write(
                                datetime.utcnow().strftime(
                                    '</ul><p>Fetched on %A %-d %B %y, %-I:%M %p (UTC).</p></body></html>'))

                    with open(file_, 'r') as f:
                        await message.channel.send(
                                embed=discord.Embed(
                                    title='ALL SONGS',
                                    colour=discord.Colour.gold(),
                                    description='''
The attached file contains all my songs.

You can add to these songs by running _.song add (Youtube URL)_ and search them through _.song search (artist, title or both)._

This list changes often. It is up to date as of this very moment.
                                    '''),
                                file=discord.File(
                                    fp=f,
                                    filename='%s_songs.html' \
                                            % Credentials.BOT_NAME.lower()))

                    os.remove(file_)

                    print(
                            'Songs sent to "%s" (%d).' \
                                    % (
                                        message.guild,
                                        message.guild.id))

                elif command.startswith('add'):
                    url = re.split(' +', command)[1]

                    c.execute(
                            'select id from songs where url = %s',
                            (url,))

                    if c.fetchone():
                        await message.channel.send(
                                'Song is already in the database.')
                        return

                    c.execute(
                            'select id from song_requests where url = %s',
                            (url,))

                    if c.fetchone():
                        await message.channel.send(
                                'Song has already been requested.')
                        return

                    c.execute(
                            'insert into song_requests (time, solicitor, s_id, url) values (%s, %s, %s, %s)',
                            (
                                datetime.now().strftime('%F %H:%M:%S.%f'),
                                message.author.id,
                                message.guild.id,
                                url))

                    self.db.commit()

                    print(
                            'Song \'%s\' has been requested for review.' % url)

                    await message.channel.send(
                            'Submitted for review.')

                elif command.startswith('search'):
                    like = '%%%s%%' % re.sub(
                            '[^A-Za-z0-9_-]+', '%', command[7:])

                    c.execute(
                            '''
select url from songs where artist || title like %s or title || artist like %s
                            ''',
                            (like, like))

                    match = c.fetchall()

                    if match:
                        await message.channel.send(
                                random.choice(match)[0])

                    else:
                        await message.channel.send(
                                'No matches. Submit a URL by typing _.song add (Youtube URL)._')

                elif command.startswith('genre'):
                    requested_genre = command[6:]

                    if requested_genre == '':
                        c.execute(
                                'select distinct genre from songs order by 1')

                        available_genres = c.fetchall()

                        available_genres_str = ''

                        for genre in available_genres:
                            available_genres_str += ', %s' % genre

                        await message.channel.send(
                                'The available genres are _%s._' \
                                        % available_genres_str[2:])
                        return

                    c.execute(
                            'select url from songs where genre = %s',
                            (requested_genre,))

                    match = c.fetchall()

                    if match:
                        await message.channel.send(
                                random.choice(match)[0])

                    else:
                        await message.channel.send(
                                'No matches. Type _.song genre_ to see all available music genres.')
                        return

                else:
                    await message.channel.send(
                            'An invalid command has been supplied. Please type _.help_ to see valid options to the _.song_ command.')

            elif message.content.startswith('.iam'):
                # Parse message
                command, trailing_space, requested_role_name = re.findall(
                        '^\.iam((?:not)?)( *)(.*)',
                        message.content)[0]

                if trailing_space == '' and requested_role_name != '':
                    # Ignore non-command
                    return

                # Check whether it is enabled for this channel
                c.execute(
                        'select c_iam, role_create from servers where s_id = %s',
                        (message.guild.id,))

                c_iam, role_create = c.fetchone()

                if not c_iam:
                    await message.channel.send(
                            'The command _.iam%s_ is not available. An admin may enable it by entering _.enable iam._' \
                                    % command)
                    return

                if message.channel.id != c_iam:
                    await message.channel.send(
                            'This command is to be run on <#%d>.' \
                                    % c_iam)
                    return

                # Get the role that gives us the 'manage roles' permission
                own_role = None

                roles = message.guild.get_member(
                    self.user.id).roles

                i = len(roles) - 1

                while i >= 0:
                    if roles[i].permissions.manage_roles:
                        own_role = roles[i]
                        break

                    i -= 1

                if not own_role:
                    await message.channel.send(
                            'Insufficient permissions. Namely, this command requires me to have _Manage Roles_ permission.')
                    return

                if requested_role_name == '':
                    await message.channel.send(
                            'Please write _.iam%s_ followed by the role name.' \
                                    % command)
                    return

                requested_role_name_lower = requested_role_name.lower()

                # Check whether the requested role exists
                existing_role = None
                for role in message.guild.roles:
                    if role.name.lower() == requested_role_name_lower:
                        existing_role = role
                        break

                # Remember whether we had 'not' in the command
                if command == 'not':
                    if not existing_role:
                        await message.channel.send(
                                'The role _%s_ does not exist. Maybe check your spelling?' \
                                        % requested_role_name) 
                        return

                    if existing_role not in message.author.roles:
                        await message.channel.send(
                                'The role _%s_ has not been assigned to you.' \
                                        % existing_role.name) 
                        return

                    elif existing_role > own_role:
                        await message.channel.send(
                                'The role _%s_ is too high on the list for me to remove it. I would need mine to be higher than the role that is to be removed.' \
                                        % existing_role.name) 
                        return

                    await message.author.remove_roles(
                            existing_role,
                            reason='Self-removed')
                    await message.channel.send(
                            '_%s_ removed.' \
                                    % existing_role.name)

                else:
                    # We are adding him the role
                    # Check whether the user has got this role
                    if existing_role in message.author.roles:
                        await message.channel.send(
                                'The role _%s_ has already been assigned to you.' \
                                        % existing_role.name) 
                        return

                    # If the role doesn't exist
                    if not existing_role:
                        # Check whether we are allowed to create it
                        if role_create == 0:
                            await message.channel.send(
                                    'The role _%s_ doesn\'t exist and cannot be created due to bot settings for this server.' \
                                            % requested_role_name)
                            return

                        # Create the role
                        existing_role = await message.guild.create_role(
                                name=requested_role_name,
                                reason='Created by %s on %s\'s request' \
                                        % (
                                            Credentials.BOT_NAME,
                                            message.author),
                                colour=discord.Colour.from_rgb(
                                    random.randrange(255),
                                    random.randrange(255),
                                    random.randrange(255)),
                                hoist=True)

                    elif existing_role.permissions.value != 0:
                        # If the role's permissions differ from the default ones
                        await message.channel.send(
                                '_%s_ is an already-existing role with additional permissions. Please ask an admin to remove all permissions from the role before you may add it.' \
                                        % existing_role.name)
                        return

                    elif existing_role > own_role:
                        # If the role can't be changed due to its position in the hierarchy
                        await message.channel.send(
                                'The role _%s_ is higher on the list than the one that allows me to manage other roles. I would need mine to be higher so I can add you the one you requested. Please ask an admin for assistance.' \
                                        % existing_role.name)
                        return

                    await message.author.add_roles(
                            existing_role,
                            reason='Self-assigned',
                            atomic=True)

                    await message.channel.send(
                            '_%s_ assigned.' \
                                    % existing_role.name)

            elif message.content.startswith('.prune'):
                # Parse the message
                trailing_space, user_str, requested_amount_str, extra_chars = re.findall(
                        '^\.prune( *)((?:<@![0-9]+>)?) *((?:[0-9]+$)?)(.*)',
                        message.content)[0]

                if trailing_space == '' and extra_chars != '':
                    # Ignore non-command
                    return

                c.execute(
                        'select max_deletions from servers where s_id = %s',
                        (message.guild.id,))

                max_deletions = c.fetchone()[0]

                # Check whether the user has the appropriate permissions
                if not message.channel.permissions_for(
                        message.author).manage_messages:
                    await message.channel.send(
                            'The _.prune_ command has to come from someone having the _Manage Messages_ permission for this channel.')
                    return

                if max_deletions == 0:
                    await message.channel.send(
                            'The _.prune_ command has been disabled. An admin may type _.set max\_deletions (number)_ to change this.')
                    return

                if requested_amount_str != '':
                    requested_amount = int(requested_amount_str)

                    if requested_amount > max_deletions:
                        effective_amount = max_deletions

                    else:
                        effective_amount = requested_amount

                    if user_str == '':
                        effective_amount += 1

                        async for line in message.channel.history(
                                limit=effective_amount):
                            await line.delete()

                    else:
                        user = int(re.findall('[0-9]+', user_str)[0])

                        await message.delete()

                        count = 0

                        async for line in message.channel.history():
                            if user == line.author.id:
                                await line.delete()

                                count += 1

                                if count >= effective_amount:
                                    break

                    if requested_amount > max_deletions:
                        await message.channel.send(
                                'For security reasons, only up to %d messages may be deleted. Type _.set max\_deletions (number)_ to change this.' \
                                        % max_deletions)

                else:
                    await message.channel.send(
                            'Invalid syntax for the _.prune_ command.')

            elif message.content.startswith('.enable'):
                # Check whether the user has the appropriate permissions
                if not message.channel.permissions_for(
                        message.author).manage_channels:
                    await message.channel.send(
                            'The _.enable_ command has to come from someone having the _Manage Channels_ permission for this channel.')
                    return

                commands = re.findall(
                        '[^ ]+', message.content[8:].lower())

                if len(commands) == 0:
                    await message.channel.send(
                            'Which command would you like to enable?')
                    return

                c_fields = await self.get_c_fields()

                for command in commands:
                    if 'c_' + command not in c_fields:
                        await message.channel.send(
                                'The command _%s_ is not valid. Please type _.admin_ to see which commands may be enabled.' \
                                        % command)
                        return

                commands_str = ''

                for command in commands:
                    c.execute(
                            'update servers set c_{} = %s where s_id = %s'.format(command),
                            (
                                message.channel.id,
                                message.guild.id))

                    commands_str += ', %s' % command

                self.db.commit()

                await message.channel.send(
                        'The following commands have been reserved for this channel: _%s._' \
                                % commands_str[2:])

            elif message.content.startswith('.disable'):
                # Check whether the user has the appropriate permissions
                if not message.channel.permissions_for(
                        message.author).manage_channels:
                    await message.channel.send(
                            'The _.disable_ command has to come from someone having the _Manage Channels_ permission for this channel.')
                    return

                commands = re.findall(
                        '[^ ]+', message.content[9:].lower())

                if len(commands) == 0:
                    await message.channel.send(
                            'Which command would you like to disable?')
                    return

                c_fields = await self.get_c_fields()

                for command in commands:
                    if 'c_' + command not in c_fields:
                        await message.channel.send(
                                '_%s_ is not valid. Please type _.admin_ to see which commands may be disabled.' \
                                        % command)
                        return

                commands_str = ''

                for command in commands:
                    c.execute('''
update servers set c_{} = null where s_id = %s
                            '''.format(command),
                            (
                                message.guild.id))

                    commands_str += ', %s' % command

                self.db.commit()

                await message.channel.send(
                        'The following commands have been disabled: _%s._' \
                                % commands_str[2:])

            elif message.content.startswith('.set'):
                # Check whether the user has the appropriate permissions
                if not message.channel.permissions_for(
                        message.author).manage_guild:
                    await message.channel.send(
                            'The _.set_ command may be run only by someone having the _Manage Server_ permission.')
                    return

                trailing_space, command, value = re.findall(
                        '^\.set( *)((?:[^ ]+)?) *(.*)$',
                        message.content)[0]

                if trailing_space == '':
                    if command != '':
                        # Ignore non-command
                        return

                    # Just print everything
                    fields = await self.get_all_fields()

                    fields_str = ''

                    for field in fields:
                        fields_str += ', %s' % field

                    c.execute(
                            'select %s from servers where s_id = %s' \
                                    % (
                                        fields_str[2:],
                                        message.guild.id))

                    fetched = c.fetchone()

                    if not fetched:
                        await message.channel.send(
                                'Uh-oh - server not added to the list. This is because the bot was not running it was allowed it to join this server. Please kick the bot and readd it through the link provided by the _.links_ command.')
                        return

                    i = 0

                    message_body = ''

                    while i < len(fields):
                        if fields[i] == 'id' or fields[i].startswith('s_'):
                            pass

                        elif fields[i].startswith('c_'):
                            if fetched[i]:
                                message_body += '**%s**: <#%d>\n' \
                                        % (
                                                fields[i][2:],
                                                fetched[i])

                            else:
                                message_body += '**%s**: Disabled\n' \
                                        % fields[i][2:]

                        else:
                            message_body += '**%s**: _%s_\n' \
                                    % (
                                            fields[i],
                                            fetched[i])
                        i += 1

                    await message.channel.send(
                            embed=discord.Embed(
                                title='ALL PROPERTIES',
                                colour=discord.Colour.gold(),
                                description=message_body + \
                                        '\nRefer to _.admin_ to see how to change them.'))
                    return

                if value == '':
                    await message.channel.send(
                            'Missing value. Type _.admin_ to find out what the properties and its possible values are.')
                    return

                if command in ('welcome', 'farewell'):
                    c.execute(
                            'update servers set %s = %s where s_id = %s'.format(command),
                            (
                                value,
                                message.guild.id))

                    self.db.commit()

                    await message.channel.send(
                            'Message saved. Remember to enable it on the desired channel by writing _.enable greting._')
                    return

                elif command == 'max_deletions':
                    if re.match('^([0-9]{1,2}|100)$', value):
                        c.execute(
                                'update servers set max_deletions = %s where s_id = %s',
                                (int(value), message.guild.id))

                        self.db.commit()

                    else:
                        await message.channel.send(
                                'Invalid amount. The limit is currently 100.')
                        return

                elif command in (
                        'role_create',
                        'role_cleanup',
                        'someone',
                        'meme_filter'):
                    if re.match('^([Tt][Rr][u][e]|[Ff][Aa][Ll][Ss][Ee])$', value):
                        value = value.lower() != 'false'

                        c.execute('''
update servers set {} = %s where s_id = %s
                                '''.format(command),
                                (
                                    value,
                                    message.guild.id))

                        self.db.commit()

                        if command[0] == 'm' and not value:
                            # We are setting meme_filter to 0, so validate that the
                            # meme channel is set to NSFW
                            c.execute(
                                    'select c_meme from servers where s_id = %s',
                                    (message.guild.id,))

                            c_meme = c.fetchone()[0]

                            if c_meme:
                                if not message.guild.get_channel(c_meme).nsfw:
                                    await message.channel.send(
                                            'Setting saved; however, because <#%d> has not been marked as NSFW, the meme filter will still take effect until this changes.' \
                                                    % c_meme)
                                    return

                    else:
                        await message.channel.send(
                                'Value must be either _true_ or _false._')
                        return

                else:
                    await message.channel.send(
                            'Please type _.admin_ to see how to run this command.')
                    return

                await message.channel.send(
                        'OK')

            elif message.content == '.links':
                await message.channel.send(
                        embed=discord.Embed(
                            title='ALL LINKS',
                            colour=discord.Colour.gold(),
                            description='''
Invite the bot to your server of choice via this link:

https://discord.com/oauth2/authorize?client_id=700307494580256768&permissions=268561408&scope=bot

To report an issue or suggest a new feature for this bot, we encourage you to do it through this site:

https://github.com/stamby/easy-pete-bot/issues/new/choose

A server is also available for help and suggestions: https://discord.gg/shvcbR2
                            '''))

            if message.author.id == Credentials.OWNER_ID:
                if message.content.startswith('.update '):
                    c.execute(
                            'select s_id, c_updates from servers where c_updates is not null')

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

        elif message.content.startswith('@someone'):
            c = self.db.cursor()

            # Check whether it is enabled
            c.execute(
                    'select someone from servers where s_id = %s',
                    (message.guild.id,))

            if c.fetchone()[0] == 0:
                return

            while True:
                random_member = random.choice(
                        message.guild.members)

                if random_member.id != message.id \
                        or not random_member.bot:
                    break

            await message.channel.send(
                    '<@!%d> %s ***(%s)***' \
                            % (
                                random_member.id,
                                random.choice((
                                    '(⁄ ⁄•⁄ω⁄•⁄ ⁄)',
                                    '(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. o ･ ｡ﾟ',
                                    '¯(°_o)/¯',
                                    '¯\_(ツ)_/¯',
                                    '༼ つ ◕_◕ ༽つ',
                                    'ヽ༼ ಠ益ಠ ༽ﾉ',
                                    '（✿ ͡◕ ᴗ◕)つ━━✫・o。')),
                                random_member.name))

        elif message.content == '<@!%d>' % self.user.id:
            await message.channel.send(
                    random.choice((
                        '<@!%d>: What is your command?' % message.author.id,
                        '<@!%d>: Yes?' % message.author.id,
                        '<@!%d>: I\'m listening.' % message.author.id,
                        'Do you need anything, <@!%d>?' % message.author.id,
                        'How may I help you, <@!%d>?' % message.author.id,
                        'Ready when you are, <@!%d>.' % message.author.id)))
