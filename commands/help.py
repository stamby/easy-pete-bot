import discord
import re

regex = re.compile(
        '\.[Hh][Ee][Ll][Pp]( |$)')

async def run(message, db):
    c = db.cursor()

    c.execute(
            '''
select c_iam, c_meme, c_song, someone from servers where s_id = %s
            ''',
            (message.guild.id,))

    c_iam, c_meme, c_song, someone = c.fetchone()

    description = '''
**.about**: Show information on the bot and how to contact the developers, as well as an invite link.
%s%s%s%s

**.admin**: More commands for admins. It shows help on how to manage the bot's features.
%s
            ''' % \
            (
                    c_iam and '''
**.iam** (role name): Assign yourself a role. If the role doesn't exist, it may be created depending on settings.

**.iamnot** (role name): Remove a role from your user. If no users have the role anymore, the role may be removed depending on settings.
                    ''' or '',
                    c_meme and '''
**.meme**: Send a random meme, straight from our repositories. Submit a meme by writing _.meme submit._
                    ''' or '',
                    c_song and '''
**.song**: Send a good song for your happy ears.

Optionally:
**.song search** (artist and/or title)
**.song genre** (music genre)
**.song submit** (Youtube URL)
**.song all**
                    ''' or '',
                    someone and '''
**@someone**: Randomly mention someone on the server.
                    ''' or '',
                    (
                        not c_iam \
                        or not c_meme \
                        or not c_song \
                        or not someone
                    ) and '''
More commands can be enabled. Admins may add them by use of _.enable_ and _.set,_ described in _.admin._
                    ''' or ''
            )

    await message.channel.send(
            embed=discord.Embed(
                title='ALL COMMANDS',
                colour=discord.Colour.gold(),
                description=description))

