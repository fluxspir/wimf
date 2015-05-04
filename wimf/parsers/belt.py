#!/usr/bin/env python

import pdb
import models
from base import BaseParser
import dateutil.parser

class BeltParser(BaseParser):

    parser_name = "belt"

    def _check_timestamp(self, timestamp):
        return dateutil.parser.parse(timestamp)

    def _decode_utf8(self, string):
        return string.decode("utf_8")

    def _get_gpg_key(self, gpgkey):
        gpg_keys = []
        q = models.session.query(models.GpgKey)
        q = q.filter(models.GpgKey.key == gpgkey)
        gpgkey = q.one()
        gpg_keys.append(gpgkey)
        return gpg_keys

    def _get_gpg_keys(self, keys_list):
        # let's raise a sqlalchemy error if problem on keys_list
        # return list of instances.
        keys_list = keys_list.split(",")
        gpg_keys = []
        for key in keys_list:
            gk_i = models.session.query(models.GgpKey).filter(
                                models.GpgKey.key == key).one()
            gpg_keys.append(gk_i)
        return gpg_keys

    def parse_args(self, command_name, args):
        
        self.command_name = command_name

        parser = self.get_parser()

        parser.add_option("-i", "--id", 
                        type=int, dest="belt_id", default=None,
                        help="specify a belt id")
        parser.add_option("-n", "--name",
                        action="store", dest="name",
                        help="name of the vault")
        parser.add_option("-g", "--gpg-key",
                        action="store", dest="gpg_key",
                        help="one gpg_key used to encrypt the belt")
        parser.add_option("--gpg-keys",
                        action="store", dest="gpg_keys",
                        help="comma separated list of keys between \" \" of keys")
        parser.add_option("-d", "--datetime", "--timestamp",
                        action="store", dest="timestamp",
                        help="belt creation datetime, ISO : YYYY-mm-dd[@HHMM]")
        parser.add_option("-e", "--entities", 
                        action="store", dest="entities",
                        help="comma separated list between \" \" of entities-id")

        (options, args) = parser.parse_args(args)

        if options.name:
            options.name = self._decode_utf8(options.name)

        if options.timestamp:
            options.timestamp = self._check_timestamp(options.timestamp)

        if options.gpg_keys and options.gpg_key:
            # let's make one of this mess
            options.gpg_keys.append(options.gpg_key)
        elif options.gpg_keys:
            options.gpg_keys = self._get_gpg_keys(options.gpg_keys)
        elif options.gpg_key:
            # unifying variable used by Command, later
            options.gpg_keys = self._get_gpg_key(options.gpg_key)
            pdb.set_trace()
        else:
            pass

        return options, args
