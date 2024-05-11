from models.hotel import Hotel
from models.guest import Guest
import pytest


class TestGuestProperties:
    '''Class Guest in guest.py'''

    @pytest.fixture(autouse=True)
    def reset_db(self):
        '''drop and recreate tables prior to each test.'''
        Guest.drop_table()
        Hotel.drop_table()
        Guest.create_table()
        Hotel.create_table()
        # clear the object cache
        Hotel.all = {}
        Guest.all = {}

    def test_name_hotel_valid(self):
        '''validates name and hotel id are valid'''
        # should not raise exception
        hotel = Hotel.create("The Winston", "228 Slick Road")
        guest = Guest.create("Lee", hotel.id)

    def test_name_is_string(self):
        '''validates name property is assigned a string'''
        with pytest.raises(ValueError):
            hotel = Hotel.create("The Gerald", "211 Slick Road")
            guest = Guest.create("Lee", hotel.id)
            guest.name = 7

    def test_name_string_length(self):
        '''validates name property length > 0'''
        with pytest.raises(ValueError):
            hotel = Hotel.create("The Phil", "128 Slick Road")
            guest = Guest.create("Lee", hotel.id)
            guest.name = ''


    def test_hotel_property(self):
        hotel = Hotel.create("The Churchill", "Winston Churchil Land")
        guest = Guest.create(
            "Raha", hotel.id)  # no exception

    def test_hotel_property_fk(self):
        with pytest.raises(ValueError):
            guest = Guest.create("Raha", 7000)

    def test_hotel_property_type(self):
        with pytest.raises(ValueError):
            guest = Guest.create("Raha", "abc")
