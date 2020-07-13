import re

async def run(message, db):
    c = db.cursor()

    # Parse the message
    trailing_space, user_str, requested_amount_str, extra_chars = re.findall(
            '^\......( *)((?:<@![0-9]+>)?) *((?:[0-9]+$)?)(.*)',
            message.content)[0]

    c.execute(
            'select max_deletions from servers where s_id = %s',
            (message.guild.id,))

    max_deletions = c.fetchone()[0]

    # Check whether the user has the appropriate permissions
    if not message.channel.permissions_for(
            message.author).manage_messages:
        await message.channel.send(
                '''
The _.prune_ command has to come from someone having the _Manage Messages_ permission for this channel.
                ''')
        return

    if max_deletions == 0:
        await message.channel.send(
                '''
The _.prune_ command has been disabled. An admin may type _.set max\_deletions (number)_ to change this.
                ''')
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
                    '''
For security reasons, only up to %d messages may be deleted. Type _.set max\_deletions (number)_ to change this.
                    ''' \
                            % max_deletions)

    else:
        await message.channel.send(
                'Invalid syntax for the _.prune_ command.')
