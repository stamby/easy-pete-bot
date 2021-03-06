import discord
import random
import re

regex = re.compile(
        '.[Ss][Ee][Tt]( |$)')

async def run(escaped_prefix, message, db):
    c = db.cursor()

    # Check whether the user has the appropriate permissions
    if not message.channel.permissions_for(
            message.author).manage_guild:
        await message.channel.send(
                '''
The _%sset_ command may be run only by someone having the _Manage Server_ permission.
                ''' % escaped_prefix)
        return

    trailing_space, command, value = re.findall(
            '^....( *)((?:[^ ]+)?) *(.*)$',
            message.content)[0]

    if trailing_space == '':
        c.execute(
                '''
select c_greeting, c_iam, c_meme, c_song, c_updates,
welcome, farewell, max_deletions, role_create,
role_cleanup, someone, meme_filter,
filter_profanity, filter_mass_mention, filter_invite
from servers where s_id = %s
                ''',
                (message.guild.id,))

        c_greeting, c_iam, c_meme, c_song, c_updates, \
                welcome, farewell, max_deletions, role_create, \
                role_cleanup, someone, meme_filter, \
                filter_profanity, filter_mass_mention, filter_invite, \
                    = c.fetchone()

        # Just print everything
        message_body = '''
**CHANNELS**

**greeting**: %s
**iam**: %s
**meme**: %s
**song**: %s
**updates**: %s

Random example: _%s%s %s_

**PROPERTIES**

**welcome**: _%s_
**farewell**: _%s_
**max_deletions**: _%d_
**role_create**: _%s_
**role_cleanup**: _%s_
**someone**: _%s_
**meme_filter**: _%s_
**filter_profanity**: _%s_
**filter_mass_mention**: _%s_
**filter_invite**: _%s_
**prefix**: _%s_

Random example: _%sset %s_

Channels may be changed through _%senable_ and _%sdisable,_ while properties require the use of _%sset._ For more information, see _%sadmin._
            ''' % (
                    c_greeting and '<#%d>' % c_greeting \
                            or 'Disabled',
                    c_iam and '<#%d>' % c_iam \
                            or 'Disabled',
                    c_meme and '<#%d>' % c_meme \
                            or 'Disabled',
                    c_song and '<#%d>' % c_song \
                            or 'Disabled',
                    c_updates and '<#%d>' % c_updates \
                            or 'Disabled',
                    escaped_prefix, # This will be already `escaped'
                    random.choice((
                        'enable',
                        'disable'
                    )),
                    random.choice((
                        'greeting',
                        'iam',
                        'meme',
                        'song',
                        'updates'
                    )),
                    discord.utils.escape_markdown(welcome),
                    discord.utils.escape_markdown(farewell),
                    max_deletions,
                    (
                        'False (bot cannot create roles)',
                        'True (allowed to create roles)'
                    )[int(role_create)],
                    (
                        'False (turned off)',
                        'True (running)'
                    )[int(role_cleanup)],
                    (
                        'False (not allowed)',
                        'True (allowed)'
                    )[int(someone)],
                    (
                        'False (memes may be for mature audiences)',
                        'True (memes can be seen by all audiences)'
                    )[int(meme_filter)],
                    (
                        '0 (not moderated)',
                        '1 (warning, not deleting)',
                        '2 (warning and deleting)',
                        '3 (deleting without warning)'
                    )[filter_profanity],
                    (
                        '0 (not moderated)',
                        '1 (warning, not deleting)',
                        '2 (warning and deleting)',
                        '3 (deleting without warning)'
                    )[filter_mass_mention],
                    (
                        '0 (not moderated)',
                        '1 (warning, not deleting)',
                        '2 (warning and deleting)',
                        '3 (deleting without warning)'
                    )[filter_invite],
                    escaped_prefix,
                    escaped_prefix,
                    random.choice((
                        'welcome Someone has joined us! Hi, @@USER@@ (@@TAG@@)!',
                        'welcome Welcome, @@USER@@! (default)',
                        'welcome Welcome, @@USER@@! Feel free to introduce yourself.',
                        'welcome Welcome, @@USER@@!',
                        'farewell Finally, @@TAG@@ has left',
                        'farewell Goodbye, @@TAG@@!',
                        'farewell See you, @@TAG@@',
                        'farewell Unfortunately, @@TAG@@ has left.',
                        'farewell \*\*@@TAG@@\*\* has left the server. (default)',
                        'filter\_invite false',
                        'filter\_invite true',
                        'filter\_mass\_mention false',
                        'filter\_mass\_mention true',
                        'filter\_profanity false',
                        'filter\_profanity true',
                        'max\_deletions false',
                        'max\_deletions true',
                        'meme\_filter false',
                        'meme\_filter true',
                        'role\_cleanup false',
                        'role\_cleanup true',
                        'role\_create false',
                        'role\_create true',
                        'someone false',
                        'someone true',
                        'prefix .',
                        'prefix ,',
                        'prefix }',
                        'prefix >'
                    )),
                    escaped_prefix,
                    escaped_prefix,
                    escaped_prefix,
                    escaped_prefix
                )

        await message.channel.send(
                embed=discord.Embed(
                    title='CURRENT SETTINGS',
                    colour=discord.Colour.gold(),
                    description=message_body))
        return

    if value == '':
        await message.channel.send(
                '''
Missing value. Type _%sadmin_ to find out what the properties and its possible values are.
                ''' % escaped_prefix)
        return

    command = command.casefold()

    if command == 'prefix':
        if len(value) == 1:
            c.execute(
                    '''
update servers set prefix = %s where s_id = %s
                    ''',
                    (
                        value,
                        message.guild.id
                    ))

            db.commit()

            if value in ('@', '#'):
                await message.channel.send(
                        '''
Setting saved. Warning: You have set the prefix to _%s,_ which might interfere with the way Discord works in few cases. To avoid this, please consider choosing another prefix.
                        ''' % value)
                return

            elif re.match('[A-Za-z0-9]', value):
                await message.channel.send(
                        '''
Setting saved. Warning: You have set the prefix to _%s,_ which is alphanumeric. To avoid confusion, we strongly recommend using a symbol instead, like the default dot _(.)._ To achieve this, write _%sset prefix ._
                        ''' % (
                            value,
                            value
                        ))
                return

        else:
            await message.channel.send(
                    '''
The prefix must be only one character. It is a dot by default.
                    ''')
            return

    elif command in ('welcome', 'farewell'):
        c.execute(
                '''
update servers set {} = %s where s_id = %s
                '''.format(command),
                (
                    value,
                    message.guild.id
                ))

        db.commit()

        await message.channel.send(
                '''
Message saved. If you haven't, remember to enable it on the desired channel by writing _%senable greeting._
                ''' % escaped_prefix)
        return

    elif command == 'max_deletions':
        if re.match('^(0|[1-9][0-9]?|100)$', value):
            c.execute(
                    '''
update servers set max_deletions = %s where s_id = %s
                    ''',
                    (
                        int(value),
                        message.guild.id
                    ))

            db.commit()

        else:
            await message.channel.send(
                    'Invalid amount. The limit is currently 100.')
            return

    elif command in (
            'filter_profanity',
            'filter_mass_mention',
            'filter_invite'):
        if re.match('^[0-3]$', value):
            c.execute(
                    '''
update servers set %s = %d where s_id = %d
                    ''' % (
                        command,
                        int(value),
                        message.guild.id))

            db.commit()

        else:
            await message.channel.send(
                    'Value should be one of _0, 1, 2_ or _3._')
            return

    elif command in (
            'role_create',
            'role_cleanup',
            'someone',
            'meme_filter'):
        if re.match(
                '^([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])$',
                value):
            value = value.lower() == 'true'

            c.execute(
                    '''
update servers set %s = %s where s_id = %s
                    ''' % (
                        command,
                        value,
                        message.guild.id
                    ))

            db.commit()

            if command[0] == 'm' and not value:
                # We are setting meme_filter to 0, so validate that the
                # meme channel is set to NSFW
                c.execute(
                        '''
select c_meme from servers where s_id = %s
                        ''',
                        (message.guild.id,))

                c_meme = c.fetchone()[0]

                if c_meme:
                    if not message.guild.get_channel(c_meme).nsfw:
                        await message.channel.send(
                                '''
Setting saved; however, because <#%d> has not been marked as NSFW, the meme filter will still take effect until this changes. Keep in mind that, without filter, some memes may be offensive to users. Please make sure that they are of age and they will agree with these changes.
                                ''' \
                                        % c_meme)
                        return

                await message.channel.send(
                        '''
Meme filter has been turned off. Warning: Some memes may be offensive and even distasteful to some users. If you do not want this to be the case, run _%sset meme\_filter true._%s
                        ''' % (
                                c_meme and '' \
                                or ' To enable the command, run _%senable meme._' \
                                    % escaped_prefix,
                                escaped_prefix
                            ))
                return

        else:
            await message.channel.send(
                    'Value must be either _true_ or _false._')
            return

    else:
        await message.channel.send(
                'Please write _%sadmin_ to see how to run this command.' \
                        % escaped_prefix)
        return

    await message.channel.send(
            'OK')
