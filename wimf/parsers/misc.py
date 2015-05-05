#!/usr/bin/env python

import pdb
import sys
from base import BaseParser


class KeywordParser(BaseParser):
    
    parser_name = "keyword"
    
    def _decode_utf8(self, string):
        return string.decode("utf_8")

    def parse_args(self, command_name, args):
        self.command_name = command_name
        command_action = command_name.split()[0]
        parser = self.get_parser()

        if command_action in ["update"]:
            parser.add_argument("-i", "--id", type=int, dest="keyword_id", 
                                                    help="specify an id")

        parser.add_argument("keywords", nargs="+", action="store",
                        help="list of keywords")

        namespace = parser.parse_args(args)
        if namespace.keywords:
            namespace.keywords = [self._decode_utf8 (kw) \
                                                for kw in namespace.keywords ]
        return namespace, args

class GeoLocationParser(BaseParser):
    parser_name = "geolocation"
    
    def _decode_utf8(self, string):
        return string.decode("utf_8")

    def parse_args(self, command_name, args):
        self.command_name = command_name
        command_action = command_name.split()[0]
        parser = self.get_parser()
        if command_action in ["update"]:
            parser.add_argument("-i", "--id", 
                        type=int, action="store", dest="geolocation_id",
                        help="id of the geo_location")

        parser.add_argument("-n", "--name", nargs="?",
                        action="store", dest="geolocation",
                        help="aproximativ location")
        parser.add_argument("--gps", nargs="?",
                        action="store", dest="gps",
                        help="precise location")

        namespace = parser.parse_args(args)

        if namespace.geolocation:
            namespace.geolocation = self._decode_utf8(namespace.geolocation)
        if namespace.gps:
            namespace.gps = self._decode_utf8(namespace.gps)

        return namespace, args

class GpgKeyParser(BaseParser):
    parser_name = "gpgkey"
    
    def _decode_utf8(self, string):
        return string.decode("utf_8")

    def parse_args(self, command_name, args):
        self.command_name = command_name
        command_action = self.command_name.split()[0]
        parser = self.get_parser()

        if command_action in [ "update",]:
            parser.add_argument("-i", "--id",
                        type=int, action="store", dest="gpgkey_id",
                        help="id of key")
        parser.add_argument("-K", "--key", "--gpg", nargs="*",
                        type="string", action="store", dest="gpgkey",
                        help="key number identifier")
        namespace = parser.parse_args(args)

        if namespace.gpgkey:
            namespace.gpgkey = [ self._decode_utf8(key)\
                                                for key in namespace.gpgkey ]
        
        return namespace, args
