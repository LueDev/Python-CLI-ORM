#!/usr/bin/env python3
import commands
import click

@click.group()
def cli():
    '''When arguments for this function are empty, as a click.group it will invoke the 'menu' command within this group.'''
    pass

@cli.command()
def menu():
    commands.menu()
    
@cli.command()
@click.option('--name', default=None, help='Name of hotel.')
@click.option('--location', default=None, help='Location of hotel.')
def create_hotel(name=None, location=None):
    """Create a new hotel."""
    commands.create_hotel(name, location)
    
@cli.command()
@click.option('--id', default=None, help='Updated name of hotel.')
@click.option('--location', default=None, help='Updated location of hotel.')
def update_hotel(id: int = None, name:str = None, location: str = None):
    """Update an existing hotel."""
    commands.update_hotel(id, name, location)

@cli.command()
@click.option('--id', default=None, help='ID of hotel to delete.')
def delete_hotel(id:int = None):
    """Delete a hotel by ID."""
    commands.delete_hotel(id)

@cli.command()
def display_all_hotels():
    """Display all hotels."""
    commands.display_all_hotels()
    
@cli.command()
@click.option('--name', default=None, help='Name of hotel name to search.')
def search_hotel_by_name(name=None):
    """Search for a hotel by name via fuzzy search"""
    commands.search_hotel_by_name(name)
    
@cli.command()
@click.option('--id', default=None, help='ID of hotel name to search.')
def search_hotel_by_id(id=None):
    """Search for a hotel by ID"""
    commands.search_hotel_by_id(id)
    
@cli.command()
@click.option('--id', default=None, help='ID of hotel new guest will be staying at.')
@click.option('--name', default=None, help='Name of new guest.')
def create_guest(id=None, name=None):
    """Create a new guest."""
    commands.create_guest(id, name)

@cli.command()
@click.option('--gid', default=None, help='ID of Guest to update.')
@click.option('--hid', default=None, help='ID of updated Hotel guest will stay at.')
@click.option('--name', default=None, help='Updated name of new guest.')
def update_guest(gid:int=None, hid:int=None, name:str=None):
    """Update an existing guest."""
    commands.update_guest(gid, hid, name)

@cli.command()
@click.option('--id', default=None, help='ID of Guest to delete.')
def delete_guest(id=None):
    """Delete a guest."""
    commands.delete_guest(id)
    
@cli.command()
def display_all_guests():
    """Display all guests."""
    commands.display_all_hotels()

@cli.command()
@click.option('--id', default=None, help='ID of Guest to find.')
def search_for_guest_by_id(id=None):
    """Search for a guest."""
    commands.search_for_guest_by_id(id)
    
@cli.command()
@click.option('--name', default=None, help='Name of Guest to find.')
def search_for_guest_by_name(name=None):
    """Search for a guest by name via fuzzy search."""
    commands.search_for_guest_by_name(name)
    
@cli.command()
@click.option('--id', default=None, help='ID of hotel to return all guests from')
def search_for_guests_from_one_hotel(id:int=None):
    """Displays all guests for a single hotel """
    commands.search_for_guests_from_one_hotel(id)

@cli.command()
@click.option('--length', default=None, help='length of guest name')
def search_for_guests_by_name_length(length:int=None):
    """Displays all guests whose name is equal to or less than length"""
    commands.search_for_guests_by_name_length(length)

if __name__ == "__main__":
    cli()