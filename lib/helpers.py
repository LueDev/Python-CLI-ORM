# lib/helpers.py

import click
import regex
from models.guest import Guest
from models.hotel import Hotel
import os 

# Clear the terminal screen
def clear_history_cli():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    """Display a menu of options."""
    click.echo("\nMenu:")
    click.echo("1. Create a hotel")
    click.echo("2. Update a hotel")
    click.echo("3. Delete a hotel")
    click.echo("4. Display all hotels")
    click.echo("5. Search for a hotel by name")
    click.echo("6. Search for a hotel by ID")
    click.echo("7. Create a guest")
    click.echo("8. Update a guest")
    click.echo("9. Delete a guest")
    click.echo("10. Search for a guest by ID")
    click.echo("11. Search for a guest by Name")
    click.echo("12. Display all guests")
    click.echo("13. Display all guests within one hotel")
    click.echo("14. Exit Program")
    
    choice = input("\nEnter your choice: ")
    return choice

def all_hotels_in_db():
    all_hotels = ""
    for hotel in Hotel.get_all():
        all_hotels = all_hotels + "\n" + str(hotel) 
    return all_hotels  

def all_guests_in_db():
    all_hotels = ""
    for hotel in Guest.get_all():
        all_hotels = all_hotels + "\n" + str(hotel) 
    return all_hotels  

def fuzzy_match(user_input, database):
    results = []
    
    pattern_string = f"{user_input}"  
    pattern = regex.compile(pattern_string)

    for entry in database:
        name = entry.name  
        match = pattern.search(name)
        if match: 
            results.append(entry) 
    return results

def ascii_symbols(ascii_art):
    if ascii_art == "hotel":
        print('''
    
                  )
             (      _[]_         (
     __[]___[]___[]/____\_[]_    )
    /______________|[][]|____\  (
    |[][]|[][]|[][]|[][]|[][]|__[]_
    |  /\|/\  |  /\|  /\|/\  |_____|
    |[]|||||[]|[]|||[]|||||[]|[_]|||
  ===================================
  -  -  -  -  -  -  -  -  -  -  -  -  -
=========================================
    ''')
    
    
    
# Helper functions for styling output
def styled_dashes_text(text):
    # Calculate the length of the text
    text_length = len(text)
    
    # Calculate the number of dashes needed on each side
    dashes_needed = (50 - text_length) // 2
    
    # Create a string of dashes
    dashes = '-' * dashes_needed
    
    # Add space before and after the text
    styled_text = f"\n\n{dashes} {text} {dashes}\n"
    
    print(styled_text)

def exit_program():
    print("Goodbye!")
    exit()
