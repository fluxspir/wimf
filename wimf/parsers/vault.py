#!/usr/bin/env python
import pdb
from base import BaseParser
import models
from sqlalchemy import or_
import argparse

class VaultParser(BaseParser):

    parser_name = "vault"

    def _decode_utf8(self, string):
        return string.decode("utf8")

    def _get_geoloc_instance(self, ui):
        """ return geolocation instance """
        
        ui = "%{}%".format(ui)
        q = models.session.query(models.GeoLocation)
        q = q.filter(or_(
                        models.GeoLocation.name.ilike(ui)),
                        (models.GeoLocation.gps.ilike(ui))
                        )
        return q.first()

    def _get_belt_instance(self, belt_id=0, belt_name=""):
        """ return list of belt's instances """
        if belt_id:
            q = models.session.query(models.Belt)
            belt_instance = q.filter(models.Belt.id == belt_id).one()
        else:
            belt_name = "%{}%".format(belt_name)
            q = models.session.query(models.Belt)
            belt_instance = q.filter(models.Belt.name.ilike(belt_name)).one()
        return belt_instance

 
    def parse_args(self, command_name, args):
        self.command_name = command_name
        command_action = command_name.split()[0]
        parser = self.get_parser()

        if command_action in ["update"]:
            parser.add_argument("-i", "--id", type=int, dest="vault_id", 
                                help="specify a vault id")

        parser.add_argument("-u", "--url", action="store",
                         dest="url",
                        help="url of the vault")
        parser.add_argument("-n", "--name", nargs="?",
                        action="store", dest="name",
                        help="name of the vault")
        parser.add_argument("-g", "--geolocation",
                        action="store", dest="geolocation", nargs="?",
                        help="where the vault is physically")
        parser.add_argument("-p", "--price",
                        action="store", type=float, dest="price",
                        help="the price you paid/are paying for the vault")
        parser.add_argument("-b", "--beltnames", nargs="*",
                        action="store", dest="belt_names",
                        help="list of belt-names stored in vault")
        parser.add_argument("--beltids", nargs="*",
                        action="store", type=int, dest="belt_ids",
                        help="list of belt-ID stored in vault")
        # this hidden option is for creating later a "belts" list of
        # belts from belt_id and belt_name
        parser.add_argument("--belts", nargs="*", help=argparse.SUPPRESS)
        namespace = parser.parse_args(args)
        if namespace.url:
            namespace.url = self._decode_utf8(namespace.url)
        if namespace.name:
            namespace.name = self._decode_utf8(namespace.name)
        if namespace.geolocation:
            namespace.geolocation = self._get_geoloc_instance(
                                                        namespace.geolocation)
        if not namespace.belts:
            namespace.belts = []
            if namespace.belt_names:
                for name in namespace.belt_names:
                    belt =  self._get_belt_instance(belt_name=name)
                    namespace.belts.append(belt)
            elif namespace.belt_ids:
                for belt_id in namespace.belt_ids:
                    belt = self._get_belt_instance(belt_id=belt_id)
                    namespace.belts.append(belt)
            else:
                pass

        return namespace, args
