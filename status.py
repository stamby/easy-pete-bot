import discord

async def load(client):
    c = client.db.cursor()

    c.execute(
            'select status from bot')

    status = c.fetchone()

    if status:
        await client.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name=status[0]))

        print("Status loaded from database: '%s'." \
                % status[0])

    c.close()

async def change(message, client):
    c = client.db.cursor()

    status = message.content[8:]

    if status == '':
        status = None

    c.execute(
            'update bot set status = %s',
            (status,))

    client.db.commit()

    await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=status))

    if status:
        print(
                'Status set to \'%s\'.' % status)
    else:
        print(
                'Status cleared.')

