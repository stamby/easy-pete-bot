import random
import re
from time import sleep

from .base_filter import BaseFilter

regex = re.compile(
        '(<@![0-9]+>.*?){4,}')

async def run(message, db):
    filter_ = BaseFilter('filter_mass_mention', message.guild.id, db)

    if filter_.deleting:
        await message.delete()

    if filter_.warning:
        message_ = await message.channel.send(
                random.choice((
                    '''
<@!%d>: Up to three mentions may be sent per message.
                    ''',
                    '''
<@!%d>: Please don't mention more than three times at one message.
                    ''',
                    '''
<@!%d>, there should be no need to mention that many times in one message. If it is important, please message each person privately instead.
                    ''',
                    '''
Mass mentions are discouraged, <@!%d>.
                    ''',
                    '''
Please don't send so many mentions, <@!%d>.
                    ''')) \
                            % message.author.id)

        sleep(3)

        await message_.delete()
