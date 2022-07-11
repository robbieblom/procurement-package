import sqlite3
import csv
from Owner import Owner


def create_db(file_name):
    """Creates a local SQLite database using the sqlite3 module and then creates a table called
    Inventory in the database. The table should be populated from a csv file. There will be three
    columns: item_name, Price, and Quantity. The composite key of the table will be (item_name, value).
    Price and Quantity will both be stored as integers in the database.

    Parameters:
    file_name: String -- the name of the csv file that contains the inventory

    Return:
    a connection the the created database
    """
    db = sqlite3.connect("Inventory.db")
    curs = db.cursor()
    csvin = csv.reader(open(file_name))
    curs.execute('''CREATE TABLE if not exists Inventory (
                'Item Name' text check('Item Name' != ""),
                Value Integer not null,
                Quantity Integer not null,
                primary key ('Item Name', Value)
                ); ''')
    for i, row in enumerate(csvin):
        if i == 0:
            continue
        curs.execute('''insert into Inventory values (?,?,?);''', tuple(row))
    curs.execute("select * from Inventory")
    db.commit()
    return db


def main(args):
    """ Create a main function that first calls create_db to create a local database containing a
    table called Inventory and populates it with the contents of a csv file. The CSV filename should be
    passed in as an argument to the main function through the command line. Then the main function should
    allow the user to create as many owners as they want to. You need to keep track of those owners (in a
    dictionary), as the user should be allowed to select any owner at any point, and call the various
    functions on them.

    Your main method should have a prompt that asks the user which which of the operations they want to call
    then from there, there should be a prompt asking which of the one of the owners they want to select. The
    user may not know the item names in the Inventory table, and if this is the case,
    they should be able to prompt the main function to provide a list of all of the inventory names in the
    Inventory table, with no duplicates. At any point, the user should be able to go quit out of
    the program. Remember to close your database connection.

    Note that when the "What would you like to do next?" prompt appears, the user can either
    "create owner", "buy inventory", "sell inventory", "check net worth", or "quit".
    """
    Owner.db = create_db(args[1])
    owners = {}
    print("Hello! Welcome to the procurement simulation.")
    while True:
        action = input("What would you like to do next? ")
        if action.lower() == "create owner":
            name = input("Great! What's your owner's name? ")
            if name.lower() == "quit":
                break
            money = input("How much money does your owner have? ")
            if money.lower() == "quit":
                break
            money = int(money)
            newOwner = Owner(name, money)
            owners[name] = newOwner
            print("Owner created!")

        elif action.lower() == "buy inventory":
            name = input("Which owner do you want to buy inventory for? ")
            if name.lower() == "quit":
                break
            if name not in owners:
                print("That owner does not exist.")
            else:
                yon = input("Do you know the item name? ")
                if yon.lower() == "quit":
                    break
                if yon.lower() == "yes":
                    itemName = input("What is the item name? ")
                    if itemName.lower() == "quit":
                        break
                    owners[name].buy_cheapest(itemName)
                elif yon == "no":
                    ans = input("Do you want to buy all the inventory you can? ")
                    if ans.lower() == "quit":
                        break
                    if ans.lower() == "yes":
                        owners[name].buy_all()
                        print("You just bought all that is possible.")
                    elif ans.lower() == "no":
                        resp = input("Do you want to see what items are available? ")
                        if resp.lower() == "quit":
                            break
                        if resp.lower() == "yes":
                            curs = Owner.db.cursor()
                            curs.execute('''select * from Inventory''')
                            items = curs.fetchall()
                            curs.close()
                            options = []
                            for tup in items:
                                options.append(tup[0])
                            options = set(options)
                            for option in options:
                                print(option)
                            yon = input("Now do you know which item you want to buy? ")
                            if yon.lower() == "quit":
                                break
                            if yon.lower() == "yes":
                                itemName = input("What is the item name? ")
                                if itemName.lower() == "quit":
                                    break
                                owners[name].buy_cheapest(itemName)
                            elif yon.lower() == "no":
                                owners[name].buy_cheapest()
                            else:
                                print("Not a valid answer.")
                        elif resp.lower() == "no":
                            owners[name].buy_cheapest()
                        else:
                            print("Not a valid answer.")
                    else:
                        print("Not a valid answer.")
                else:
                    print("Not a valid answer.")

        elif action.lower() == "sell inventory":
            name = input("Which owner do you want to sell inventory for? ")
            if name.lower() == "quit":
                break
            if name not in owners:
                print("That owner does not exist.")
            else:
                yon = input("Do you know the name of the item you want to sell? ")
                if yon.lower() == "quit":
                    break
                if yon.lower() == "yes":
                    itemName = input("What is the item name? ")
                    if itemName.lower() == "quit":
                        break
                    owners[name].sell_item(itemName)
                elif yon == "no":
                    ans = input("Do you want to sell everything you own? ")
                    if ans.lower() == "quit":
                        break
                    if ans.lower() == "yes":
                        owners[name].fire_sale()
                        print("You just sold everything.")
                    elif ans.lower() == "no":
                        resp = input("Do you want to see what items are available for you to sell? ")
                        if resp.lower() == "quit":
                            break
                        if resp.lower() == "yes":
                            for myItem in owners[name].inventory_dict:
                                print(myItem[0])
                            yon = input("Now do you know which item you want to sell? ")
                            if yon.lower() == "quit":
                                break
                            if yon.lower() == "yes":
                                itemName = input("What is the item name? ")
                                if itemName.lower() == "quit":
                                    break
                                owners[name].sell_item(itemName)
                            elif yon.lower() == "no":
                                owners[name].sell_item()
                            else:
                                print("Not a valid answer. Nothing was sold.")
                        elif resp.lower() == "no":
                            owners[name].sell_item()
                        else:
                            print("Not a valid answer. Nothing was sold.")
                    else:
                        print("Not a valid answer. Nothing was sold.")
                else:
                    print("Not a valid answer. Nothing was sold.")

        elif action.lower() == "check net worth":
            name = input("Which owner do you want to check net worth for? ")
            if name.lower() == "quit":
                break
            if name not in owners:
                print("That owner does not exist.")
            else:
                print("The net worth of", name, "is", owners[name].net_worth())

        elif action.lower() == "quit":
            break

        else:
            print("Not a valid answer")

    curs = Owner.db.cursor()
    curs.execute('''drop table Inventory''')
    curs.close()
    Owner.db.close()



if __name__ == "__main__":
    import sys
    main(sys.argv)
