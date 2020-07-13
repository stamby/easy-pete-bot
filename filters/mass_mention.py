import random
import re

regex = re.compile(
        '(<@![0-9]+>.*?){4,}')

async def run(message, db):
    c = db.cursor()

    c.execute(
            '''
select filter_mass_mention, filter_action from servers where s_id = %s
            ''',
            (message.guild.id,))

    filter_mass_mention, filter_action = c.fetchone()

    if not filter_mass_mention or not filter_action:
        return

    warning = filter_action == 1 or filter_action == 2
    deleting = filter_action == 2 or filter_action == 3

    if warning:
        await message.channel.send(
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

    if deleting:
        await message.delete()
