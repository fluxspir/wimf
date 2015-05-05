#!/usr/bin/env python

import argparse

class BaseParser():

    def get_parser(self):
        return argparse.ArgumentParser(description=
                        "usage=%prog {}".format(self.command_name))
