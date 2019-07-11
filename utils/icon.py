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
        "program": "/usr/bin/gio",
        "arguments": ["info"]
    },
    "restore": {
        "program": "/usr/bin/gio",
        "arguments": ["set", "-t", "string"]
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

    def print_item(self, number, max_number, string_prefix, string_suffix):
        # get the lenght of the number
        length_number = len(str(max_number))

        print(
            "%s (%s/%d) %s" % (
                string_prefix,
                # print the number padded my the lenght of the maximum number
                ("%%%dd" % length_number) % number,
                max_number,
                string_suffix
            ),

            # if is not the last item just return the carriage
            # if it is print a new line at the end
            end='\n' if number == max_number else '\r'
        )

    def backup(self, backup_path):

        absolute_path = path.abspath(backup_path)

        # get all items in folder
        list_items = self.list_items_dir(absolute_path)

        # calculate the total number of iterations for verbose purposes
        total_iterations = len(list_items)

        # variable that will store the icons data
        icons_data = list()

        # iterate the list and get all the data
        for index, each_item in enumerate(list_items):

            # simple verbose
            self.print_item(index + 1, total_iterations, "Item", "")

            built_command = [
                PROGRAMS["backup"]["program"], *PROGRAMS["backup"]["arguments"],
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

    def restore(self, data_to_restore):

        # calculate the total number of iterations for verbose purposes
        total_iterations = sum(len(each_item[1]) for each_item in data_to_restore)

        # simple counter for verbose
        iteration_n = 0

        # iterate the list of the items
        for each_item in data_to_restore:

            # renaming vars
            path_received = each_item[0]
            attribute_couples = each_item[1]

            # add the attribute prefix
            for each_attr in attribute_couples:
                each_attr[0] = "%s::%s" % (
                    ATTRIBUTE_PREFIX_NAME,
                    each_attr[0]
                )

            # unfortunately i havent found anyt documentation that shows that
            # this commands can replace multiple attributes simmultaneously
            # so a command is run for each attribute set
            for each_attr_couple in attribute_couples:

                # simple verbose
                iteration_n += 1
                self.print_item(iteration_n, total_iterations, "Item", "")

                # build the command
                built_command = [
                    PROGRAMS["restore"]["program"], *PROGRAMS["restore"]["arguments"],
                    path.abspath(path_received),
                    *each_attr_couple
                ]

                # run the built command
                program_output = subprocess.check_output(built_command)
