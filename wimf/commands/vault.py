#!/usr/bin/env python

from base import BaseCommand
import models

class AddVault(BaseCommand):
    """  """
    command_name = "add vault"
    
    def __init__(self):
       self.values = {}

    def run(self, values):
        self.values = values
        new_vault = models.Vault(**self.values)
        models.session.add(new_vault)
        models.session.commit()
        
