#!/usr/bin/env bash

#############
# Variables #
#############

FOLDER_TO_BACKUP="$HOME/Desktop"

BACKUP_FOLDER="$HOME/.icon-location"
BACKUP_FILE_NAME="backup.json"
BACKUP_LOG_NAME="std-backup.log"
RESTORE_LOG_NAME="std-restore.log"

BACKUP_FULL_FILE_NAME="$BACKUP_FOLDER/$BACKUP_FILE_NAME"
BACKUP_FULL_LOG_NAME="$BACKUP_FOLDER/$BACKUP_LOG_NAME"
RESTORE_FULL_LOG_NAME="$BACKUP_FOLDER/$RESTORE_LOG_NAME"

BINARY_PATH="./manage.py"

LOG_FILE_MAX_CYCLE=20
LOG_MAX_CYCLE=5

#############

# needed for realtime stdout flush when piping python to tee
export PYTHONUNBUFFERED=1

#############

create_folder() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
    fi
}

save_previous() {
    savelog -C -q -c "$2" -n "$1"
}

backup() {

    # create the files folder if not present
    create_folder "$BACKUP_FOLDER"

    # rotate files
    save_previous "$BACKUP_FULL_FILE_NAME" "$LOG_FILE_MAX_CYCLE"
    save_previous "$BACKUP_FULL_LOG_NAME" "$LOG_MAX_CYCLE"

    "$BINARY_PATH" --backup "$FOLDER_TO_BACKUP" "$BACKUP_FULL_FILE_NAME" 2>&1 | tee "$BACKUP_FULL_LOG_NAME"

}

restore() {

    # create the log folder
    create_folder "$BACKUP_FOLDER"

    # rotate log
    save_previous "$RESTORE_LOG_NAME" "$LOG_MAX_CYCLE"

    # restore the icons
    "$BINARY_PATH" --restore "$BACKUP_FULL_FILE_NAME" 2>&1 | tee "$RESTORE_FULL_LOG_NAME"

}

#############

case "$1" in
    backup)
        backup
        ;;
    restore)
        restore
        ;;
    *)
       echo "Usage: $0 {backup | restore}"
esac

exit 0
