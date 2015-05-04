#!/usr/bin/env python

from base import BaseCommand
import models

class AddBelt(BaseCommand):
    """  """
    command_name = "add belt"
    
    def __init__(self):
       self.values = {}

    def run(self, options):
        self.values = {
            "beltname" = options.beltname.decode("utf_8"),
            
            }
        new_belt = models.Belt(**self.values)
        models.session.add(new_belt)
        models.session.commit()
 
