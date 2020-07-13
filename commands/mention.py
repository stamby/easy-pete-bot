import random

async def run(message):
    await message.channel.send(
            random.choice((
                '<@!%d>: What is your command?',
                '<@!%d>: Yes?',
                '<@!%d>: I\'m listening.',
                'Do you need anything, <@!%d>?',
                'How may I help you, <@!%d>?',
                'Ready when you are, <@!%d>.')) \
                        % message.author.id)

