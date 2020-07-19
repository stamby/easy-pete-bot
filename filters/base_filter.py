class BaseFilter:
    def __init__(self, db_field, db):
        c = db.cursor()

        c.execute(
                    '''
select {} from servers where s_id = %s
                    '''.format(db_field),
                    (message.guild.id,))

        value = c.fetchone()[0]

        self.warning = value == 1 or value == 2
        self.deleting = value == 2 or value == 3

