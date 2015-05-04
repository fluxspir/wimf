#!/usr/bin/env python

import models
from base import BaseParser
import dateutil.parser

class BeltParser(BaseParser):

    parser_name = "belt"

    def _check_timestamp(self, timestamp):
        return dateutil.parser.parse(timestamp)

    def _get_gpg_key(self, gpgkey):
        q = models.session.query(models.GpgKey)
        q = q.filter(models.GpgKey.key == gpgkey)
        gpgkey = q.one()
        return gpgkey

    def _get_gpg_keys(self, keys_list):
        # let's raise a sqlalchemy error if problem on keys_list
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
                        action="store", dest="beltname",
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

        (options, args) = parser.parse_args(args)

        if options.timestamp:
            options.timestamp = self._check_timestamp(options.timestamp)

        if options.gpg_keys and options.gpg_key:
            # let's make one of this mess
            options.gpg_keys.append(options.gpg_key)
        if options.gpg_keys:
            options.gpg_keys = self._get_gpg_keys(options.gpg_keys)
        if options.gpg_key:
            # unifying variable used by Command, later
            options.gpg_keys = self._get_gpg_key(options.gpg_key)

        return options, args
