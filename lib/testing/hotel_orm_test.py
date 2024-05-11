from models.__init__ import CONN, CURSOR
from models.hotel import Hotel
import pytest


class TestHotel:
    '''Class Hotel in hotel.py'''

    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''drop tables prior to each test.'''

        CURSOR.execute("DROP TABLE IF EXISTS guests")
        CURSOR.execute("DROP TABLE IF EXISTS hotels")
        Hotel.all = {}

    def test_creates_table(self):
        '''contains method "create_table()" that creates table "hotels" if it does not exist.'''

        Hotel.create_table()
        assert (CURSOR.execute("SELECT * FROM hotels"))

    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "hotels" if it exists.'''

        sql = """
            CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

        Hotel.drop_table()

        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='hotels'
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result is None)

    def test_saves_hotel(self):
        '''contains method "save()" that saves a Hotel instance to the db and assigns the instance an id.'''

        Hotel.create_table()
        hotel = Hotel("Sonder", "828 Brittle Road")
        hotel.save()

        sql = """
            SELECT * FROM hotels
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (hotel.id, hotel.name, hotel.location) ==
                (row[0], "Sonder", "828 Brittle Road"))

    def test_creates_hotel(self):
        '''contains method "create()" that creates a new row in the db using parameter data and returns a Hotel instance.'''

        Hotel.create_table()
        hotel = Hotel.create("Sonder", "828 Brittle Road")

        sql = """
            SELECT * FROM hotels
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (hotel.id, hotel.name, hotel.location) ==
                (row[0], "Sonder", "828 Brittle Road"))

    def test_updates_row(self):
        '''contains a method "update()" that updates an instance's corresponding db row to match its new attribute values.'''
        Hotel.create_table()

        hotel1 = Hotel.create(
            "Jackal", "Jackal Lane")
        id1 = hotel1.id
        hotel2 = Hotel.create("Marketing", "Building B, 3rd Floor")
        id2 = hotel2.id

        # Assign new values for name and location
        hotel2.name = "Yao International"
        hotel2.location = "Pond near Verne"

        # Persist the updated name and location values
        hotel2.update(hotel2.name, hotel2.location)

        # assert hotel1 row was not updated, hotel1 object state not updated
        # assert row not updated
        hotel = Hotel.find_by_id(id1)
        assert ((hotel.id, hotel.name, hotel.location)
                == (id1, "Jackal", "Jackal Lane")
                == (hotel1.id, hotel1.name, hotel1.location))

        # assert hotel2 row was updated, hotel2 object state is correct
        hotel = Hotel.find_by_id(id2)
        assert ((hotel.id, hotel.name, hotel.location)
                == (id2, "Yao International", "Pond near Verne")
                == (hotel2.id, hotel2.name, hotel2.location))

    def test_deletes_row(self):
        '''contains a method "delete()" that deletes the instance's corresponding db row'''
        Hotel.create_table()

        hotel1 = Hotel.create(
            "Jackal", "Jackal Lane")
        id1 = hotel1.id
        hotel2 = Hotel.create(
            "Yao International", "Pond near Verne")
        id2 = hotel2.id

        hotel2.delete()

        # assert hotel1 row was not deleted, hotel1 object state is correct
        hotel = Hotel.find_by_id(id1)
        assert ((hotel.id, hotel.name, hotel.location)
                == (id1, "Jackal", "Jackal Lane")
                == (hotel1.id, hotel1.name, hotel1.location))

        # assert hotel2 row is deleted
        assert (Hotel.find_by_id(id2) is None)
        # assert hotel2 object state is correct, id should be None
        assert ((None, "Yao International", "Pond near Verne")
                == (hotel2.id, hotel2.name, hotel2.location))
        # assert dictionary entry was deleted
        assert (Hotel.all.get(id2) is None)

    def test_instance_from_db(self):
        '''contains method "instance_from_db()" that takes a table row and returns a Hotel instance.'''

        Hotel.create_table()
        Hotel.create("Sonder", "828 Brittle Road")

        sql = """
            SELECT * FROM hotels
        """
        row = CURSOR.execute(sql).fetchone()
        hotel = Hotel.instance_from_db(row)

        assert ((row[0], row[1], row[2]) ==
                (hotel.id, hotel.name, hotel.location) ==
                (row[0], "Sonder", "828 Brittle Road"))

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Hotel instances for every row in the db.'''

        Hotel.create_table()

        hotel1 = Hotel.create(
            "Jackal", "Jackal Lane")
        hotel2 = Hotel.create("Marketing", "Building B, 3rd Floor")

        hotels = Hotel.get_all()

        assert (len(hotels) == 2)
        assert (
            (hotels[0].id, hotels[0].name, hotels[0].location) ==
            (hotel1.id, "Jackal", "Jackal Lane"))
        assert ((hotels[1].id, hotels[1].name, hotels[1].location) ==
                (hotel2.id, "Marketing", "Building B, 3rd Floor")
                )

    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns a Hotel instance corresponding to the db row retrieved by id.'''

        Hotel.create_table()
        hotel1 = Hotel.create(
            "Jackal", "Jackal Lane")
        hotel2 = Hotel.create("Marketing", "Building B, 3rd Floor")

        hotel = Hotel.find_by_id(hotel1.id)
        assert (
            (hotel.id, hotel.name, hotel.location) ==
            (hotel1.id, "Jackal", "Jackal Lane")
        )
        hotel = Hotel.find_by_id(hotel2.id)
        assert (
            (hotel.id, hotel.name, hotel.location) ==
            (hotel2.id, "Marketing", "Building B, 3rd Floor")
        )
        hotel = Hotel.find_by_id(0)
        assert (hotel is None)

    def test_finds_by_name(self):
        '''contains method "find_by_name()" that returns a Hotel instance corresponding to the db row retrieved by name.'''

        Hotel.create_table()
        hotel1 = Hotel.create(
            "Jackal", "Jackal Lane")
        hotel2 = Hotel.create("Marketing", "Building B, 3rd Floor")

        hotel = Hotel.find_by_name("Jackal")
        assert (
            (hotel.id, hotel.name, hotel.location) ==
            (hotel1.id, "Jackal", "Jackal Lane")
        )

        hotel = Hotel.find_by_name("Marketing")
        assert (
            (hotel.id, hotel.name, hotel.location) ==
            (hotel2.id, "Marketing", "Building B, 3rd Floor")
        )
        hotel = Hotel.find_by_name("Unknown")
        assert (hotel is None)

    def test_get_guests(self):
        '''contain a method "guests" that gets the guests for the current Hotel instance '''

        from models.guest import Guest  # avoid circular import issue
        Guest.all = {}

        Hotel.create_table()
        hotel1 = Hotel.create("Sonder", "828 Brittle Road")
        hotel2 = Hotel.create(
            "Jackal", "Building C, 2nd Floor")

        Guest.create_table()
        guest1 = Guest.create("Raha", hotel1.id)
        guest2 = Guest.create("Tal", hotel1.id)
        guest3 = Guest.create("Amir", hotel2.id)

        guests = hotel1.guests()
        assert (len(guests) == 2)
        assert ((guests[0].id, guests[0].name, guests[0].hotel_id) ==
                (guest1.id, guest1.name, guest1.hotel_id))
        assert ((guests[1].id, guests[1].name, guests[1].hotel_id) ==
                (guest2.id, guest2.name, guest2.hotel_id))