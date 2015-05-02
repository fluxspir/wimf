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
    # add a keyword
    values = { "keyword": "Test_add_keyword" }
    add_keyword = commands.misc.AddKeyword()
    try:
        add_keyword.run(values)
        print("new keyword {} added to __keyword__ table".format(
                                                            values["keyword"]))
    except:
        raise

    # add a geolocation
    test_values = [
        { "name": "" , "gps": "" },
        { "name": "Paris", "gps": "" },
        { "name": "Paris", "gps": "43.3 ; 120.6" },
        { "name": "" , "gps": "52N48'33'' , 018E12'30''" }
        ]
    add_geo = commands.misc.AddGeoLocation()
    try:
        for values in test_values:
            add_geo.run(values)
            print("added (name {}, gps {} in __geolocation__ table".format(
                                            values["name"], values["gps"]))
    except:
        raise


if __name__ == "__main__":
    test_model()
    test_add()
