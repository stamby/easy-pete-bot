#!/bin/sh

### Easy Pete Bot: back up & purge

DATE=`date +%F-%H`

BACKUP_DIR=/srv/easy-pete-backup/backup
BACKUP_FILE=$BACKUP_DIR/${DATE}-easy-pete.bak

BACKUP_LOG_DIR=/srv/easy-pete-backup/log
BACKUP_LOG=$BACKUP_LOG_DIR/${DATE}-easy-pete.out.log
BACKUP_ERR_LOG=$BACKUP_LOG_DIR/${DATE}-easy-pete.err.log

exec 2> $BACKUP_ERR_LOG > $BACKUP_LOG

# $1 = Number of files, $2 = Oldest file without directory name 
purge() {
    while [ $1 -gt 5 ]; do
        # Remove backup
        rm -v "$BACKUP_DIR/$2"

        # Also remove its log file
        rm -v "$BACKUP_LOG_DIR/`printf '%s' $2 | sed 's/\.bak$//'`"*
    done
}

back_up() {
    pg_dumpall > $BACKUP_FILE
}

purge `ls -t $BACKUP_DIR | sed -n '${=;p}'`
back_up

