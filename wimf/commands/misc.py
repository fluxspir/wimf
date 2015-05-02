
#!/usr/bin/env python

from base import BaseCommand
import models

class AddKeyword(BaseCommand):
    """ """
    command__name = "add_keyword"
    
    def __init__(self):
       self.values = {}

    def run(self, values):
       new_keyword = models.Keyword(**self.values)
       models.session.add(new_keyword)
       models.session.commit()
        
