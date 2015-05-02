#!/usr/bin/env python

import pdb
import models
import commands
import sqlalchemy

def test_model(test):
    if test:
        try:
            if models.session:
                print("Success: session object exists")
        except:
            raise

def test_add_keyword_geolocation_gpg(test=False):
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
        test_values = [
            { "name": "" , "gps": "" },
            { "name": "Paris", "gps": "" },
            { "name": "Paris", "gps": "43.3 ; 120.6" },
            { "name": "" , "gps": "52N48'33'' , 018E12'30''" }
            ]
        add_geo = commands.misc.AddGeoLocation()

        for values in test_values:
            try:
                add_geo.run(values)
                print("Success: added (name {}, gps {} in __geolocation__ \
                            table".format(values["name"], values["gps"]))
            except:
                raise
        
        # add a gpg_key
        test_values = [
            ( { "key_id": None }, "Success, gpg accept empty id" ),
            ( { "key_id": "NONE" }, "Success, gpg refuse double entry key_id"),
            ( { "key_id": "key_id" }, "Success: gpg accept string"), 
            ( { "key_id": "4096R/BB5A3352"}, "Success: gpg accept key id"),
            ( { "key_id": "0x37acff7261654182"},"Success: gpg accept key hexa")
            ]
        add_gpg = commands.misc.AddGpgKey()
        for values, msg in test_values:
            try:
                add_gpg.run(values)
                print(msg)
            except sqlalchemy.exc.IntegrityError:
                if values["key_id"] is "NONE" or values["key_id"] is None:
                    models.session.rollback()
                    print(msg)
                else:
                    raise

def test_add_vault(test):
    # add a vault [ ( values={}, msg), ]
    if test:
        test_values = [
            ( 
                { "url": None, "name": None, "geolocation": None, 
                                                    "price": None }, 
                                            "Success: Vault refuse null url"
            ),
            ( 
                { "url": "/dev/null", 
                        "name": "trash", "geolocation": None, "price": None },
                        "Success: Vault accept local path {}".format(
                                                                "/dev/null")
            ),
            ( 
                { "url": "franck@prometheus.tamentis.com", 
                    "name": "test_price_num", 
                    "geolocation": 1, 
                    "price": 12.3 },
                    "Success: Vault accept price numeric and geoloc.id"
            ),
            ( 
                { "url": "franck@prometheus.tamentis.com", 
                    "name": "test_price_num", 
                    "geolocation": None, "price": None},
                    "FAILURE: Vault ACCEPT double entry url-name"
            ),
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
    test_add_keyword_geolocation_gpg(True)
    test_add_vault(True)

