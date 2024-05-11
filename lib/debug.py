#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import ipdb
from models.guest import Guest
from models.hotel import Hotel


def reset_database():
    Guest.drop_table()
    Hotel.drop_table()
    Hotel.create_table()
    Guest.create_table()

    # Create seed data
    lafayette = Hotel.create("The Lafayette", "50st and Lafayette, New York, NY")
    sprinkle = Hotel.create("The Sprinkle", "281 East Harlem 148st, New York")
    guest1 = Guest.create("Lee", lafayette.id)
    guest2 = Guest.create("Sasha", sprinkle.id)
    print(guest1)
    print(guest2)



reset_database()
ipdb.set_trace()

