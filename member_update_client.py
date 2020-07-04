from base_client import BaseClient

class MemberUpdateClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self, 'Member Update')

    async def on_ready(self):
        print('Member Update has started.')

    async def on_member_update(self, before, after):
        if len(before.roles) == len(after.roles):
            return

        c = self.db.cursor()

        c.execute(
                'select role_cleanup from servers where s_id = %s',
                (before.guild.id,))

        if c.fetchone()[0]:
            for role in before.roles:
                if len(role.members) == 0:
                    await role.delete(
                            reason='Cleaning up unused role')

        c.close()

    async def on_member_remove(self, member):
        c = self.db.cursor()

        c.execute(
                'select role_cleanup from servers where s_id = %s',
                (member.guild.id,))

        if c.fetchone()[0]:
            for role in member.roles:
                if len(role.members) == 0:
                    await role.delete(
                            reason='Cleaning up unused role')

        c.close()

