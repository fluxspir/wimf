
#!/usr/bin/env python

import pdb
from base import BaseCommand
import models

class AddKeyword(BaseCommand):
    """ """
    command_name = "add_keyword"
    
    def __init__(self):
       self.values = {}

    def run(self, values):
        self.values = values
        new_keyword = models.Keyword(**self.values)
        models.session.add(new_keyword)
        models.session.commit()

class AddGeoLocation(BaseCommand):
    """ """
    command_name = "add_geolocation"
    def __init__(self):
        self.values = {}
    def run(self, values):
        self.values = values
        new_location = models.GeoLocation(**self.values)
        models.session.add(new_location)
        models.session.commit()

class AddGpgKey(BaseCommand):
    command_name = "add_gpgkey"
    def __init__(self):
        self.values = {}
    def run(self, values):
        self.values = values
        new_gpgkey = models.GpgKey(**self.values)
        models.session.add(new_gpgkey)
        models.session.commit()

