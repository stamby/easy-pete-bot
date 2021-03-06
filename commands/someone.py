import discord
import random
import re

regex = re.compile(
        '(@|[Aa][Tt] *)[Ss][Oo][Mm][Ee][Oo][Nn][Ee]')

async def run(message, db):
    c = db.cursor()

    # Check whether it is enabled
    c.execute(
            'select someone from servers where s_id = %s',
            (message.guild.id,))

    if c.fetchone()[0] == 0:
        return

    while True:
        random_member = random.choice(
                message.guild.members)

        if not random_member.bot and (
                random_member.id != message.author.id \
                        or len(message.guild.members) < 10
                ):
            break

    await message.channel.send(
            '<@!%d> %s ***(%s)***' \
                    % (
                        random_member.id,
                        random.choice((
                            '(⁄ ⁄•⁄ω⁄•⁄ ⁄)',
                            '(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. o ･ ｡ﾟ',
                            '¯(°_o)/¯',
                            '¯\_(ツ)_/¯',
                            '༼ つ ◕_◕ ༽つ',
                            'ヽ༼ ಠ益ಠ ༽ﾉ',
                            '（✿ ͡◕ ᴗ◕)つ━━✫・o。')),
                        random_member.name
                    ))

