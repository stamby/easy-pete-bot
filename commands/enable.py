import discord
import re

regex = re.compile(
        '.[Ee][Nn][Aa][Bb][Ll][Ee]( |$)')

async def run(escaped_prefix, message, db):
    # Check whether the user has the appropriate permissions
    if not message.channel.permissions_for(
            message.author).manage_channels:
        await message.channel.send(
                '''
The _%senable_ command has to come from someone having the _Manage Channels_ permission for this channel.
                ''' % escaped_prefix)
        return

    commands = re.findall(
            '[^ ]+', message.content[8:].lower())

    if len(commands) == 0:
        await message.channel.send(
                'Which command would you like to enable?')
        return

    c = db.cursor()

    c.execute(
            '''
select column_name from information_schema.columns where table_name = 'servers'
and column_name like 'c\_%'
            ''')

    c_fields = [field[0][2:] for field in c.fetchall()]

    for command in commands:
        if command not in c_fields:
            await message.channel.send(
                    'The command _%s_ is not valid. Please type _%sadmin_ to see which commands may be enabled.' \
                            % (
                                discord.utils.escape_markdown(
                                    command),
                                escaped_prefix
                            ))
            return

    for command in commands:
        c.execute(
                '''
update servers set c_%s = %d where s_id = %d
                ''' % (
                    command,
                    message.channel.id,
                    message.guild.id
                ))

    db.commit()

    await message.channel.send(
            '''
The following commands have been reserved for this channel: _%s._
            ''' \
                    % ', '.join(commands))

