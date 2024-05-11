#!/usr/bin/env python3

import click
from models.guest import *
from models.hotel import *
import os
from helpers import *
import time

clear_history_cli()

@click.group()
def cli():
    '''When arguments for this function are empty, as a click.group it will invoke the 'menu' command within this group.'''
    pass

def clear_screen(message_to_terminal=None, clear_history=True):
    
    '''Decorator to handle the post function notification to user via CLI.'''
    def wrapper(func):
    
        @click.pass_context
        def inner_wrapper(ctx, *args, **kwargs):
            result = func(*args, **kwargs)
            clear_history_cli() if clear_history else None
            styled_dashes_text(message_to_terminal) if message_to_terminal else None
            click.echo(result) if result else None
            ctx.invoke(menu)
        
        return inner_wrapper
        
    return wrapper

@cli.command()
@click.pass_context
def menu(ctx):
    """Display a menu of options."""

    choice = display_menu()
    if choice == '1':
        ctx.invoke(create_hotel)
    elif choice == '2':
        ctx.invoke(update_hotel)
    elif choice == '3':
        ctx.invoke(delete_hotel)
    elif choice == '4':
        ctx.invoke(display_all_hotels)
    elif choice == '5':
        ctx.invoke(search_hotel_by_name)
    elif choice == '6':
        ctx.invoke(search_hotel_by_id)    
    elif choice == '7':
        ctx.invoke(create_guest)
    elif choice == '8':
        ctx.invoke(update_guest)
    elif choice == '9':
        ctx.invoke(delete_guest)
    elif choice == '10':
        ctx.invoke(search_for_guest_by_id)
    elif choice == '11':
        ctx.invoke(search_for_guest_by_name)
    elif choice == '12':
        ctx.invoke(display_all_guests)
    elif choice == '13':
        ctx.invoke(search_for_guests_within_one_hotel)
    elif choice == '14':
        exit_program()

# @clear_screen("New Hotel Created")
@cli.command()
@click.option('--name', default=None, help='Name of hotel.')
@click.option('--location', default=None, help='Location of hotel.')
def create_hotel(name=None, location=None):
    """Create a new hotel."""
    styled_dashes_text("Creating a hotel")
    ascii_symbols("hotel")
    hotel_name = click.prompt("\nEnter the name of the hotel", type=str) if name == None else name
    hotel_location = click.prompt("Location of the hotel", type=str) if location == None else location
    return Hotel.create(hotel_name, hotel_location)
    
    
@cli.command()
@clear_screen("Hotel Updated")
def update_hotel():
    """Update an existing hotel."""
    styled_dashes_text("Updating a hotel")
    
    for hotel in Hotel.get_all():
        print(hotel)
    hotel_selected = Hotel.find_by_id(click.prompt("\nEnter the hotel id from the list of available hotels above", type=int))
    click.echo(f"Hotel Selected: {hotel_selected}")
    new_hotel_name = input(f"\nEnter the new name for the Hotel selected: {hotel_selected}: ")
    new_hotel_location = input(f"\nEnter the new location for the Hotel selected: {hotel_selected}: ")
    return hotel_selected.update(new_hotel_name, new_hotel_location)
    
@cli.command()
@clear_screen("Hotel Deleted")
def delete_hotel():
    """Delete a hotel by ID."""
    styled_dashes_text("Deleting a hotel")
    for hotel in Hotel.get_all():
            print(hotel)
    hotel_selected = Hotel.find_by_id(click.prompt("\nEnter the hotel id from the list of available hotels above", type=int))
    return hotel_selected.delete()


@cli.command()
@clear_screen("Displaying All Hotels")
def display_all_hotels():
    """Display all hotels."""
    styled_dashes_text("Displaying all hotels")
    return all_hotels_in_db()      
        
@cli.command()
@clear_screen("Found Entries For Hotel Searched By Name", True)
def search_hotel_by_name():
    """Search for a hotel by name via fuzzy search"""
    hotel_name_to_search = click.prompt("\nEnter the name of the hotel to search")
    hotel_matches = ""
    for index, entry in enumerate(fuzzy_match(hotel_name_to_search, Hotel.get_all())):
        hotel_matches += f"{index+1}. {entry}\n"
    return hotel_matches
    
@cli.command()
@clear_screen("Found Entry For Hotel Searched By ID")
def search_hotel_by_id():
    """Search for a hotel by ID"""
    return Hotel.find_by_id(click.prompt("\nEnter the ID of the hotel to search", type=int))

@cli.command()
@clear_screen("Created A New Guest")
def create_guest():
    """Create a new guest."""
    styled_dashes_text("Creating a guest")
    print(all_hotels_in_db(), end="\n\n")
    guest_hotel_id = click.prompt("Enter the ID of the hotel, the guest is staying at", type=int)
    guest_name = click.prompt("\nEnter the name of the guest", type=str)
    return Guest.create(guest_name, guest_hotel_id)


@cli.command()
@clear_screen("Updated A Guest")
def update_guest():
    """Update an existing guest."""
    styled_dashes_text("Updating A Guest")
    print(all_guests_in_db(), end="\n\n")
    guest = Guest.find_by_id(click.prompt("Enter the ID of the guest you want to update", type=int))
    guest_name = click.prompt("\nEnter the updated name of the guest", type=str)
    print(all_hotels_in_db(), end="\n\n")
    guest_hotel_id = click.prompt("\nEnter the updated ID of the hotel our guest is staying at", type=int)
    return guest.update(guest_name, guest_hotel_id)


@cli.command()
@clear_screen("Deleted A Guest")
def delete_guest():
    """Delete a guest."""
    styled_dashes_text("Deleting A Guest")
    print(all_guests_in_db(), end="\n\n")
    guest = Guest.find_by_id(click.prompt("Enter the ID of the guest you want to delete", type=int))
    guest.delete()
    return guest

@cli.command()
@clear_screen("Displaying All Guests")
def display_all_guests():
    """Display all hotels."""
    styled_dashes_text("Displaying all hotels")
    return all_guests_in_db()

@cli.command()
@clear_screen("Found Entry For Guest Searched By ID")
def search_for_guest_by_id():
    """Search for a guest."""
    styled_dashes_text("Searching A Guest By ID")
    print(all_guests_in_db(), end="\n\n")
    guest = Guest.find_by_id(click.prompt("Enter the ID of the guest you are searching for", type=int))
    return guest

@cli.command()
@clear_screen("Found Entries For Guest Searched By Name")
def search_for_guest_by_name():
    """Search for a guest by name via fuzzy search."""
    styled_dashes_text("Searching A Guest By Name")
    guest_name_to_search = input("\nEnter the name of the guest: ")
    guest_matches = ""
    for index, entry in enumerate(fuzzy_match(guest_name_to_search, Guest.get_all())):
        guest_matches += f"{index+1}. {entry}\n"
    return guest_matches

@cli.command()
@clear_screen("Found Entries For Guests Within One Hotel")
def search_for_guests_within_one_hotel():
    """Displays all guests for a single hotel """
    styled_dashes_text("Displaying All Guests Within One Hotel")
    print(all_hotels_in_db())
    hotel = Hotel.find_by_id(click.prompt("\nSelect the hotel to check their guest list", type=int))
    guest_matches = ""
    for index, entry in enumerate(hotel.guests()):
        guest_matches += f"{index+1}. {entry}\n"
    return guest_matches

if __name__ == "__main__":
    cli()


