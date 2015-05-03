#!/usr/bin/env python

from base import BaseCommand
import models

class AddTree(BaseCommand):
    """  """
    command_name = "add_tree"
    
    def __init__(self):
       self.values = {}

    def run(self, values):
        self.values = values
        new_tree = models.Tree(**self.values)
        models.session.add(new_tree)
        models.session.commit()
        
