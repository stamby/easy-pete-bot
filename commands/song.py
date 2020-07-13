import discord
import os
import random
import re

async def run(message, db, credentials):
    c = db.cursor()

    # Check whether it is enabled for this channel
    c.execute(
            'select c_song from servers where s_id = %s',
            (message.guild.id,))

    c_song = c.fetchone()[0]

    if not c_song and message.channel.permissions_for(
            message.author).manage_channels:
        await message.channel.send(
                '''
Please enable this command by means of _.enable song._
                ''')
        return

    if message.channel.id != c_song:
        await message.channel.send(
                'Songs will be sent on <#%d>.' \
                        % c_song)
        return

    # Parse the message
    trailing_space, command, extra_chars = re.findall(
            '^\.....( *)((?:all$|submit +(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]+$|search .+|genre(?: .+|$))?)(.*)',
            message.content.lower())[0]

    if trailing_space == '' and command == '':
        # No command is being provided, therefore send a random song from the DB
        c.execute(
                'select url from songs order by random() limit 1')

        song_message = await message.channel.send(
                c.fetchone()[0])
        await song_message.add_reaction('👍')
        await song_message.add_reaction('👎')

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
                                credentials.BOT_NAME,
                                credentials.BOT_NAME.upper()
                            ))

            while True:
                line = c.fetchone()

                if not line:
                    break

                f.write(line[0])

            c.execute(
                    'select max(added_on) from songs')

            f.write(
                    c.fetchone()[0].strftime(
                        '</ul><p>Last song added on %A %-d %B %y, %-I:%M %p (UTC).</p></body></html>'))

        with open(file_, 'r') as f:
            await message.channel.send(
                    embed=discord.Embed(
                        title='ALL SONGS',
                        colour=discord.Colour.gold(),
                        description='''
The attached file contains all my songs.

You can add to these songs by running _.song submit (Youtube URL)_ and search them through _.song search (artist, title or both)._

This list changes often. It is up to date as of this very moment.
                        '''),
                    file=discord.File(
                        fp=f,
                        filename='%s_songs.html' \
                                % credentials.BOT_NAME.lower()))

        os.remove(file_)

        print(
                'Songs sent to "%s" (%d).' \
                        % (
                            message.guild,
                            message.guild.id
                        ))

    elif command.startswith('submit'):
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
                '''
insert into song_requests (solicitor, s_id, url) values (%s, %s, %s)
                ''',
                (
                    message.author.id,
                    message.guild.id,
                    url))

        db.commit()

        print(
                'Song \'%s\' has been requested for review.' % url)

        await message.channel.send(
                'Submitted for review.')

    elif command.startswith('search'):
        like = '%%%s%%' % re.sub(
                '[^A-Za-z0-9_-]+',
                '%',
                command[7:])

        c.execute(
                '''
select url from songs where artist || title ilike %s
or title || artist ilike %s
order by random() limit 1
                ''',
                (like, like))

        match = c.fetchone()

        if match:
            song_message = await message.channel.send(match[0])
            await song_message.add_reaction('👍')
            await song_message.add_reaction('👎')

        else:
            await message.channel.send(
                    '''
No matches. Submit a URL by typing _.song submit (Youtube URL)._
                    ''')

    elif command.startswith('genre'):
        requested_genre = command[6:]

        if requested_genre == '':
            c.execute(
                    'select distinct genre from songs order by 1')

            await message.channel.send(
                    'The available genres are _%s._' \
                            % ', '.join(
                                [
                                    genre[0]
                                    for genre in c.fetchall()
                                ]
                            ))
            return

        c.execute(
                '''
select url from songs where genre = %s
order by random() limit 1
                ''',
                (requested_genre,))

        match = c.fetchone()

        if match:
            song_message = await message.channel.send(match[0])
            await song_message.add_reaction('👍')
            await song_message.add_reaction('👎')

        else:
            await message.channel.send(
                    '''
No matches. Type _.song genre_ to see all available music genres.
                    ''')
            return

    else:
        await message.channel.send(
                '''
An invalid command has been supplied. Please type _.help_ to see valid options to the _.song_ command.
                ''')
