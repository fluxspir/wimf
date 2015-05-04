#!/usr/bin/env python

import sys
from base import BaseParser


class EntityParser(BaseParser):
    parser_name = "entity"
    def parse_args(self, command_name, args):
        self.command_name = command_name
        parser = self.get_parser()

        parser.add_option("-i", "--id", 
                        type=int, dest="entity_id", 
                        default=None,
                        help="specify a tree id")
        parser.add_option("-f", "--filename", action="store",
                        type="string", dest="filename",
                        help="entity's filename")
        parser.add_option("-p", "--path",
                        action="store", type=int, dest="tree_id",
                        help="tree.id for corresponding path")
        parser.add_option("-b", "--belt",
                        action="store", type=int, dest="belt_id",
                        help="belt id where entity is store")
        parser.add_option("-t", "--timestamp",
                        action="store", dest="timestamp",
                        help="datetime, isoformat")
        parser.add_option("-g", "--geolocation",
                        action="store", dest="geolocation",
                        help="locate the entity events")
        parser.add_option("-e", "--extension",
                        action="store", dest="extension",
                        help="file type ; avi, jpg...")
        parser.add_option("-r", "--resolution",
                        action="store", dest="resolution",
                        help="resolution")
        parser.add_option("-m", "--md5", "--md5sum",
                        action="store", dest="md5sum",
                        help="md5sum of the entity")
        parser.add_option("-S", "--signature",
                        action="store", dest="signature",
                        help="signature of the file")
        parser.add_option("-k", "--keywords",
                        action="store", dest="keywords",
                        help="comma separated list of keywords")

        (options, args) = parser.parse_args(args)

        return options, args
