#!/usr/bin/env python

import sys
from base import BaseParser


class KeywordParser(BaseParser):
    parser_name = "keyword"
    def parse_args(self, command_name, args):
        self.command_name = command_name
        parser = self.get_parser()

        parser.add_option("-i", "--id", 
                        type=int, dest="keyword_id", 
                        default=None,
                        help="specify an id")
        parser.add_option("-k", "--keyword", action="store",
                        type="string", dest="keyword",
                        help="whatever needed keyword")

        (options, args) = parser.parse_args(args)

        return options, args

class GeoLocationParser(BaseParser):
    parser_name = "geolocation"
    def parse_args(self, command_name, args):
        self.command_name = command_name
        parser = self.get_parser()

        parser.add_option("-i", "--id", 
                        type=int, action="store", dest="geolocation_id",
                        help="id of the geo_location")
        parser.add_option("-n", "--name",
                        type="string", action="store", dest="geolocation",
                        help="aproximativ location")
        parser.add_option("--gps",
                        type="string", action="store", dest="gps",
                        help="precise location")
        (options, args) = parser.parse_args(args)

        return options, args

class GpgKeyParser(BaseParser):
    parser_name = "gpgkey"
    def parse_args(self, command_name, args):
        self.command_name = command_name
        parser = self.get_parser()

        parser.add_option("-i", "--id",
                        type=int, action="store", dest="gpgkey_id",
                        help="id of key")
        parser.add_option("-K", "--key", "--gpg",
                        type="string", action="store", dest="gpgkey",
                        help="key number identifier")
        (options, args) = parser.parse_args(args)
        
        return options, args
