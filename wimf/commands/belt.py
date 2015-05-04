#!/usr/bin/env python

from base import BaseCommand
import models

class AddBelt(BaseCommand):
    """  """
    command_name = "add belt"
    
    def __init__(self):
       self.values = {}
    
    def run(self, options):
        import pdb
        pdb.set_trace()
        self.values = {
            "name": options.name.decode("utf_8"),
            "timestamp": options.timestamp,
            "gpg_keys": options.gpg_keys,
            "entities": options.entities,
            }
        new_belt = models.Belt(**self.values)
        models.session.add(new_belt)
        models.session.commit()
 
