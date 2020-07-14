def get(s_id, db):
    c = db.cursor()

    c.execute(
            '''
select prefix from servers where s_id = %s
            ''',
            (s_id,))

    return c.fetchone()[0]
