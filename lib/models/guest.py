from models.__init__ import CURSOR, CONN 
from models.hotel import Hotel

class Guest:
    
    all = {}
    
    def __init__(self, name, hotel_id, id=None):
        self.id = id
        self.name = name 
        self.hotel_id = hotel_id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name can't be blank and must be type string")
        
    @property
    def hotel_id(self):
        return self._hotel_id
    
    @hotel_id.setter
    def hotel_id(self, hotel_id):
        if isinstance(hotel_id, int) and Hotel.find_by_id(hotel_id):
            self._hotel_id = hotel_id
        else: 
            raise ValueError("Hotel ID must reference a hotel in the database. Create the hotel first.")
        
    def __repr__(self):
        return (
            f"<Guest {self.id}: {self.name}> -- "
            f"{Hotel.find_by_id(self.hotel_id)}"
        )
    
    def __str__(self):
        return (
            f"<Guest {self.id}: {self.name}> -- "
            f"{Hotel.find_by_id(self.hotel_id)}"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Employee instances """
        sql = """
            CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY,
            name TEXT,
            hotel_id INT,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Employee instances """
        sql = """
            DROP TABLE IF EXISTS guests;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, job title, and department id values of the current Employee object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO guests (name, hotel_id)
                VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.hotel_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self, name, hotel_id):
        """Update the table row corresponding to the current Employee instance."""
        sql = """
            UPDATE guests
            SET name = ?, hotel_id = ?
            WHERE id = ?
        """
        self.name = name
        self.hotel_id = hotel_id
        CURSOR.execute(sql, (self.name, self.hotel_id, self.id))
        CONN.commit()
        return self

    def delete(self):
        """Delete the table row corresponding to the current Employee instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM guests
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None
        

    @classmethod
    def create(cls, name, hotel_id):
        """ Initialize a new Employee instance and save the object to the database """
        guest = cls(name, hotel_id)
        guest.save()
        return guest

    @classmethod
    def instance_from_db(cls, row):
        """Return an Employee object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        guest = cls.all.get(row[0])
        if guest:
            # ensure attributes match row values in case local instance was modified
            guest.name = row[1]
            guest.hotel_id= row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            guest = cls(row[1], row[2])
            guest.id = row[0]
            cls.all[guest.id] = guest
        return guest

    @classmethod
    def get_all(cls):
        """Return a list containing one Employee object per table row"""
        sql = """
            SELECT *
            FROM guests
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Employee object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM guests
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return Employee object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM guests
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name_length(cls, length):
        """Return a list of guests whose name length is less than or equal to the length parameter"""

        return [guest for guest in cls.get_all() if len(guest.name) <= length]