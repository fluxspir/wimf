#!/usr/bin/env python

import sys
from base import BaseParser


class TreeParser(BaseParser):
    parser_name = "tree"
    def parse_args(self, command_name, args):
        self.command_name = command_name
        parser = self.get_parser()

        parser.add_option("-i", "--id", 
                        type=int, dest="tree_id", 
                        default=None,
                        help="specify a tree id")
        parser.add_option("-o", "--owner", action="store",
                        type="string", dest="url",
                        help="url of the vault")
        parser.add_option("-t", "--timestamp",
                        action="store", dest="timestamp",
                        help="datetime, isoformat")
        parser.add_option("-d" "--days",
                        action="store", dest="days_duration",
                        help="Duration of event in days")
        parser.add_option("-s" "--seconds",
                        action="store", dest="seconds_duration",
                        help="Duration of event in seconds")
        parser.add_option("-g", "--geolocation",
                        action="store", dest="geolocation",
                        help="locate the tree events")
        parser.add_option("-p", "--path",
                        action="store", dest="path",
                        help="path/to/folder/ in the archive")
        parser.add_option("-k", "--keywords",
                        action="store", dest="keywords",
                        help="comma separated list of keywords")
        parser.add_option("-e", "--entities",
                        action="store", dest="entities",
                        help="entities")

        (options, args) = parser.parse_args(args)

        return options, args
