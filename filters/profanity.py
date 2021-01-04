import random
import re
from time import sleep

from .base_filter import BaseFilter

regex = re.compile(
        r'\b([Ss][Uu][Cc][CcKk][Ee][Rr]|([Ss][Uu][Cc][Kk].*[Dd]|d)[Iil][Cc][Kk]|[Dd][Iil][Cc][Kk][Hh][Ee][Aa][Dd]|[Ff][Uu][Cc][CcKk]|[Ff][Aa][Gg]{2}[Oo][Tt]|[Nn][Iil]+[Gg]{2,}([Aa]|[Ee][Rr])|[Rr][Ee][Tt][Aa][Rr][Dd]|[Iil][Dd][Iil][Oo][Tt]|[Ss][Tt][Uu][Pp][Iil][Dd]|([Aa][Rr][Ss][Ee]|[Aa][Ss]{2})([Hh][Oo][Ll][Ee]|[Hh][Aa][Tt]|[Cc][Hh][Ee]{2}[Kk])|[Cc][Oo][Cc][CcKk]([^Tt]|$)|[Dd][Aa][RrMm][Nn]|[Cc][Uu][Nn][Tt]|[Cc][Rr][Aa][Pp]|[Bb][Uu][Gg]{2}[Ee][Rr]|[Bb][Iil][Tt][Cc][Hh]|[Bb][Uu]+[LlI]{2,}[Ss]+[Hh]+[Iil][Tt]|[Pp][Rr][Iil][Cc][Kk]|[Pp][Uu][Nn]{1,2}[Aa][Nn][IilYy]|[Pp][Uu][Ss]{2}[Yy]|[Ss][Nn][Aa][Tt][Cc][Hh]|[Ss][Hh][Aa][Gg]|[Hh][Oo][Ee]|[Ww][Hh][Oo][Rr][Ee])')

async def run(message, db):
    filter_ = BaseFilter('filter_profanity', message.guild.id, db)

    if filter_.deleting:
        await message.delete()

    if filter_.warning:
        message_ = await message.channel.send(
                random.choice((
                    '''
<@!%d>, our server has been set up to discourage the use of swearing. Please be nice.
                    ''',
                    '''
<@!%d>: Please adhere to our server's Victorian values by avoiding undisguised, foul language.
                    ''',
                    '''
<@!%d>, we like all kinds of debauchery here but not swear words! Please avoid using them.
                    ''',
                    '''
Please make sure you don't use any swear words, <@!%d>.
                    ''',
                    '''
<@!%d>: There is one thing you might not know about swear words on this server: We don't use them.
                    ''')) \
                            % message.author.id)

        sleep(3)

        await message_.delete()

