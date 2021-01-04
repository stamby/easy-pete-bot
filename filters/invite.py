import random
import re
from time import sleep

from .base_filter import BaseFilter

regex = re.compile(
        'discord((app)?\.com/invite\/[^ ]|\.gg\/[^ ])')

async def run(message, db):
    filter_ = BaseFilter('filter_invite', message.guild.id, db)

    if filter_.deleting:
        await message.delete()

    if filter_.warning:
        message_ = await message.channel.send(
                random.choice((
                    "Please don't advertise your server here, <@!%d>.",
                    'Server invites are discouraged, <@!%d>.')) \
                            % message.author.id)

        sleep(3)

        await message_.delete()
