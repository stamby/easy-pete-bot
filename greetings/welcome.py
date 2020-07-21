import re

async def run(member):
    c = self.db.cursor()

    c.execute(
            '''
select c_greeting, welcome from servers where s_id = %s
            ''',
            (member.guild.id,))

    c_greeting, welcome = c.fetchone()

    if c_greeting:
        await member.guild.get_channel(c_greeting).send(
                re.sub(
                    '@@[Uu][Ss][Ee][Rr]@@',
                    '<@!%d>' % member.id,
                    welcome))

