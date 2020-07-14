import discord
import re

regex = re.compile(
        '\.[Dd][Ii][Ss][Aa][Bb][Ll][Ee]( |$)')

def run(message, db):
    c = db.cursor()

    # Check whether the user has the appropriate permissions
    if not message.channel.permissions_for(
            message.author).manage_channels:
        await message.channel.send(
                '''
The _.disable_ command has to come from someone having the _Manage Channels_ permission for this channel.
                ''')
        return

    commands = re.findall(
            '[^ ]+', message.content[9:].lower())

    if len(commands) == 0:
        await message.channel.send(
                'Which command would you like to disable?')
        return

    c.execute(
            '''
select column_name from information_schema.columns where table_name = 'servers'
and column_name like 'c\_%'
            ''')

    c_fields = [field[0][2:] for field in c.fetchall()]

    for command in commands:
        if command not in c_fields:
            await message.channel.send(
                    '''
_%s_ is not valid. Please type _.admin_ to see which commands may be disabled.
                    ''' \
                            % discord.utils.escape_markdown(
                                command))
            return

    for command in commands:
        c.execute(
                '''
update servers set c_{} = null where s_id = %s
                '''.format(command),
                (message.guild.id,))

    db.commit()

    await message.channel.send(
            'The following commands have been disabled: _%s._' \
                    % ', '.join(commands))
