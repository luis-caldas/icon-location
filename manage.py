#!/usr/bin/env python3

import argparse

def main():

    argument_parser = argparse.ArgumentParser(description="Manages the position of icons (backup and restoration) in folders such as $HOME/Desktop")

    # add the needed arguments
    argument_parser.add_argument("path", type=str, help="The path to the folder that will have its items managed")
    argument_parser.add_argument("filepath", type=str, help="The file from which the information will be read or stored")

    exclusive_group = argument_parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument("-b", "--backup", action="store_true", help="Backup the icons")
    exclusive_group.add_argument("-r", "--restore", action="store_true", help="Restore the icons")

    # parse the args
    arguments = argument_parser.parse_args()



if __name__ == "__main__":
    main()
