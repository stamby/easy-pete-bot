import random
import re

from .base_filter import BaseFilter

regex = re.compile(
        'discord((app)?\.com/invite\/[^ ]|\.gg\/[^ ])')

async def run(message, db):
    filter_ = BaseFilter('filter_invite', message.guild.id, db)

    if filter_.warning:
        await message.channel.send(
                random.choice((
                    "Please don't advertise your server here, <@!%d>.",
                    'Server invites are discouraged, <@!%d>.')) \
                            % message.author.id)

    if filter_.deleting:
        await message.delete()

