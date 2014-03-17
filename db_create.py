#! /usr/bin/env python
# -*- coding: utf-8 -*-

from web import db
from web.models import User, Station
from werkzeug import generate_password_hash

from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
        MetaData,
        Table,
        DropTable,
        ForeignKeyConstraint,
        DropConstraint,
        )

def db_DropEverything(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn=db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in 
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()



db_DropEverything(db)
db.create_all()

user = User(firstname="admin", lastname="admin", email="email@mail.com", pwdhash=generate_password_hash("password"))
station1 = Station(name="Metz", altitude=200, latitude=49.115558, longitude=6.175635, user_id=user.id)
station2 = Station(name="Luxembourg Kirchberg", altitude=300, latitude=49.6286904, longitude=6.1626319, user_id=user.id)
station3 = Station(name="New-York", altitude=320, latitude=40.717977, longitude=-74.006015, user_id=user.id)
user.stations.extend([station1, station2, station3])

db.session.add(user)
db.session.commit()