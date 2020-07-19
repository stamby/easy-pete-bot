async def run(member, db):
    c = db.cursor()

    c.execute(
            'select role_cleanup from servers where s_id = %s',
            (member.guild.id,))

    if c.fetchone()[0]:
        for role in member.roles:
            if len(role.members) == 0:
                await role.delete(
                        reason='Cleaning up unused role')

    c.close()

