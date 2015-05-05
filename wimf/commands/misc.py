
#!/usr/bin/env python

import pdb
from base import BaseCommand
import models

class AddKeyword(BaseCommand):
    """ receive list of keywords """
    command_name = "add keyword"
    
    def __init__(self):
        self.values = {}
    
    def run(self, namespace):
        for val in namespace.keywords:
            self.values["keyword"] = val
            new_keyword = models.Keyword(**self.values)
            models.session.add(new_keyword)
        models.session.commit()

class AddGeoLocation(BaseCommand):
    """ """
    command_name = "add geolocation"
    def __init__(self):
        self.values = {}

    def run(self, options):
        self.values = options
        new_location = models.GeoLocation(**self.values)
        models.session.add(new_location)
        models.session.commit()

class AddGpgKey(BaseCommand):
    command_name = "add gpgkey"
    def __init__(self):
        self.values = {}
    def run(self, options):
        self.values = options
        new_gpgkey = models.GpgKey(**self.values)
        models.session.add(new_gpgkey)
        models.session.commit()

