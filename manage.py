#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from utils import file as local_file
from utils import error as local_error
from utils.icon import Icons


def main():

    argument_parser = argparse.ArgumentParser(description="Manages the position of icons (backup and restoration) in folders such as $HOME/Desktop")

    # add the needed arguments
    argument_parser.add_argument("filepath", type=str, help="The file from which the information will be read or stored (JSON Format)")

    exclusive_group = argument_parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument("-b", "--backup", type=str, help="Backup the icons of the given folder")
    exclusive_group.add_argument("-r", "--restore", action="store_true", help="Restore the icons")

    # parse the args
    arguments = argument_parser.parse_args()

    # check if the given paths are valid
    if not local_file.check_file(arguments.filepath):
        local_error.show("The file path given was invalid", argument_parser, True)

    if arguments.backup and not local_file.check_dir(arguments.backup):
        local_error.show("The directory path given was invalid", argument_parser, True)

    # create the manager
    icon_manager = Icons()

    # check the chosen operation and run it
    if arguments.backup:
        data_managed = icon_manager.backup(arguments.backup)
    else:
        icon_manager.restore()


if __name__ == "__main__":
    main()
