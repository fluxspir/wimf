#!/usr/bin/env python

from base import BaseCommand
import models

class AddEntity(BaseCommand):
    """  """
    command_name = "add entity"
    
    def __init__(self):
       self.values = {}

    def run(self, values):
        self.values = values
        new_entity = models.Entity(**self.values)
        models.session.add(new_entity)
        models.session.commit()
 
