import discord
import re

async def run(message, db):
    c = db.cursor()

    # Check whether the user has the appropriate permissions
    if not message.channel.permissions_for(
            message.author).manage_guild:
        await message.channel.send(
                '''
The _.set_ command may be run only by someone having the _Manage Server_ permission.
                ''')
        return

    trailing_space, command, value = re.findall(
            '^\....( *)((?:[^ ]+)?) *(.*)$',
            message.content.lower())[0]

    if trailing_space == '':
        c.execute(
                '''
select c_greeting, c_iam, c_meme, c_song, c_updates,
welcome, farewell, max_deletions, role_create,
role_cleanup, someone, meme_filter, filter_action,
filter_profanity, filter_mass_mention, filter_invite
from servers where s_id = %s
                ''',
                (message.guild.id,))

        c_greeting, c_iam, c_meme, c_song, c_updates, \
                welcome, farewell, max_deletions, role_create, \
                role_cleanup, someone, meme_filter, \
                filter_action, filter_profanity, \
                filter_mass_mention, filter_invite \
                    = c.fetchone()

        # Just print everything
        message_body = '''
**CHANNELS**

**greeting**: %s
**iam**: %s
**meme**: %s
**song**: %s
**updates**: %s

Syntax: _.enable greeting_ (and/or _iam, meme,_ etc.)

**PROPERTIES**

**welcome**: _%s_
**farewell**: _%s_
**max_deletions**: _%d_
**role_create**: _%s_
**role_cleanup**: _%s_
**someone**: _%s_
**meme_filter**: _%s_
**filter_action**: _%s_
**filter_profanity**: _%s_
**filter_mass_mention**: _%s_
**filter_invite**: _%s_

Syntax: _.set someone false_ (or any other property for that matter)

Channels may be changed through _.enable_ and _.disable,_ while properties require the use of _.set._ For more information, see _.admin._
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
                    welcome,
                    farewell,
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
                        '0 (off)',
                        '1 (warning, not deleting)',
                        '2 (warning and deleting)',
                        '3 (deleting without warning)'
                    )[filter_action],
                    (
                        'False (not moderated)',
                        'True (swear words reached by filter)'
                    )[int(filter_profanity)],
                    (
                        'False (not moderated)',
                        'True (mass mentioning reached by filter)'
                    )[int(filter_mass_mention)],
                    (
                        'False (not moderated)',
                        'True (Discord invites reached by filter)'
                    )[int(filter_invite)]
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
Missing value. Type _.admin_ to find out what the properties and its possible values are.
                ''')
        return

    if command in ('welcome', 'farewell'):
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
Message saved. If you haven't, remember to enable it on the desired channel by writing _.enable greeting._
                ''')
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

    elif command == 'filter_action':
        if re.match('^[0-3]$', value):
            c.execute(
                    '''
update servers set filter_action = %s where s_id = %s
                    ''',
                    (int(value), message.guild.id))

            db.commit()

            if value != '0':
                c.execute(
                        '''
select filter_profanity, filter_mass_mention, filter_invite
from servers where s_id = %s
                        ''',
                        (message.guild.id,))

                filter_profanity, filter_mass_mention, filter_invite = \
                        c.fetchone()

                if not filter_profanity \
                        and not filter_mass_mention \
                        and not filter_invite:
                    await message.channel.send(
                            '''
Settings saved. Remember to enable one of the available filters by running _.set,_ followed by _filter\_profanity, filter\_mass\_mention_ or _filter\_invite,_ followed by _true_ or _false._
                            ''')
                    return

        else:
            await message.channel.send(
                    'Value should be one of _0, 1, 2_ or _3._')
            return

    elif command in (
            'role_create',
            'role_cleanup',
            'someone',
            'meme_filter',
            'filter_profanity',
            'filter_mass_mention',
            'filter_invite'):
        if re.match('^(true|false)$', value):
            value = value != 'false'

            c.execute(
                    '''
update servers set {} = %s where s_id = %s
                    '''.format(command),
                    (
                        value,
                        message.guild.id
                    ))

            db.commit()

            if command[0] == 'f' and value:
                c.execute(
                        '''
select filter_action from servers where s_id = %s
                        ''',
                        (message.guild.id,))

                if not c.fetchone()[0]:
                    await message.channel.send(
                            '''
Setting saved. Please make sure to also run _.set filter\_action_ followed by _1_ to send warnings to those whose messages are being filtered, _2_ to warn and also delete their messages and _3_ to delete without warning. The current setting is _0,_ which does nothing.
                            ''')
                    return

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
Meme filter has been turned off. Warning: Some memes may be offensive and even distasteful to some users. If you do not want this to be the case, run _.set meme\_filter true._%s
                        ''' % (
                                not c_meme and \
                                    ' To enable the command, run _.enable meme._'v\
                                or ''
                            ))
                return

        else:
            await message.channel.send(
                    'Value must be either _true_ or _false._')
            return

    else:
        await message.channel.send(
                'Please write _.admin_ to see how to run this command.')
        return

    await message.channel.send(
            'OK')
