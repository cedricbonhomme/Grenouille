#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Grenouille - An online service for weather data.
# Copyright (C) 2014 Cédric Bonhomme - http://cedricbonhomme.org/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2014/03/16 $"
__revision__ = "$Date: 2014/03/24 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "AGPLv3"

from web import db
from web.models import User, Station, Role
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

    conn = db.engine.connect()

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
            if not fk["name"]:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk["name"]))
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


db_DropEverything(db)
db.create_all()

role_admin = Role(name="admin")
role_user = Role(name="user")

user1 = User(
    firstname="admin",
    lastname="admin",
    email="root@grenouille.localhost",
    pwdhash=generate_password_hash("root"),
)

user1.roles.extend([role_admin, role_user])

station1 = Station(
    name="Metz",
    country="FR",
    altitude=200,
    latitude=49.115558,
    longitude=6.175635,
    user_id=user1.id,
)
station2 = Station(
    name="Luxembourg Kirchberg",
    country="LU",
    altitude=300,
    latitude=49.6286904,
    longitude=6.1626319,
    user_id=user1.id,
)
station3 = Station(
    name="New-York",
    country="US",
    altitude=320,
    latitude=40.717977,
    longitude=-74.006015,
    user_id=user1.id,
)
user1.stations.extend([station1, station2, station3])

db.session.add(user1)
db.session.commit()
