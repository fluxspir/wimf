#!/usr/bin/env python

from optparse import OptionParser

class BaseCommand():
    
    def get_parser(self):
        return OptionParser(usage="%prog {}".format(self.command_name))

