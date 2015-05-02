#!/usr/bin/env python

import pdb
import models
import commands
import sqlalchemy

def test_model(True):
    try:
        if models.session:
            print("Success: session object exists")
    except:
        raise

def test_add_keyword_geolocation(test=False):
    if test:
        # add a keyword
        values = { "keyword": "Test_add_keyword" }
        add_keyword = commands.misc.AddKeyword()
        try:
            add_keyword.run(values)
            print("Success: new keyword {} added to __keyword__ table".format(
                                                        values["keyword"]))
        except:
            raise

        # add a geolocation
        if True:
            test_values = [
                { "name": "" , "gps": "" },
                { "name": "Paris", "gps": "" },
                { "name": "Paris", "gps": "43.3 ; 120.6" },
                { "name": "" , "gps": "52N48'33'' , 018E12'30''" }
                ]
            add_geo = commands.misc.AddGeoLocation()

        if True:
            for values in test_values:
                try:
                    add_geo.run(values)
                    print("Success: added (name {}, gps {} in __geolocation__ 
                                table".format(values["name"], values["gps"]))
                except:
                    raise

def test_add_vault(test):
    # add a vault [ ( values={}, msg), ]
    test_values = [
        ( { "url": None, "name": None, "geolocation": None, "price": None }, 
                                            "Success: Vault refuse null url"),
        ( { "url": "/dev/null", 
                    "name": "trash", "geolocation": None, "price": None },
                    "Success: Vault accept local path {}".format("/dev/null")),
        ( { "url": "franck@prometheus.tamentis.com", 
            "name": "test_price_num", 
            "geolocation": 1, 
            "price": 12.3 },
            "Success: Vault accept price numeric and geoloc.id"),
        ( { "url": "franck@prometheus.tamentis.com", 
            "name": "test_price_num", 
            "geolocation": None, "price": None},
            "Success: Vault refuse double entry url-name"),
        ]
    add_vault = commands.vault.AddVault()
    for (values, msg) in test_values:
        try:
            add_vault.run(values)
            print(msg)
        except sqlalchemy.exc.StatementError:
            if not values["url"]:
                models.session.rollback()
                print(msg)
            else:
                raise



if __name__ == "__main__":
    test_model(True)
    test_add_keyword_geolocation(True)
    test_add_vault(True)

