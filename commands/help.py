import discord
import re

regex = re.compile(
        '.[Hh][Ee][Ll][Pp]( |$)')

async def run(escaped_prefix, message, db):
    c = db.cursor()

    c.execute(
            '''
select c_iam, c_meme, c_song, someone from servers where s_id = %s
            ''',
            (message.guild.id,))

    c_iam, c_meme, c_song, someone = c.fetchone()

    description = '''
**%sabout**: Show information on the bot and how to contact the developers, as well as an invite link.
%s%s%s%s

**%sadmin**: More commands for admins. It shows help on how to manage the bot's features.
%s
            ''' % \
            (
                    escaped_prefix,
                    c_iam and '''
**%siam** (role name): Assign yourself a role. If the role doesn't exist, it may be created depending on settings.

**%siamnot** (role name): Remove a role from your user. If no users have the role anymore, the role may be removed depending on settings.
                    ''' % (
                        escaped_prefix,
                        escaped_prefix
                    ) or '',
                    c_meme and '''
**%smeme**: Send a random meme, straight from our repositories. Submit a meme by writing _%smeme submit._
                    ''' % (
                        escaped_prefix,
                        escaped_prefix
                    ) or '',
                    c_song and '''
**%ssong**: Send a good song for your happy ears.

Optionally:
**%ssong search** (artist and/or title)
**%ssong genre** (music genre)
**%ssong submit** (Youtube URL)
**%ssong all**
                    ''' % (
                        escaped_prefix,
                        escaped_prefix,
                        escaped_prefix,
                        escaped_prefix,
                        escaped_prefix
                    ) or '',
                    someone and '''
**@someone**: Randomly mention someone on the server.
                    ''' or '',
                    escaped_prefix,
                    (
                        not c_iam \
                        or not c_meme \
                        or not c_song \
                        or not someone
                    ) and '''
More commands can be enabled. Admins may add them by use of _%senable_ and _%sset,_ described in _%sadmin._
                    ''' % (
                        escaped_prefix,
                        escaped_prefix,
                        escaped_prefix
                    ) or ''
            )

    await message.channel.send(
            embed=discord.Embed(
                title='ALL COMMANDS',
                colour=discord.Colour.gold(),
                description=description))

