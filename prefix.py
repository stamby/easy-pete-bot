class Prefix:
    def __init__(self, db):
        c = db.cursor()

        c.execute(
                '''
select s_id, prefix from servers
                ''')

        self.from_s_id = {}

        # Load EVERY prefix on memory (this might be a bad idea in the future)
        while True:
            s_id_and_prefix = c.fetchone()

            if not s_id_and_prefix:
                break

            self.from_s_id[s_id_and_prefix[0]] = s_id_and_prefix[1]
