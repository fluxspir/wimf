
#!/usr/bin/env python

import pdb
from base import BaseCommand
import models

class AddKeyword(BaseCommand):
    """ """
    command_name = "add keyword"
    
    def __init__(self):
        self.values = {}
    
    def run(self, options):
        pdb.set_trace()
        self.values = {
            "keyword": options.keyword.decode("utf_8"),
            }
        new_keyword = models.Keyword(**self.values)
        models.session.add(new_keyword)
        models.session.commit()

class AddGeoLocation(BaseCommand):
    """ """
    command_name = "add geolocation"
    def __init__(self):
        self.values = {}

    def run(self, options):
        self.values = {
            "name": options.name.decode("utf_8"),
            "gps": options.gps.decode("utf_8")
            }
        new_location = models.GeoLocation(**self.values)
        models.session.add(new_location)
        models.session.commit()

class AddGpgKey(BaseCommand):
    command_name = "add gpgkey"
    def __init__(self):
        self.values = {}
    def run(self, options):
        self.values = {
            "key": options.gpgkey.decode("utf_8"),
            }
        new_gpgkey = models.GpgKey(**self.values)
        models.session.add(new_gpgkey)
        models.session.commit()

