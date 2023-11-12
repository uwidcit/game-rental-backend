import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate, db
from App.main import create_app
from App.controllers import ( 

    get_all_customers,
    get_all_staff,
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
    get_outstanding_user_rentals,
    cache_api_games,
    get_listing,
    get_staff,
    create_customer,
    create_staff,
    get_customer,
    get_rental,
    get_game
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
    db.drop_all()
    create_db(app)
    bob = create_staff("bob", "bobpass")
    rob = create_customer("rob", "robpass")
    jane = create_customer("jane", "janepass")
    # create a list of games
    games = [
        create_game("Frogger", "Everyone", "NSW", "https://image.com/pic.png", "Platform"),
        create_game("Mario", "Everyone", "NSW", "https://image.com/pic.png", "Platform"),
        create_game("Zelda", "Everyone", "NSW", "https://image.com/pic.png", "Adventure"),
        create_game("Pokemon", "Everyone", "NSW", "https://image.com/pic.png", "RPG"),
        create_game("Sonic", "Everyone", "NSW", "https://image.com/pic.png", "Platform"),
        create_game("Fortnite", "Teen", "NSW", "https://image.com/pic.png", "Shooter"),
        create_game("COD", "Teen", "NSW", "https://image.com/pic.png", "Shooter"),
    ]
    db.session.add_all(games)

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

'''
Customer Commands
'''

customer_cli = AppGroup('customer', help='Customer object commands')

# Then define the command and any parameters and annotate it with the group (@)
@customer_cli.command("create", help="Creates a customer")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_customer_command(username, password):
    new_customer = create_customer(username, password)
    print(new_customer)

@customer_cli.command("list", help="Lists the customers in the database")
def get_customers():
    print(get_all_customers())

app.cli.add_command(customer_cli)

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
    print(get_all_customers())
    userId = input('Enter a customerId: ')
    print(get_all_games())
    gameId = input('Enter a gameId: ')
    res = list_game(userId, gameId)
    if res:
        print('Game added to user!')
    else :
        print("error add game to user")

@list_cli.command("remove", help="Delists a game")
def delist_game_command():
    print(get_all_customers())
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
    print(get_all_customers())
    userId = input('Enter customer Id: ')
    print(get_all_listings())
    listingId = input("Enter a listing Id: ")
    create_rental(userId, listingId)
    print("Rental created!")

@rental_cli.command("return", help="Lets a user return a game")
def return_game_command():
    print(get_all_customers())
    userId = input('Enter customer Id: ')
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

@game_cli.command("load", help="Loads games from the api into the database")
@click.argument("page", default=1)
def load_game_command(page):
    games = cache_api_games(page)
    print(f"{len(games)} games loaded from API")
    


app.cli.add_command(game_cli)

'''
Staff Commands
'''

staff_cli = AppGroup('staff', help='Staff object commands')


@staff_cli.command("list-game", help="Lets a staff member list a game for rental")
@click.argument("staff_id", default=1)
@click.argument("customer_id", default=1)
@click.argument("game_id", default=1)
@click.argument("condition", default="good")
@click.argument("price", default=10.40)
def staff_list_game_command(staff_id, customer_id, game_id, condition, price):
    staff = get_staff(staff_id)
    customer = get_customer(customer_id)
    game = get_game(game_id)
    listing = staff.list_game(customer, game, condition, price)
    print(f"Game {game.title} listed by {staff.username} for ${price}")
    print(listing.toJSON_with_game())

app.cli.add_command(staff_cli)

@staff_cli.command("create", help="Creates a staff member")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def create_staff_command(username, password):
    new_staff = create_staff(username, password)
    print(new_staff)

@staff_cli.command("list", help="Lists the staff in the database")
def get_staff_command():
    print(get_all_staff())

@staff_cli.command("confirm-rental", help="Lets a staff member confirm a rental")
@click.argument("staff_id", default=1)
@click.argument("listing_id", default=1)
@click.argument("customer_id", default=1)
def confirm_rental_command(staff_id, listing_id, customer_id):
    staff = get_staff(staff_id)
    listing = get_listing(listing_id)
    renter = get_customer(customer_id)
    rental = staff.confirm_rental(renter, listing)
    if rental:
        print(f"Rental {rental.rentalId} confirmed by {staff.username}")
    else:
        print("Error confirming rental")

@staff_cli.command("confirm-return", help="Lets a staff member confirm a return")
@click.argument("staff_id", default=1)
@click.argument("rental_id", default=1)
def confirm_return_command(staff_id, rental_id):
    staff = get_staff(staff_id)
    rental = get_rental(rental_id)
    fees = staff.confirm_return(rental)
    if fees == None:
        print("Error returning rental")
    else:
        print(f"Rental {rental.rentalId} returned by {staff.username} with fees of ${fees}")

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
