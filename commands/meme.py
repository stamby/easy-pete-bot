import discord
import os
import random
import re

regex = re.compile(
        '\.[Mm][Ee][Mm][Ee]( |$)')

async def run(message, db, credentials):
    c = db.cursor()

    # Check whether it is enabled for this channel
    c.execute(
            '''
    select c_meme, meme_filter from servers where s_id = %s
            ''',
            (message.guild.id,))

    c_meme, meme_filter = c.fetchone()

    if not c_meme and message.channel.permissions_for(
            message.author).manage_channels:
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
            '^\.....( *)((?:[Ss][Uu][Bb][Mm][Ii][Tt]$)?)(.*)',
            message.content)[0]

    if extra_chars != '':
        await message.channel.send(
                '''
    The only valid option to the _.meme_ command is the word _submit._
                ''')
        return

    if command != '':
        if len(message.attachments) == 0:
            await message.channel.send(
                    '''
    A submission requires an attachment. Please try again.
                    ''')
            return

        if len(message.attachments) != 1:
            await message.channel.send(
                    'Only one attachment allowed per submission.')
            return

        if not message.attachments[0].height:
            await message.channel.send(
                    '''
    A valid attachment must be either an image or video.
                    ''')
            return

        if message.attachments[0].size > 8388608:
            await message.channel.send(
                    '''
    The size of the attachment needs not to exceed 8 MB.
                    ''')
            return

        with open(
                os.path.join(
                    credentials.MEME_SUBMISSIONS,
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
            meme_filter = True

        if meme_filter:
            dir_ = os.path.join(
                    credentials.MEME_DIR_ALL_AUDIENCES,
                    random.choice(
                        os.listdir(
                            credentials.MEME_DIR_ALL_AUDIENCES)))

        else:
            dir_ = random.choice((
                    credentials.MEME_DIR_ALL_AUDIENCES,
                    credentials.MEME_DIR_OVER_EIGHTEEN))

            dir_ = os.path.join(
                    dir_,
                    random.choice(
                        os.listdir(dir_)))

        file_ = random.choice(
                os.listdir(dir_))

        with open(
                os.path.join(dir_, file_),
                'rb') as f:
            await message.channel.send(
                    file=discord.File(
                        fp=f,
                        filename=file_))

