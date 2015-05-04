#!/usr/bin/env python

import pdb
import models
import commands
import parsers
import sqlalchemy
import datetime


def test_adding(test):
    if test:
        def test_model(test):
            if test:
                try:
                    if models.session:
                        print("Success: session object exists")
                except:
                    raise

        def test_add_keyword_geolocation_gpg(test):
            if test:
                # add a keyword
                test_values = [ { "keyword": "Test_add_keyword" }, 
                { "keyword": "123456"},
                { "keyword": "{ }" }
                ]
                add_keyword = commands.misc.AddKeyword()
                for values in test_values:
                    try:
                        add_keyword.run(values)
                        print("Success: new keyword {} added to keyword table"\
                                                    .format(values["keyword"]))
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
                        print("Success: added (name {}, gps {} in geolocation\
                                table".format(values["name"], values["gps"]))
                    except:
                        raise
                
                # add a gpg_key
                test_values = [
                    ( { "key": None }, "Success, gpg_key refuses null key, using\
                                            'NONE'as default value".strip() ),
                    ( { "key": "NONE" }, "Success, gpg refuse double entry key"),
                    ( { "key": "key" }, "Success: gpg accept string"), 
                    ( { "key": "4096R/BB5A3352"}, "Success: gpg accept key id"),
                    ( { "key": "0x37acff7261654182"},"Success: gpg accept key hexa")
                    ]
                add_gpg = commands.misc.AddGpgKey()
                for values, msg in test_values:
                    try:
                        add_gpg.run(values)
                        print(msg)
                    except sqlalchemy.exc.IntegrityError:
                        models.session.rollback()
                        print(msg)

        def test_add_vault(test):
            # add a vault [ ( values={}, msg), ]
            if test:
                test_values = [
                    ( 
                        { "url": None, "name": None, "geolocation": None, 
                            "price": None , "belts": [] },
                            "Success: Vault refuse null url"
                    ),
                    ( 
                        { "url": "/dev/null", 
                            "name": "trash", "geolocation": None, "price": None,
                            "belts": [] },
                            "Success: Vault accept local path {}".format("/dev/null")
                    ),
                    ( 
                        { "url": "franck@prometheus.tamentis.com", 
                            "name": "test_price_num", 
                            "geolocation": 1, 
                            "price": 12.3, "belts": []  },
                            "Success: Vault accept price numeric and geoloc.id"
                    ),
                    ( 
                        { "url": "franck@prometheus.tamentis.com", 
                            "name": "test_price_num", 
                            "geolocation": None, "price": None,
                            "belts": [] },
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

        def test_add_belt(test):
            if test:
                q = models.session.query(models.GpgKey)
                q.all()
                test_values = [
                    ( { "beltname": "1st belt", "gpg_keys": [], 
                        "timestamp": None,},
                        "Success: Belt refuses None values"),
                    ( { "beltname": "2nd belt","gpg_keys": [q[1]],
                        "timestamp": datetime.datetime.now(), },
                        "Success: of ?"),
                    ( { "beltname": "bla","gpg_keys": [q[1], q[2]] ,
                        "timestamp": datetime.datetime.now(), },
                        "Success: of ?"),
                    ( { "beltname": "should work","gpg_keys": [q[3]],
                        "timestamp": datetime.datetime.now(), },
                        "Success: Belt finds vault_id keys and time")
                    ]
                add_belt = commands.belt.AddBelt()
                for values, msg in test_values:
                    try:
                        add_belt.run(values)
                        print(msg)
                    except AttributeError:
                            raise
                    except sqlalchemy.exc.IntegrityError:
                        raise
        #                for col in values:
        #                    if not values[col]:
        #                        pass
        #                    
        #                    else:
        #                        raise
                        models.session.rollback()
                        print(msg)

        def test_add_tree(test):
            if test:
                kws = models.session.query(models.Keyword)
                kws = kws.all()
                ent = models.session.query(models.Entity)
                ent = ent.all()
                test_values = [
                    ( { "owner": None , 
                        "timestamp": None ,
                        "duration": None , 
                        "geolocation":  None, 
                        "path": None ,
                        "keywords": [] , 
                        "entities": [] }, 
                        "Success: Tree refuses empties datas "),
                    ( { "owner": "user" , 
                        "timestamp": datetime.datetime.now(),
                        "duration": datetime.timedelta(1) , 
                        "geolocation": None ,
                        "path": "path/to/dirname",
                        "keywords": [kws[0]] , 
                        "entities": [], },
                        "Success: geolocalisation, keywords not mandatory" ),
                    ( { "owner": "user2" , 
                        "timestamp": None , 
                        "duration": datetime.timedelta(1) , 
                        "geolocation": 1 ,
                        "path": "path/to/dirfile" ,
                        "keywords":  [kws[1], kws[2]], 
                        "entities": [],} ,
                        "Success: while adding tree"),
#                      { "owner":  , "timestamp":  , "duration": ,
#                        "geolocation": ,
#                        "keywords":  , "path":  },
#                        "Success: "),
                    ]
                add_tree = commands.tree.AddTree()
                for values, msg in test_values:
                    try:
                        add_tree.run(values)
                        print(msg)
                    except AttributeError:
                        print(msg)
                    except sqlalchemy.exc.IntegrityError:
                        for col in values:
                            if not values[col]:
                                pass
                            else:
                                raise
                        models.session.rollback()
                        print(msg)

        def test_add_entity(test):
            if test:
                test_values = [
                    ( { "filename": "name1",
                        "tree_id": 1 , 
                        "belt_id": 1,
                        "geolocation": 0,
                        "extension": "jpg" , "resolution": "1024x768",
                        "timestamp": None , "md5sum": "",
                        "signature": "" ,  } , 
                        "Success: entity refuses non-existent-tree"
                    ),
                    ( { "filename": "name1",
                        "tree_id": 2 , 
                        "belt_id": 1,
                        "geolocation": "",
                        "extension": "jpg" , "resolution": "1024x768",
                        "timestamp": None , "md5sum": "",
                        "signature": "" ,  } , 
                        "Success: geolocation as to exists"
                    ),
                    ( { "filename": "name1",
                        "tree_id": 2 , 
                        "belt_id": 1,
                        "geolocation": 0,
                        "extension": "jpg" , "resolution": "1024x768",
                        "timestamp": None , "md5sum": "",
                        "signature": "" ,  } , 
                        "Success: geolocation as to exists"
                    ),

                    ( { "filename": "name1",
                        "tree_id": 2 , 
                        "belt_id": 1,
                        "geolocation": 1 ,
                        "extension": "mov" , "resolution": "" ,
                        "timestamp": datetime.date.today() , "md5sum": "" ,
                        "signature": ""  } , 
                        "Success: timestamp is a date"
                    )
        #            ( { "tree_id":  , "belt_id":  ,
        #                "keywords":  , "geolocation":  ,
        #                "extension":  , "resolution":  ,
        #                "timestamp":  , "md5sum":  ,
        #                "signature":  ,  } , "Success: " 
        #            ),
                    ]
                add_entity = commands.entity.AddEntity()
                for values, msg in test_values:
                    try:
                        add_entity.run(values)
                        print(msg)
                    except AttributeError:
                        print(msg)
                    except sqlalchemy.exc.IntegrityError:
                        if values["tree_id"] == 1:
                            print(msg)
                            models.session.rollback()
                        elif values["geolocation"] == 0:
                            print(msg)
                            models.session.rollback()
                        else:
                            raise
                    except sqlalchemy.exc.DataError:
                        if values["geolocation"] == "":
                            print(msg)
                            models.session.rollback()
                        else:
                            raise

        test_model(True)
        test_add_keyword_geolocation_gpg(True)
        test_add_vault(False)
        test_add_belt(False)
        test_add_tree(False)
        test_add_entity(False)

def test_parsing(test):
    if test:
        def test_parsing_misc(test):
            if test:
                # Test parsing keyword (not effective)
                test_values = [
                    ( None , None, "FAILURE: Empty command_name and args are parsed"),
                    ( "add_other", [], 
                        "FAILURE: weird command_name refused"),
                    ( "add_keyword", [], 
                        "Success: command name add_keyword  accepted"),
                    ( "add_keyword", [ "-k", "test_parsed_keyword_1" ],
                        "Success: test_parsed_keyword_1 parsed correctly"),
                    ( "add_keyword", [ "--keyword", "test various parsed keyword 2"],
                        "Success: test various parsed" )
                    ]
                parse_keyword = parsers.misc.KeywordParser()
                for command_name, args, msg in test_values:
                    try:
                        parse_keyword.parse_args(command_name, args)
                        print(msg)
                    except:
                        raise

        test_parsing_misc(True)


if __name__ == "__main__":
    test_adding(True)
    test_parsing(False)

