#!/usr/bin/env python3
import click
from models.guest import *
from models.hotel import *
from helpers import *


clear_history_cli()

# @click.group()
# def cli():
#     '''When arguments for this function are empty, as a click.group it will invoke the 'menu' command within this group.'''
#     pass

def clear_screen(message_to_terminal=None, clear_history=True):
    
    '''Decorator to handle the post function notification to user via CLI.'''
    def wrapper(func):
    
        def inner_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            clear_history_cli() if clear_history else None
            styled_dashes_text(message_to_terminal) if message_to_terminal else None
            click.echo(result) if result else None
            menu()
        
        return inner_wrapper
        
    return wrapper


def menu():
    """Display a menu of options."""

    choice = display_menu()
    if choice == '1':
        create_hotel()
    elif choice == '2':
        update_hotel()
    elif choice == '3':
        delete_hotel()
    elif choice == '4':
        display_all_hotels()
    elif choice == '5':
        search_hotel_by_name()
    elif choice == '6':
        search_hotel_by_id()
    elif choice == '7':
        create_guest()
    elif choice == '8':
        update_guest()
    elif choice == '9':
        delete_guest()
    elif choice == '10':
        search_for_guest_by_id()
    elif choice == '11':
        search_for_guest_by_name()
    elif choice == '12':
        display_all_guests()
    elif choice == '13':
        search_for_guests_from_one_hotel()
    elif choice == '14':
        search_for_guests_by_name_length()
    elif choice == '15':
        exit_program()

@clear_screen("New Hotel Created")
def create_hotel(name=None, location=None):
    """Create a new hotel."""   
    styled_dashes_text("Creating a hotel")
    ascii_symbols("hotel")
    hotel_name = click.prompt("\nEnter the name of the hotel", type=str) if name == None else name
    hotel_location = click.prompt("Location of the hotel", type=str) if location == None else location
    return Hotel.create(hotel_name, hotel_location)
    
@clear_screen("Hotel Updated")
def update_hotel(id: int = None, name:str = None, location: str = None):
    """Update an existing hotel."""
    styled_dashes_text("Updating a hotel")
    print(all_hotels_in_db()) if id == None else None
    hotel_selected = Hotel.find_by_id(click.prompt("\nEnter the hotel id from the list of available hotels above", type=int)) if id == None else Hotel.find_by_id(int(id))
    while hotel_selected not in Hotel.get_all():
        click.echo("That hotel is not in our db. Please re-enter the id for an existing hotel")
        hotel_selected = Hotel.find_by_id(click.prompt("\nEnter the hotel id from the list of available hotels above", type=int)) if id == None else Hotel.find_by_id(int(id))
    click.echo(f"Hotel Selected: {hotel_selected}") if name == None else None
    new_hotel_name = input(f"\nEnter the new name for the Hotel selected: {hotel_selected}: ") if name == None else name
    new_hotel_location = input(f"\nEnter the new location for the Hotel selected: {hotel_selected}: ") if location == None else location
    return hotel_selected.update(new_hotel_name, new_hotel_location)

@clear_screen("Hotel Deleted")
def delete_hotel(id:int = None):
    """Delete a hotel by ID."""
    styled_dashes_text("Deleting a hotel")
    print(all_hotels_in_db()) if id == None else None
    hotel_selected = Hotel.find_by_id(click.prompt("\nEnter the hotel id from the list of available hotels above", type=int)) if id == None else Hotel.find_by_id(int(id))
    return hotel_selected.delete()

@clear_screen("Displaying All Hotels")
def display_all_hotels():
    """Display all hotels."""
    styled_dashes_text("Displaying all hotels")
    return all_hotels_in_db()  

@clear_screen("Found Entries For Hotel Searched By Name", True)        
def search_hotel_by_name(name=None):
    """Search for a hotel by name via fuzzy search"""
    print(all_hotels_in_db())
    hotel_name_to_search = click.prompt("\nEnter the name of the hotel to search") if name == None else name
    hotel_matches = ""
    for index, entry in enumerate(fuzzy_match(hotel_name_to_search, Hotel.get_all())):
        hotel_matches += f"{index+1}. {entry}\n"
    return hotel_matches
    
@clear_screen("Found Entry For Hotel Searched By ID")
def search_hotel_by_id(id):
    """Search for a hotel by ID"""
    print(all_hotels_in_db())
    return Hotel.find_by_id(click.prompt("\nEnter the ID of the hotel to search", type=int)) if id == None else Hotel.find_by_id(int(id))

@clear_screen("Created A New Guest")
def create_guest(id=None, name=None):
    """Create a new guest."""    
    styled_dashes_text("Creating a guest")
    print(all_hotels_in_db(), end="\n\n") if id == None else None
    guest_hotel_id = click.prompt("Enter the ID of the hotel the guest is staying at", type=int) if id == None else int(id)
    if not Guest.find_by_id(guest_hotel_id):
        print("That hotel ID is not available. Please try again")
        guest_hotel_id = click.prompt("Enter the ID of the hotel the guest is staying at", type=int)
    guest_name = click.prompt("\nEnter the name of the guest", type=str) if name == None else name
    return Guest.create(guest_name, guest_hotel_id)

