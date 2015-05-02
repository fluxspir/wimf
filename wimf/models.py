#!/usr/bin/env python


#import pdb
import os
import datetime

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Interval, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()
#session=None

from zope.sqlalchemy import ZopeTransactionExtension

## belts / vault
#belts_vault_table = Table('vault_storage', Base.metadata,
#Column('belt_id', Integer, ForeignKey('belt.id')),
#Column('vault_id', Integer, ForeignKey('vault.id'))
#)
#
## files / belt
#files_belt_table = Table('file_belt', Base.metadata,
#Column('file_id', Integer, ForeignKey('file.id')),
#Column('belt_id', Integer, ForeignKey('belt.id'))
#)
#

class GeoLocation(Base):
    """ name and/or gps coordinate"""
    __tablename__ = "__geolocation__"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="")
    gps = Column(String, default="")

class Vault(Base):
    """ access to the vault
        url: set to something like "protocol://(ip|dns|path)
        name: of the "my_vault" 
        geolocalisation: por example a country name, or an area, a gps...
        price = if needed
        The vault may return which encryted archives are store in him
        """
    __tablename__ = "__vault__"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    name = Column(String, default="")
    geolocation = Column(Integer, ForeignKey(GeoLocation.id))
    price = Column(Numeric, default=0)
    #belts = relationship("Belt", secondary=belts_vault_table, backref="vault")

class Keyword(Base):
    """ """
    __tablename__ = "__keyword__"
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False)

class GpgKey(Base):
    """ 
        Mostly needed if user uses multiples keys, signatures...
        primary key id may be set to str("NONE")
        """
    __tablename__ = "__gpg_key__"
    privatekey_id = Column(String, primary_key=True)
 
class Belt(Base):
    """ The archive file, encrypted (or not if you're brave :) )
        vault: storage location of the archive
        gpg_keys: used to encrypt the archive
        timestamp: could be the Archive encryption 
    """
    __tablename__ = "__belt__"
    id = Column(Integer, primary_key=True)
    vault = Column(Integer, ForeignKey(Vault.id))
    gpg_keys = Column(Integer, ForeignKey(GpgKey.privatekey_id))
    timestamp = Column(DateTime, nullable=False)
    #files = relationship("File", secondary=files_belt_table, backref="belt")

class Tree(Base):
    """ File's "human logical" access point
        owner
        timestamp: when "action" iniciated
        duration: timedelta 
        geolocalisation: ""
        keywords: 
        tree
    """
    __tablename__ = "__tree__"
    id = Column(Integer, primary_key=True)
    owner = Column(String)
    timestamp = Column(DateTime, nullable=False)
    duration = Column(DateTime)
    geolocation = Column(Integer, ForeignKey(GeoLocation.id))
    keywords = Column(Integer, ForeignKey(Keyword.id))
    path = Column(String, nullable=False)

class File(Base):
    """ Individual archived file
        parent: path in the Tree.path_tree
        encrypted_tar: element of an EncryptedArchive
        keywords: denomate the file
        geolocalisation do event
        extension: type of the file
        timestamp: of the event
        resolution: dict of random values
        md5sum: of the file
        signature: of the file
    """
    __tablename__ = "__file__"
    id = Column(Integer, primary_key=True)
    belt = Column(Integer, ForeignKey(Belt.id))
    keywords = Column(Integer, ForeignKey(Keyword.id))
    geolocation = Column(Integer, ForeignKey(GeoLocation.id))
    extension = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    resolution = Column(String)
    md5sum = Column(String)
    signature = Column(String)
    filename = Column(String, nullable=False)
    belt = Column(Integer, ForeignKey(Belt.id))

db_url = os.path.join(os.path.expanduser("~"), ".wimf.sql")
engine = create_engine("sqlite:///{}".format(db_url), 
                                    echo=False, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind = engine))
Base.metadata.create_all(engine)
session = Session()

