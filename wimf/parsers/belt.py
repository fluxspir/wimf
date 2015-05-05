#!/usr/bin/env python

import models
from base import BaseParser
import dateutil.parser
import argparse

class BeltParser(BaseParser):

    parser_name = "belt"

    def _check_timestamp(self, timestamp):
        return dateutil.parser.parse(timestamp)

    def _decode_utf8(self, string):
        return string.decode("utf_8")

    def _get_gpgkey_instance(self, gpgkeys=[], gpgkey_id=0, gpgkey_name=""):
        """ returns a gpg_key_instance """
        if gpgkey_id:
            q = models.session.query(models.GpgKey)
            q = q.filter(models.GpgKey.id == gpgkey_id).one()
        else:
            gpgkey_name = "%{}%".format(gpgkey_name)
            q = q.filter(models.GpgKey.key.ilike(gpgkey_name)).one()
        return q

    def _get_entities_instances(self, entities_id=[]):
        """ returns a list of entities' instances """
        entities_instances = []
        for entity_id in entities_id:
            q = models.session.query(models.Entity)
            entity = q.filter(models.Entity.id == entity_id).one()
            entities_instances.append(entity)
        return entities_instances

    def parse_args(self, command_name, args):
        
        self.command_name = command_name
        command_action = self.command_name.split()[0]
        parser = self.get_parser()

        if command_name in [ "update" ]:
            parser.add_argument("-i", "--id", 
                            type=int, dest="belt_id",
                            help="specify a belt id")
        parser.add_argument("-n", "--name", nargs="?",
                        action="store", dest="name",
                        help="name of the belt")
        parser.add_argument("--gpg-keys-id", nargs="*",
                        action="store", dest="gpg_keys_id", type=int,
                        help="gpg_keys db_id used to encrypt the belt")
        parser.add_argument("--gpg-keys-name", "--gpg-keys", nargs="*",
                        action="store", dest="gpg_keys_name",
                        help="list of keys used to encrypt the belt")
        #### hidden argument to make the gpg-key mix of names and ids
        parser.add_argument("--gpg_keys_instances", help=argparse.SUPPRESS)
        ####
        parser.add_argument("--md5", "--md5sum",
                        action="store", dest="md5sum",
                        help="md5sum of the belt")
        parser.add_argument("-S", "--signature",
                        action="store", dest="signature",
                        help="signature of the belt")
        parser.add_argument("-t", "--timestamp",
                        action="store", dest="timestamp",
                        help="belt creation datetime")
        parser.add_argument("-e", "--entities", nargs="*",
                        action="store", type=int, dest="entities",
                        help="list of files/entities ID guarded in belt")

        namespace = parser.parse_args(args)

        if namespace.name:
            namespace.name = self._decode_utf8(namespace.name)

        if namespace.timestamp:
            namespace.timestamp = self._check_timestamp(namespace.timestamp)
        
        if not namespace.gpg_keys_instances:
            namespace.gpg_keys_instances = []
            if namespace.gpg_keys_id:
                for gpgkey_id in namespace.gpg_keys_id:
                    gpg_key_instance = self._get_gpgkey_instance(
                                                        gpgkey_id=gpgkey_id)
                    namespace.gpg_keys_instances.append(gpg_key_instance)
            elif namespace.gpg_keys_name:
                for name in namespace.gpg_keys_name:
                    gpg_key_instance = self._get_gpgkey_instance(
                                                            gpgkey_name=name)
                    namespace.gpg_keys_instances.append(gpg_key_instance)
            else:
                pass

        if namespace.entities:
            namespace.entities = self._get_entities_instances(
                                                         namespace.entities)

        return namespace, args
