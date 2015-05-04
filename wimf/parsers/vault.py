#!/usr/bin/env python

from base import BaseParser

class VaultParser(BaseParser):
    parser_name = "vault"
    def parse_args(self, command_name, args):

        self.command_name = command_name

        parser = self.get_parser()

        parser.add_option("-i", "--id", 
                        type=int, dest="vault_id", 
                        default=None,
                        help="specify a vault id")
        parser.add_option("-u", "--url", action="store",
                        type="string", dest="url",
                        help="url of the vault")
        parser.add_option("-n", "--name",
                        action="store", dest="vault_name",
                        help="name of the vault")
        parser.add_option("-g", "--geolocation",
                        action="store", dest="geolocation",
                        help="where the vault is physically")
        parser.add_option("-p", "--price",
                        action="store", type=float, dest="price",
                        help="the price you paid/are paying for the vault")
        parser.add_option("-b", "--belt",
                        action="store", type=int, dest="belt",
                        help="belt store in vault")

        (options, args) = parser.parse_args(args)

        return options, args
