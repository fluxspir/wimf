#!/usr/bin/env python

from base import BaseCommand
import models

class AddBelt(BaseCommand):
    """  """
    command_name = "add_belt"
    
    def __init__(self):
       self.values = {}

    def run(self, values):
        self.values = values
        new_belt = models.Belt(**self.values)
        models.session.add(new_belt)
        models.session.commit()
 
