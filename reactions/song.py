def add(message, payload, db):
    c = db.cursor()

    if payload.emoji.name == '👍':
        c.execute(
                '''
update songs set yes = yes + 1 where url = %s
                ''',
                (message.content,))

    elif payload.emoji.name == '👎':
        c.execute(
                '''
update songs set no = no + 1 where url = %s
                ''',
                (message.content,))

    else:
        return

    db.commit()

def remove(message, payload, db):
    c = db.cursor()

    if payload.emoji.name == '👍':
        c.execute(
                '''
update songs set yes = yes - 1 where url = %s
                ''',
                (message.content,))
        
    elif payload.emoji.name == '👎':
        c.execute(
                '''
update songs set no = no - 1 where url = %s
                ''',
                (message.content,))

    else:
        return

    db.commit()
