import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users,
    get_available_listings, 
    get_all_games, 
    create_game,
    delist_game,
    get_all_listings, 
    get_user_listings, 
    list_game,
    create_rental,
    get_outstanding_rentals,
    return_rental,
    get_outstanding_user_rentals 
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

'''
Generic Commands
'''

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())


@user_cli.command("games", help="Shows the game listings of a user")
def list_user__games_command():
    print(get_all_users())
    userId = input('Enter a userId: ')
    print(get_user_listings(userId))


app.cli.add_command(user_cli) # add the group to the cli

'''
Game Commands
'''

game_cli = AppGroup('game', help='Game object commands') 

@game_cli.command("list", help="Lists the games in the database")
def get_games():
    print(get_all_games())

@game_cli.command("create", help="Creates a game")
@click.argument("title") #can be customized to accept genre, platform etc
def make_game(title):
    create_game(title)
    print('Game Created')

app.cli.add_command(game_cli)


'''
Listing Commands
'''

list_cli = AppGroup('listing', help='Game Listing commands') 

@list_cli.command("list", help="Lists the available listings in the database")
def get_listings_command():
    print(get_available_listings(None))

@list_cli.command("create", help="Lets a user list a game for rental")
def list_game_command():
    print(get_all_users())
    userId = input('Enter a userId: ')
    print(get_all_games())
    gameId = input('Enter a gameId: ')
    res = list_game(userId, gameId)
    if res:
        print('Game added to user!')
    else :
        print("error add game to user")

@list_cli.command("remove", help="Delists a game")
def delist_game_command():
    print(get_all_users())
    userId = input('Enter a userId: ')
    print(get_available_listings())
    listingId = input('Enter a listingId: ')
    res = delist_game(listingId, userId)
    if res:
        print('Game un listed')
    else :
        print("Error removing listing bad ID or unauthorized")

app.cli.add_command(list_cli)

'''
Rental Commands
'''

rental_cli = AppGroup('rental', help='Game Rental commands')

@rental_cli.command("list", help="Lists outstanding rentals")
def view_rentals_command():
    print(get_outstanding_rentals())

@rental_cli.command("create", help="Lets a user rent a game")
def rent_game_command():
    print(get_all_users())
    userId = input('Enter user Id: ')
    print(get_all_listings())
    listingId = input("Enter a listing Id: ")
    create_rental(userId, listingId)
    print("Rental created!")

@rental_cli.command("return", help="Lets a user return a game")
def return_game_command():
    print(get_all_users())
    userId = input('Enter user Id: ')
    print(get_outstanding_user_rentals(userId))
    rentalId = input("Enter a rental Id: ")
    res = return_rental(userId, rentalId)
    if res :
        print("rental returned!")
    else:
        print("Error, bad id or unauthorized")

app.cli.add_command(rental_cli)

'''
Game Commands
'''

game_cli = AppGroup('game', help='Game object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@game_cli.command("create", help="Creates a game")
@click.argument("title", default="frogger")
@click.argument("rating", default="teens")
@click.argument("platform", default="NSW")
@click.argument("boxart", default="https://image.com/pic.png")
@click.argument("genre", default="platform")
def create_game_command(title, rating, platform, boxart, genre):
    create_game(title, rating, platform, boxart, genre)
    print(f'{title} created!')

@game_cli.command("list", help="Lists games in the database")
def list_game_command():
    print(get_all_games())


app.cli.add_command(game_cli)
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
