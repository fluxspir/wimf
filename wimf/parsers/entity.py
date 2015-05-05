#!/usr/bin/env python

from base import BaseParser
import models
import os
import argparse
import dateutil.parser
from sqlalchemy import or_

class EntityParser(BaseParser):

    parser_name = "entity"

    def _decode_utf8(self, string):
        return string.decode("utf_8")

    def _check_timestamp(self, timestamp):
        return dateutil.parser.parse(timestamp)

    def _split_path_filename(self, path):
        path = self._decode_utf8(path)
        (path, filename) = os.path.split(path)
        q = models.session.query(models.Tree)
        t_i = q.filter(models.Tree.path == path).one()
        return t_i, filename

    def _get_belt_instance(self, name):
        q = models.session.query(models.Belt)
        b_i = q.filter(models.Belt.name == name).one()
        return b_i

    def _get_geoloc_instance(self, ui):
        ui = "%{}%".format(ui)
        q = models.session.query(models.GeoLocation)
        g_i = q.filter(or_(
                    models.GeoLocation.name.ilike(ui),
                    models.GeoLocation.gps.ilike(ui))
                    )
        return g_i.first()
    
    def _get_keywords_instances(self, kw_list):
        q = models.session.query(models.Keyword)
        kw_i = []
        for kw in kw_list:
            k_i = q.filter(models.Keyword.keyword == kw).one()
            kw_i.append(k_i)
        return kw_i
            

    def parse_args(self, command_name, args):
        self.command_name = command_name
        command_action = self.command_name.split()[0]

        parser = self.get_parser()

        if command_action in [ "update" ]:
            parser.add_argument("-i", "--id", 
                        type=int, dest="entity_id", 
                        help="specify a tree id")
        
        parser.add_argument("--filename", help=argparse.SUPPRESS)
        parser.add_argument("--tree_instance", help=argparse.SUPPRESS)
        parser.add_argument("--belt_instance", help=argparse.SUPPRESS)
        parser.add_argument("path", action="store",
                        help="path from belt_root to filename")
        parser.add_argument("belt", action="store",
                        help="belt name where the path_to_filename is stored")
        parser.add_argument("-t", "--timestamp",
                        action="store", dest="timestamp",
                        help="datetime, isoformat")
        parser.add_argument("-g", "--geolocation",
                        action="store", dest="geolocation",
                        help="locate the entity events")
        parser.add_argument("-e", "--extension",
                        action="store", dest="extension",
                        help="file type ; avi, jpg...")
        parser.add_argument("-r", "--resolution",
                        action="store", dest="resolution",
                        help="resolution")
        parser.add_argument("-m", "--md5", "--md5sum",
                        action="store", dest="md5sum",
                        help="md5sum of the entity")
        parser.add_argument("-S", "--signature",
                        action="store", dest="signature",
                        help="signature of the entity")
        parser.add_argument("-k", "--keywords", nargs="*",
                        action="store", dest="keywords",
                        help="comma separated list of keywords")

        namespace = parser.parse_args(args)

        if namespace.path:
            (namespace.tree_instance, namespace.filename) =\
                                    self._split_path_filename(namespace.path)
        if namespace.belt:
            namespace.belt_instance = self._get_belt_instance(namespace.belt)
        if namespace.timestamp:
            namespace.timestamp = self._check_timestamp(namespace.timestamp)
        if namespace.geolocation:
            namespace.geolocation = self._get_geoloc_instance(
                                                        namespace.geolocation)
        if namespace.extension:
            namespace.extension = self._decode_utf8(namespace.extension)
        if namespace.resolution:
            namespace.resolution = self._decode_utf8(namespace.resolution)
        if namespace.md5sum:
            namespace.md5sum = self._decode_utf8(namespace.md5sum)
        if namespace.signature:
            namespace.signature = self._decode_utf8(namespace.signature)
        if namespace.keywords:
            namespace.keywords = self._get_keywords_instances(
                                                        namespace.keywords)

        return namespace, args
