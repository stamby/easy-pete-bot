#!/bin/sh

### Easy Pete Bot: back up & purge

BACKUP_DIR=/srv/easy-pete-backup/backup
BACKUP_FILE=$BACKUP_DIR/`date +%F`-easy-pete.bak

BACKUP_LOG_DIR=/srv/easy-pete-backup/log
BACKUP_LOG=$BACKUP_LOG_DIR/`date +%F`-easy-pete.log

exec 2>&1 > $BACKUP_LOG

back_up() {
    pg_dumpall > $BACKUP_FILE
}

# $1 = Number of files, $2 = Oldest file without directory name 
purge() {
    if [ $1 -gt 5 ]; then
        # Remove backup
        rm -v $BACKUP_DIR/$2

        # Also remove its log file
        rm -v $BACKUP_LOG_DIR/`printf '%s' $2 | sed 's/\.bak$/.log/'`
    fi

}

back_up
purge `ls -t $BACKUP_DIR | sed -n '${=;p}'`

