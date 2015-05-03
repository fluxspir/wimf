#!/usr/bin/env python

import sys
from optparse import OptionParser


def __init__(self):
    pass

class BaseCommand():

    def get_parser(self):
        return OptionParser("usage=%prog {}".format(self.command_name))

class BeltParser(BaseCommand):
    def parse_args(self, command_name, args):
        self.command_name = command_name
        parser = self.get_parser()

        parser.add_option("-i", "--id", 
                        type=int, dest="belt_id", 
                        default=None,
                        help="specify a belt id")
        parser.add_option("-n", "--name",
                        action="store", dest="belt_name",
                        help="name of the vault")
        parser.add_option("-g", "--gpg-keys",
                        action="store", dest="gpg_keys"
                        help="gpg_keys used to encrypt the belt")
        parser.add_option("-d", "--datetime", "--timestamp"
                        action="store", dest="timestamp"
                        help="belt creation datetime, ISO : YYYY-mm-dd[@HHMM]")

        (options, args) = parser.parse_args(args)

        return options, args
