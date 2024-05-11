from models.hotel import Hotel
import pytest



class TestHotelProperties:
    '''Class Hotel in hotel.py'''

    @pytest.fixture(autouse=True)
    def clear_dictionary(self):
        '''clear out the class dictionary.'''
        Hotel.all = {}

    def test_name_location_valid(self):
        '''validates name and location assigned valid non-empty strings'''
        # should not throw an exception
        hotel = Hotel("Jordan's Villa", "Miami Beach")

    def test_name_is_string(self):
        '''validates name property is assigned a string'''
        with pytest.raises(ValueError):
            hotel = Hotel("Pippens' Villa", "South Beach")
            hotel.name = 7

    def test_name_string_length(self):
        '''validates name property length > 0'''
        with pytest.raises(ValueError):
            hotel = Hotel("Jamaican Gardens", "Jamaica")
            hotel.name = ''

    def test_location_is_string(self):
        '''validates location property is assigned a string'''
        with pytest.raises(ValueError):
            hotel = Hotel("Lux", "Los Angeles")
            hotel.location = True

    def test_location_string_length(self):
        '''validates location property length > 0'''
        with pytest.raises(ValueError):
            hotel = Hotel("King Kai's House", "The clouds")
            hotel.name = ''
