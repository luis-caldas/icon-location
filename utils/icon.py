# -*- coding: utf-8 -*-

import re
import subprocess

from os import path
from os import listdir

ATTRIBUTE_PREFIX_NAME = "metadata"
ATTRIBUTE_COMBO_REGEX = "::(?P<name>[^:]+): (?P<value>.+)\n"

ATTRIBUTES_ALLOWED = {
    "items": ["icon-scale", "nemo-icon-position"],
    "root":  [
        "nemo-icon-view-zoom-level",
        "nemo-icon-view-auto-layout",
        "nemo-icon-view-tighter-layout"
    ]
}

PROGRAMS = {
    "backup": {
        "info": "/usr/bin/gvfs-info",
        "arguments": []
    },
    "restore": {
        "program": "gvfs-set-attribute",
        "arguments": ["-t", "string"]
    }
}


class Icons:

    def list_items_dir(self, given_path):
        # get all the items in the folder
        return [
            given_path,
            *[
                path.join(given_path, each_item)
                for each_item in listdir(given_path)
            ]
        ]

    def get_gvfs_output_values(self, item_prefix: str, data_input: str):

        # build the regex for the matching
        regex = "%s%s" % (item_prefix, ATTRIBUTE_COMBO_REGEX)

        # get and format the found items
        all_found = [
            [each_found.group("name"), each_found.group("value")]
            for each_found in re.finditer(regex, data_input)
        ]

        # return the list with all
        return all_found

    def remove_unwanted(self, allowed_list, input_list):
        return [each_allowed for each_allowed in input_list if each_allowed[0] in allowed_list]

    def backup(self, backup_path):

        absolute_path = path.abspath(backup_path)

        # get all items in folder
        list_items = self.list_items_dir(absolute_path)

        # variable that will store the icons data
        icons_data = list()

        # iterate the list and get all the data
        for each_item in list_items:

            built_command = [
                PROGRAMS["backup"]["info"], *PROGRAMS["backup"]["arguments"],
                path.abspath(each_item)
            ]

            # run the built command
            program_output = subprocess.check_output(built_command)

            # gvfs values
            values_list = self.get_gvfs_output_values(ATTRIBUTE_PREFIX_NAME, program_output.decode())

            # reap unwanted items
            cleansed_values = self.remove_unwanted(
                ATTRIBUTES_ALLOWED["root" if each_item == absolute_path else "items"],
                values_list
            )

            # add to the icons data
            icons_data.append([
                each_item,
                cleansed_values
            ])

        # return the data
        return icons_data

    def restore(self):

        pass
