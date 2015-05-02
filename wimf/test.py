#!/usr/bin/env python

import pdb
import models
import commands

def test_model():
    try:
        if models.session:
            print("session object exists")
    except:
        raise

def test_add():
    try:
        add_keyword = commands.misc.AddKeyword()
        values = { "keyword": "Test_add_keyword" }
        add_keyword.run(values)
        print("new keyword {} added to __keyword__ table".format(
                                                            values["keyword"]))
    except:
        raise


if __name__ == "__main__":
    test_model()
    test_add()
