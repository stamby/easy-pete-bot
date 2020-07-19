class BaseFilter:
    def __init__(self, db_field, s_id, db):
        c = db.cursor()

        c.execute(
                    '''
select %s from servers where s_id = %d
                    ''' % (
                        db_field,
                        s_id))

        value = c.fetchone()[0]

        self.warning = value == 1 or value == 2
        self.deleting = value == 2 or value == 3

