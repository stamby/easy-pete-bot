import random
import re

regex = re.compile(
        '[Ss][Uu][Cc][CcKk][Ee][Rr]|([Ss][Uu][Cc][Kk].*[Dd]|d)[Ii][Cc][Kk]|[Dd][Ii][Cc][Kk][Hh][Ee][Aa][Dd]|[Ff][Uu][Cc][CcKk]|[Ff][Aa][Gg]{2}[Oo][Tt]|[Nn][Ii][Gg]{2}([Aa]|[Ee][Rr])|[Rr][Ee][Tt][Aa][Rr][Dd]|[Ii][Dd][Ii][Oo][Tt]|[Ss][Tt][Uu][Pp][Ii][Dd]|(^|[^a-z])[Aa][Ss]{2}|(^|[^a-z])[Aa][Rr][Ss][Ee]|(^|[^a-z])[Aa][Nn][Uu][Ss]|(^|[^a-z])[Cc][Oo][Cc][CcKk]|[Dd][Aa][RrMm][Nn]|[Cc][Uu][Nn][Tt]|[Cc][Rr][Aa][Pp]|[Bb][Uu][Gg]{2}[Ee][Rr]|[Bb][Ii][Tt][Cc][Hh]|[Bb][Uu][Ll]{2}[Ss][Hh][Ii][Tt]|[Pp][Rr][Ii][Cc][Kk]|[Pp][Uu][Nn]{1,2}[Aa][Nn][IiYy]|[Pp][Uu][Ss]{2}[Yy]|[Ss][Nn][Aa][Tt][Cc][Hh]|[Ss][Hh][Aa][Gg]|[Hh][Oo][Ee]|[Ww][Hh][Oo][Rr][Ee]')

def run(message, db):
    c = db.cursor()

    c.execute(
                '''
select filter_profanity, filter_action from servers where s_id = %s
                ''',
                (message.guild.id,))

    filter_profanity, filter_action = c.fetchone()

    if not filter_profanity or not filter_action:
        return

    warning = filter_action == 1 or filter_action == 2
    deleting = filter_action == 2 or filter_action == 3

    if warning:
        await message.channel.send(
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

    if deleting:
        await message.delete()

