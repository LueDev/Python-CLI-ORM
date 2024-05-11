from models.__init__ import CONN, CURSOR
from models.guest import Guest
from models.hotel import Hotel
from faker import Faker
import pytest


class TestGuest:
    '''Class Guest in guest.py'''

    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''drop tables prior to each test.'''

        CURSOR.execute("DROP TABLE IF EXISTS guests")
        CURSOR.execute("DROP TABLE IF EXISTS hotels")

        Hotel.all = {}
        Guest.all = {}

    def test_creates_table(self):
        '''contains method "create_table()" that creates table "guests" if it does not exist.'''

        Hotel.create_table()  # ensure Hotel table exists due to FK constraint
        Guest.create_table()
        assert (CURSOR.execute("SELECT * FROM guests"))

    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "guests" if it exists.'''

        sql = """
            CREATE TABLE IF NOT EXISTS hotels
                (id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT)
        """
        CURSOR.execute(sql)

        sql = """  
            CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY,
            name TEXT,
            hotel_id INTEGER,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id))
        """
        CURSOR.execute(sql)

        Guest.drop_table()

        # Confirm hotels table exists
        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='hotels'
            LIMIT 1
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result)

        # Confirm guests table does not exist
        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='guests'
            LIMIT 1
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result is None)

    def test_saves_guest(self):
        '''contains method "save()" that saves an Guest instance to the db and sets the instance id.'''

        Hotel.create_table()
        hotel = Hotel("The Glizzy", "East Harlem")
        hotel.save()  # tested in hotel_test.py

        Guest.create_table()
        guest = Guest("Sasha", hotel.id)
        guest.save()

        sql = """
            SELECT * FROM guests
        """

        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (guest.id, guest.name, guest.hotel_id) ==
                (guest.id, "Sasha", hotel.id))

    def test_creates_guest(self):
        '''contains method "create()" that creates a new row in the db using the parameter data and returns an Guest instance.'''

        Hotel.create_table()
        hotel = Hotel("Sonder", "545 Utica Avenue")
        hotel.save()  # tested in hotel_test.py

        Guest.create_table()
        guest = Guest.create("Kai", hotel.id)

        sql = """
            SELECT * FROM guests
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (guest.id, guest.name, guest.hotel_id) ==
                (guest.id, "Kai", hotel.id))

    def test_updates_row(self):
        '''contains a method "update()" that updates an instance's corresponding database record to match its new attribute values.'''

        Hotel.create_table()
        hotel1 = Hotel("Sonder", "545 Utica Avenue")
        hotel1.save()
        hotel2 = Hotel("Human Resources", "Building C, 2nd Floor")
        hotel2.save()

        Guest.create_table()

        guest1 = Guest.create("Raha", hotel1.id)
        guest2 = Guest.create(
            "Tal", hotel2.id)
        id1 = guest1.id
        id2 = guest2.id
        guest1.name = "Raha Lee"
        guest1.hotel_id = hotel2.id
        guest1.update(guest1.name, guest1.hotel_id)

        # Confirm guest updated
        guest = Guest.find_by_id(id1)
        assert ((guest.id, guest.name, guest.hotel_id) ==
                (guest1.id, guest1.name, guest1.hotel_id) ==
                (id1, "Raha Lee", hotel2.id))

        # Confirm guest not updated
        guest = Guest.find_by_id(id2)
        assert ((guest.id, guest.name, guest.hotel_id) ==
                (guest2.id, guest2.name, guest2.hotel_id) ==
                (id2, "Tal", hotel2.id))

    def test_deletes_row(self):
        '''contains a method "delete()" that deletes the instance's corresponding database record'''
        Hotel.create_table()
        hotel = Hotel("Sonder", "545 Utica Avenue")
        hotel.save()

        Guest.create_table()

        guest1 = Guest.create("Raha", hotel.id)
        id1 = guest1.id
        guest2 = Guest.create(
            "Tal", hotel.id)
        id2 = guest2.id

        guest = Guest.find_by_id(id1)
        guest.delete()
        # assert row deleted
        assert (Guest.find_by_id(guest1.id) is None)
        # assert Guest object state is correct, id should be None
        assert ((guest1.id, guest1.name, guest1.hotel_id) ==
                (None, "Raha", hotel.id))
        # assert dictionary entry was deleted
        assert (Guest.all.get(id1) is None)

        guest = Guest.find_by_id(id2)
        # assert guest2 row not modified, guest2 object not modified
        assert ((guest.id, guest.name, guest.hotel_id) ==
                (guest2.id, guest2.name, guest2.hotel_id) ==
                (id2, "Tal", hotel.id))

    def test_instance_from_db(self):
        '''contains method "instance_from_db()" that takes a db row and creates an Guest instance.'''

        Hotel.create_table()
        hotel = Hotel("Sonder", "545 Utica Avenue")
        hotel.save()  # tested in hotel_test.py

        Guest.create_table()
        sql = """
            INSERT INTO guests (name, hotel_id)
            VALUES ('Amir', ?)
        """
        CURSOR.execute(sql, (hotel.id,))

        sql = """
            SELECT * FROM guests
        """
        row = CURSOR.execute(sql).fetchone()

        guest = Guest.instance_from_db(row)
        assert ((row[0], row[1], row[2]) ==
                (guest.id, guest.name, guest.hotel_id) ==
                (guest.id, "Amir", hotel.id))

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Guest instances for every record in the db.'''

        Hotel.create_table()
        hotel = Hotel("Sonder", "545 Utica Avenue")
        hotel.save()

        Guest.create_table()
        guest1 = Guest.create("Tristan", hotel.id)
        guest2 = Guest.create("Sasha", hotel.id)

        guests = Guest.get_all()
        assert (len(guests) == 2)
        assert ((guests[0].id, guests[0].name, guests[0].hotel_id) ==
                (guest1.id, guest1.name, guest1.hotel_id))
        assert ((guests[1].id, guests[1].name, guests[1].hotel_id) ==
                (guest2.id, guest2.name, guest2.hotel_id))

    def test_finds_by_name(self):
        '''contains method "find_by_name()" that returns an Guest instance corresponding to the db row retrieved by name.'''

        Hotel.create_table()
        hotel = Hotel("Sonder", "545 Utica Avenue")
        hotel.save()
        Guest.create_table()
        faker = Faker()
        guest1 = Guest.create(faker.name(), hotel.id)
        guest2 = Guest.create(
            faker.name(), hotel.id)

        guest = Guest.find_by_name(guest1.name)
        assert (
            (guest.id, guest.name, guest.hotel_id) ==
            (guest1.id, guest1.name, guest1.hotel_id)
        )
        guest = Guest.find_by_name(guest2.name)
        assert (
            (guest.id, guest.name, guest.hotel_id) ==
            (guest2.id, guest2.name, guest2.hotel_id)
        )
        guest = Guest.find_by_name("Unknown")
        assert (guest is None)

    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns a Guest instance corresponding to its db row retrieved by id.'''

        Hotel.create_table()
        hotel = Hotel("The Moxy Hotel", "Soho")
        hotel.save()
        Guest.create_table()
        faker = Faker()
        guest1 = Guest.create(faker.name(), hotel.id)
        guest2 = Guest.create(
            faker.name(), hotel.id)

        guest = Guest.find_by_id(guest1.id)
        assert (
            (guest.id, guest.name, guest.hotel_id) ==
            (guest1.id, guest1.name, guest1.hotel_id)
        )

        guest = Guest.find_by_id(guest2.id)
        assert (
            (guest.id, guest.name, guest.hotel_id) ==
            (guest2.id, guest2.name,guest2.hotel_id)
        )

        guest = Guest.find_by_id(3)
        assert (guest is None)