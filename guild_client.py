from base_client import BaseClient

class GuildClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self, 'Guild Client')

    async def on_ready(self):
        print("'%s' has connected to Discord!" \
                % self.name)

    async def on_member_join(self, member):
        c = self.db.cursor()

        c.execute(
                'select c_greeting, welcome from servers where s_id = %s',
                (member.guild.id,))

        c_greeting, welcome = c.fetchone()

        if c_greeting:
            await member.guild.get_channel(c_greeting).send(
                    re.sub(
                        '@@[Uu][Ss][Ee][Rr]@@',
                        '<@!%d>' % member.id,
                        welcome))

    async def on_member_remove(self, member):
        c = self.db.cursor()

        c.execute(
                'select c_greeting, farewell from servers where s_id = %s',
                (member.guild.id,))

        c_greeting, farewell = c.fetchone()

        if c_greeting:
            await member.guild.get_channel(c_greeting).send(
                    re.sub(
                        '@@[Uu][Ss][Ee][Rr]@@',
                        '<@!%d>' % member.id,
                        farewell))

    async def on_guild_join(self, guild):
        c = self.db.cursor()

        c.execute(
                'insert into servers (s_id, s_owner) values (%s, %s)',
                (guild.id, guild.owner.id))

        self.db.commit()

        print(
                'Joined \'%s\' (%d): %d members, %d channels.' \
                        % (
                            guild,
                            guild.id,
                            len(guild.members),
                            len(guild.channels)))

