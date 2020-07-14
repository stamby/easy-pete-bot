import discord

def run(message, client):
    c.execute(
            '''
select s_id, c_updates from servers where c_updates is not null
            ''')

    while True:
        s_id_and_c_updates = c.fetchone()

        if not s_id_and_c_updates:
            break

        channel = client.get_guild(
                s_id_and_c_updates[0]).get_channel(
                        s_id_and_c_updates[1])

        await channel.send(
                embed=discord.Embed(
                    title='ANNOUNCEMENT',
                    colour=discord.Colour.gold(),
                    description=message.content[8:]))
