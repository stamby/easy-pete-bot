import discord
import re

regex = re.compile(
        '.[Aa][Bb][Oo][Uu][Tt]( |$)')

async def run(message, credentials):
    await message.channel.send(
            embed=discord.Embed(
                title='ABOUT %s' % credentials.BOT_NAME.upper(),
                colour=discord.Colour.gold(),
                description='''
Website: https://bot.molteni.im

Invite: https://discord.com/oauth2/authorize?client_id=700307494580256768&permissions=268561408&scope=bot

Source code: https://github.com/stamby/easy-pete-bot

Report an issue or suggest a new feature: https://github.com/stamby/easy-pete-bot/issues/new/choose

A server is also available for help and suggestions: https://discord.gg/shvcbR2
                '''))