@clear_screen("Updated A Guest")
def update_guest(gid:int=None, hid:int=None, name:str=None):
    """Update an existing guest."""
    styled_dashes_text("Updating A Guest")
    print(all_guests_in_db(), end="\n\n") if gid == None else None
    guest = Guest.find_by_id(click.prompt("Enter the ID of the guest you want to update", type=int)) if hid == None else Guest.find_by_id(int(hid))
    while guest not in Guest.get_all():
        click.echo("\nThat guest ID is not in our db. Please enter an existing guest ID from the list of guests above.")
        guest = Guest.find_by_id(click.prompt("Enter the ID of the guest you want to update", type=int)) 
    guest_name = click.prompt("\nEnter the updated name of the guest", type=str) if name == None else name
    print(all_hotels_in_db(), end="\n\n") if hid == None else None
    guest_hotel_id = click.prompt("\nEnter the updated ID of the hotel our guest is staying at", type=int) if hid == None else int(hid)
    found_hotel = Hotel.find_by_id(guest_hotel_id)
    while found_hotel not in Hotel.get_all():
        click.echo("\nThat hotel is not in our db. Please enter a hotel ID from the list of hotels above.")
        guest_hotel_id = click.prompt("Enter the ID of the hotel you are looking for", type=int) 
        found_hotel = Hotel.find_by_id(guest_hotel_id)
    return guest.update(guest_name, guest_hotel_id)

@clear_screen("Deleted A Guest")
def delete_guest(id=None):
    """Delete a guest."""
    styled_dashes_text("Deleting A Guest")
    print(all_guests_in_db(), end="\n\n") if id == None else None
    guest_search = click.prompt("Enter the ID of the guest you want to delete", type=int) if id == None else Guest.find_by_id(int(id))
    found_guest = Guest.find_by_id(guest_search)
    while found_guest not in Guest.get_all():
        click.echo("\nThat guest is not in our db. Please enter a guest ID from the list of guests above.")
        guest_search = click.prompt("Enter the ID of the guest you want to delete", type=int)
        found_guest = Guest.find_by_id(guest_search)
    return found_guest if found_guest != None else f"No results found for {guest_search}"

@clear_screen("Displaying All Guests")
def display_all_guests():
    """Display all guests."""
    styled_dashes_text("Displaying all hotels")
    return all_guests_in_db()

@clear_screen("Found Entry For Guest Searched By ID")
def search_for_guest_by_id(id=None):
    """Search for a guest."""
    styled_dashes_text("Searching A Guest By ID")
    print(all_guests_in_db(), end="\n\n")
    guest_search = click.prompt("Enter the ID of the guest you are searching for", type=int) if id == None else Guest.find_by_id(int(id))
    found_guest = Guest.find_by_id(guest_search)
    while found_guest not in Guest.get_all():
        click.echo("\nThat guest is not in our db. Please enter a guest ID from the list of guests above.")
        guest_search = click.prompt("Enter the name of the guest you are searching for", type=int)
        found_guest = Guest.find_by_id(guest_search)
    return found_guest if found_guest != None else f"No result found for {guest_search}"

@clear_screen("Found Entries For Guest Searched By Name")
def search_for_guest_by_name(name=None):
    """Search for a guest by name via fuzzy search."""
    styled_dashes_text("Searching A Guest By Name")
    print(all_guests_in_db())
    guest_name_to_search = input("\nEnter the name of the guest: ") if name == None else name
    guest_matches = ""
    for index, entry in enumerate(fuzzy_match(guest_name_to_search, Guest.get_all())):
        guest_matches += f"{index+1}. {entry}\n"
    return guest_matches if len(guest_matches) > 0 else "No guests found by that name"

@clear_screen("Found Entries For Guests Within One Hotel")
def search_for_guests_from_one_hotel(id:int=None):
    """Displays all guests for a single hotel """
    styled_dashes_text("Displaying All Guests Within One Hotel")
    print(all_hotels_in_db())
    hotel = Hotel.find_by_id(click.prompt("\nSelect the hotel by ID to check their guest list", type=int)) if id == None else int(id)
    guest_matches = ""
    for index, entry in enumerate(hotel.guests()):
        guest_matches += f"{index+1}. {entry}\n"
    return guest_matches if len(guest_matches) > 0 else "No guests found for this hotel"

@clear_screen("Found Entries For Guests With Selected Name Length")
def search_for_guests_by_name_length(length:int=None):
    """Displays all guests whose name is equal to or less than length"""
    styled_dashes_text("Displaying All Guests With Specific Name Length")
    print(all_guests_in_db())
    guest_name_length = click.prompt("\nEnter the name length to search guest names by", type=int) if length == None else int(length)
    guest_matches = ""
    for index, entry in enumerate(Guest.find_by_name_length(guest_name_length)):
        guest_matches += f"{index+1}. {entry}\n"
    return guest_matches if len(guest_matches) > 0 else "No guests found for this length"