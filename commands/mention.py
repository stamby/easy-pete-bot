import random

async def run(escaped_prefix, message):
    await message.channel.send(
            random.choice((
                '<@!%d>: What is your command? Don\'t they begin with _%s?_',
                '<@!%d>: Yes? Do you need help? _%sHelp_ might be what you\'re looking for.',
                '<@!%d>: I\'m listening. Type _%shelp_ to get started.',
                'Do you need anything, <@!%d>? _%s_ is the current prefix.',
                'How may I help you, <@!%d>? Maybe check _%shelp?_',
                'Ready when you are, <@!%d>. Just type _%shelp._')) \
                        % (message.author.id, escaped_prefix))

