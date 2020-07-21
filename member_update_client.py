import greetings.welcome
import greetings.farewell

import misc.role_cleanup

from base_client import BaseClient

class MemberUpdateClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self, 'Member Update')

    async def on_ready(self):
        print('Member Update has started.')

    async def on_member_join(self, member):
        await greetings.welcome.run(member)

    async def on_member_remove(self, member):
        await greetings.farewell.run(member)

        await misc.role_cleanup.run(member, self.db)

    async def on_member_update(self, before, after):
        if len(before.roles) > len(after.roles):
            await misc.role_cleanup.run(before, self.db)

