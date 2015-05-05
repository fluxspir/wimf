#!/usr/bin/env python

from base import BaseParser
import models
from sqlalchemy import or_
import dateutil.parser


class TreeParser(BaseParser):

    parser_name = "tree"

    def _decode_utf8(self, string):
        return string.decode("utf_8")

    def _check_timestamp(self, timestamp):
        return dateutil.parser.parse(timestamp)

    def _get_geoloc_instance(self, ui):
        ui = self._decode_utf8("%{}%".format(ui))
        q = models.session.query(models.GeoLocation)
        g_i = q.filter(or_(
                        models.GeoLocation.name.ilike(ui),
                        models.GeoLocation.gps.ilike(ui))
                        )
        return g_i.first()

    def _get_keywords_instances(self, kwds):
        keywords_instances = []
        for keyword in kwds:
            kw = "%{}".format(keyword)
            q = models.session.query(models.Keyword)
            kw_i = q.filter(or_(
                                models.Keyword.keyword == keyword,
                                models.Keyword.keyword.ilike(kw))
                                ).one()
            keywords_instances.append(kw_i)
        return keywords_instances

    def _get_entities_instances(self, entities_id):
        entities_instances = []
        for entity_id in entities_id:
            q = models.session.query(models.Entity)
            e_i = q.filter(models.Entity.id == entity_id).one()
            entities_instances.append(e_i)
        return entities_instances

    def parse_args(self, command_name, args):

        self.command_name = command_name
        command_action = self.command_name.split()[0]

        parser = self.get_parser()

        if command_action in ["update"]:
            parser.add_argument("-i", "--id", 
                        type=int, dest="tree_id", 
                        help="specify a tree id")

        parser.add_argument("-p", "--path",
                        action="store", dest="path",
                        help="path/to/folder/ in the archive")
        parser.add_argument("-o", "--owner", action="store",
                        dest="owner",
                        help="owner of the tree")
        parser.add_argument("-t", "--timestamp",
                        action="store", dest="timestamp",
                        help="datetime, isoformat")
        parser.add_argument("-d" "--days", type=float,
                        action="store", dest="days_duration",
                        help="Duration of event in days")
        parser.add_argument("-s" "--seconds", type=int,
                        action="store", dest="seconds_duration",
                        help="Duration of event in seconds")
        parser.add_argument("-g", "--geolocation",
                        action="store", dest="geolocation",
                        help="locate the tree events")
        parser.add_argument("-k", "--keywords", nargs="*",
                        action="store", dest="keywords",
                        help="comma separated list of keywords")
        parser.add_argument("-e", "--entities", nargs="*",
                        action="store", dest="entities",
                        help="entities")

        namespace = parser.parse_args(args)

        if namespace.owner:
            namespace.owner = self._decode_utf8(namespace.owner)
        if namespace.path:
            namespace.path = self._decode_utf8(namespace.path)
        if namespace.timestamp:
            namespace.timestamp = self._check_timestamp(namespace.timestamp)
        if namespace.geolocation:
            namespace.geolocation = self._get_geoloc_instance(
                                                        namespace.geolocation)
        if namespace.keywords:
            namespace.keywords = self._get_keywords_instances(
                                                        namespace.keywords)
        if namespace.entities:
            namespace.entities = self._get_entities_instances(
                                                        namespace.entities)
        return namespace, args
