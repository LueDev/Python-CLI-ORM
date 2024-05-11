from models.__init__ import CURSOR, CONN 

class Hotel:
    
    all = {}
    
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name 
        self.location = location 
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Hotel name must be a string and can't be blank")
        
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, location):
        if isinstance(location, str) and len(location) > 0:
            self._location = location
        else:
            raise ValueError("Hotel location must be a string and can't be blank")
            
        
    def __repr__(self):
        return (
            f"<Hotel {self.id}: {self.name} @{self.location}>"
        )
    
    def __str__(self):
        return (
            f"<Hotel {self.id}: {self.name} @{self.location}>"
        )
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Hotel instances """
        sql = """
            CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Hotel instances """
        sql = """
            DROP TABLE IF EXISTS hotels;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Hotel instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO hotels (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        """ Initialize a new Hotel instance and save the object to the database """
        hotel = cls(name, location)
        hotel.save()
        return hotel

    def update(self, name, location):
        """Update the table row corresponding to the current Hotel instance."""
        sql = """
            UPDATE hotels
            SET name = ?, location = ?
            WHERE id = ?
        """
        self.name = name
        self.location = location 
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()
        return self

    def delete(self):
        """Delete the table row corresponding to the current Hotel instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM hotels
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None
        
        return self

    @classmethod
    def instance_from_db(cls, row):
        """Return a Hotel object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        hotel = cls.all.get(row[0])
        if hotel:
            # ensure attributes match row values in case local instance was modified
            hotel.name = row[1]
            hotel.location = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            hotel = cls(row[1], row[2])
            hotel.id = row[0]
            cls.all[hotel.id] = hotel
        return hotel

    @classmethod
    def get_all(cls):
        """Return a list containing a Hotel object per row in the table"""
        sql = """
            SELECT *
            FROM hotels
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Hotel object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM hotels
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return a Hotel object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM hotels
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def guests(self):
        """Return list of guests associated with current hotel"""
        from models.guest import Guest
        sql = """
            SELECT * FROM guests
            WHERE hotel_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [Guest.instance_from_db(row) for row in rows]