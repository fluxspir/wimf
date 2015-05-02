#!/usr/bin/env python


#import pdb
import os
import ConfigParser
import datetime

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Interval, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()
#session=None

from zope.sqlalchemy import ZopeTransactionExtension

# entity - keywords
entity_keywords_table = Table('entity_keywords', Base.metadata,
Column('entity_id', Integer, ForeignKey('entity.id')),
Column('keyword_id', Integer, ForeignKey('keyword.id'))
)
# tree - keywords
tree_keywords_table = Table('tree_keywords', Base.metadata,
Column('tree_id', Integer, ForeignKey('tree.id')),
Column('keyword_id', Integer, ForeignKey('keyword.id'))
)
# belt - gpg_keys
belt_gpg_keys_table = Table('belts_gpg_keys', Base.metadata,
Column('gpg_key_id', Integer, ForeignKey('gpg_key.id')),
Column('belt_id', Integer, ForeignKey('belt.id'))
)
# vault - belts
#vault_belts_table = Table("vault_belts", Base.metadata,
#Column("belt_id", Integer, ForeignKey("belt.id")),
#Column("vault_id", Integer, ForeignKey("vault.id"))
#)

class Keyword(Base):
    """ """
    __tablename__ = "keyword"
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False)

class GeoLocation(Base):
    """ name and/or gps coordinate"""
    __tablename__ = "geolocation"
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
    __tablename__ = "vault"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    name = Column(String, default="")
    geolocation = Column(Integer, ForeignKey(GeoLocation.id))
    price = Column(Numeric, default=0)
    belts = relationship("Belt", secondary=vault_belts_table)

class GpgKey(Base):
    """ 
        Mostly needed if user uses multiples keys, signatures...
        primary key id may be set to str("NONE")
        """
    __tablename__ = "gpg_key"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, default="NONE", nullable=False)
 
class Belt(Base):
    """ The archive file, encrypted (or not if you're brave :) )
        vault: storage location of the archive
        gpg_keys: used to encrypt the archive
        timestamp: could be the Archive encryption 
    """
    __tablename__ = "belt"
    id = Column(Integer, primary_key=True)
    beltname = Column(String, nullable=False)
    gpg_keys = relationship("GpgKey", secondary=belt_gpg_keys_table)
    timestamp = Column(DateTime, nullable=False)
    vault_id = Column(Integer, ForeignKey(Vault.id))

class Tree(Base):
    """ File's "human logical" access point
        owner
        timestamp: when "action" iniciated
        duration: timedelta 
        geolocalisation: ""
        keywords: 
        tree
    """
    __tablename__ = "tree"
    id = Column(Integer, primary_key=True)
    owner = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    duration = Column(Interval)
    geolocation = Column(Integer, ForeignKey(GeoLocation.id))
    path = Column(String, nullable=False)
    keywords = relationship("Keyword", secondary=tree_keywords_table)
    entities = relationship("Entity")

class Entity(Base):
    """ Individual archived file
        tree_id: location of the file
        belt_id: element of a Belt
        geolocalisation do event
        timestamp: of the event
        extension: type of the file
        resolution: dict of random values
        md5sum: of the file
        signature: of the file
        keywords: denomate the file
    """
    __tablename__ = "entity"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    tree_id = Column(Integer, ForeignKey(Tree.id)) # add constraint tree_id - filename unique
    belt_id = Column(Integer, ForeignKey(Belt.id)) 
    geolocation = Column(Integer, ForeignKey(GeoLocation.id))
    timestamp = Column(DateTime, default=datetime.datetime.now())
    extension = Column(String)
    resolution = Column(String)
    md5sum = Column(String)
    signature = Column(String)
    keywords = relationship("Keyword", secondary=entity_keywords_table)

parser = ConfigParser.ConfigParser()
home = os.path.expanduser("~")
parser.read(os.path.join(home, ".franckdbrc"))
db_url = parser.get("wimf", "url")
engine = create_engine(db_url, echo=False, convert_unicode=True)
#db_url = os.path.join(home, ".wimf.sql")
#engine = create_engine("sqlite:///{}".format(db_url), 
#                                    echo=False, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind = engine))
Base.metadata.create_all(engine)
session = Session()

