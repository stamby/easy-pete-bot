import discord
import random
import re

async def run(message, db, id_, credentials):
    c = db.cursor()

    # Parse message
    command, trailing_space, requested_role_name = re.findall(
            '^\.[Ii][Aa][Mm]((?:[Nn][Oo][Tt])?)( *)(.*)',
            message.content)[0]

    # Check whether it is enabled for this channel
    c.execute(
            '''
select c_iam, role_create from servers where s_id = %s
            ''',
            (message.guild.id,))

    c_iam, role_create = c.fetchone()

    if not c_iam and message.channel.permissions_for(
            message.author).manage_channels:
        await message.channel.send(
                '''
The command _.iam%s_ is not available. An admin may enable it by entering _.enable iam._
                ''' \
                        % command.lower())
        return

    if message.channel.id != c_iam:
        await message.channel.send(
                'This command is to be run on <#%d>.' \
                        % c_iam)
        return

    # Get the role that gives us the 'manage roles' permission
    own_role = None

    roles = message.guild.get_member(id_).roles

    i = len(roles)

    while i > 0:
        i -= 1

        if roles[i].permissions.manage_roles:
            own_role = roles[i]
            break

        if i == 0:
            break

    if not own_role:
        await message.channel.send(
                '''
Insufficient permissions. Namely, this command requires me to have _Manage Roles_ permission.
                ''')
        return

    if requested_role_name == '':
        await message.channel.send(
                'Please write _.iam%s_ followed by the role name.' \
                        % command.lower())
        return

    requested_role_name_lower = requested_role_name.lower()

    # Check whether the requested role exists
    existing_role = discord.utils.find(
            lambda r: r.name.lower() == requested_role_name_lower,
            message.guild.roles)

    # Remember whether we had 'not' in the command
    if command != '':
        if not existing_role:
            await message.channel.send(
                    '''
The role _%s_ does not exist. Maybe check your spelling?
                    ''' \
                            % discord.utils.escape_markdown(
                                requested_role_name))
            return

        if existing_role not in message.author.roles:
            await message.channel.send(
                    'The role _%s_ has not been assigned to you.' \
                            % discord.utils.escape_markdown(
                                existing_role.name))
            return

        elif existing_role > own_role:
            await message.channel.send(
                    '''
The role _%s_ is too high on the list for me to remove it. I would need mine to be higher than the role that is to be removed.
                    ''' \
                            % discord.utils.escape_markdown(
                                existing_role.name))
            return

        await message.author.remove_roles(
                existing_role,
                reason='Self-removed')

        await message.channel.send(
                '_%s_ removed.' \
                        % discord.utils.escape_markdown(
                            existing_role.name))

    else:
        # We are adding him the role
        # If the role doesn't exist
        if not existing_role:
            # Check whether we are allowed to create it
            if role_create == 0:
                await message.channel.send(
                        '''
The role _%s_ doesn't exist and cannot be created due to bot settings for this server.
                        ''' \
                                % discord.utils.escape_markdown(
                                    requested_role_name))
                return

            # Create the role
            existing_role = await message.guild.create_role(
                    name=requested_role_name,
                    reason='Created by %s on %s\'s request' \
                            % (
                                credentials.BOT_NAME,
                                message.author),
                    colour=discord.Colour.from_rgb(
                        random.randrange(255),
                        random.randrange(255),
                        random.randrange(255)),
                    hoist=True)

        elif existing_role in message.author.roles:
            await message.channel.send(
                    'The role _%s_ has already been assigned to you.' \
                            % discord.utils.escape_markdown(
                                existing_role.name))
            return

        elif existing_role > own_role:
            # If the role can't be changed due to its position in the hierarchy
            await message.channel.send(
                    'The role _%s_ is higher on the list than the one that allows me to manage other roles. I would need mine to be higher so I can add you the one you requested. Please ask an admin for assistance.' \
                            % discord.utils.escape_markdown(
                                existing_role.name))
            return

        elif existing_role.permissions.value != 0:
            await message.channel.send(
                    '''
_%s_ is an already-existing role with additional permissions. Please ask an admin to remove all permissions from the role before you may add it.
                    ''' \
                            % discord.utils.escape_markdown(
                                existing_role.name))
            return

        await message.author.add_roles(
                existing_role,
                reason='Self-assigned',
                atomic=True)

        await message.channel.send(
                '_%s_ assigned.' \
                        % discord.utils.escape_markdown(
                            existing_role.name))
