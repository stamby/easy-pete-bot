import random
import re

regex = re.compile(
        'discord((app)?\.com/invite\/[^ ]|\.gg\/[^ ])')

def run(message, db):
    c = db.cursor()

    c.execute(
            '''
select filter_invite, filter_action from servers where s_id = %s
            ''',
            (message.guild.id,))

    filter_invite, filter_action = c.fetchone()

    if not filter_invite or not filter_action:
        return

    warning = filter_action == 1 or filter_action == 2
    deleting = filter_action == 2 or filter_action == 3

    if warning:
        await message.channel.send(
                random.choice((
                    "Please don't advertise your server here, <@!%d>.",
                    'Server invites are discouraged, <@!%d>.')) \
                            % message.author.id)

    if deleting:
        await message.delete()

