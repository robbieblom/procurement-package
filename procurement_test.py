# Robert Blom
# 903261321

import sqlite3
import csv
class Owner:
    """The Owner class should have one class attribute db (initialized as None) which will represent a
    database connection object. Each owner instance should have instance variables that hold the
    owner's unique name, money, and a dictionary of their inventory in the form {(item, price): count)}
    """
    db = None

    def __init__(self, name, money = 500.0, inventory_dict = {}):
        """money and inventory_dict have initital default values, but any other money amount can be
        passed in to the init method

        Parameters:
        self
        name: String
        money: float -- the Owner's money, is 500.0 if not given
        inventory_dict: dict -- keeps track of Owner's inventory, is {} when first initialized}
        """

        self.name = name
        self.money = money
        self.inventory_dict = inventory_dict


    def buy_cheapest(self, item_name = None):
        """Buys the cheapest item with the specified item_name, and if no item_name is specified,
        buys one of the cheapest items in the Inventory table. The price to buy something is
        95% of its value.  Reduce the Owner's money by that much, decrease the
        count of that item in the Inventory table (or remove it if there are none left
        after you decrease the count), and add it to the Owner's inventory_dict,
        with the value being the price they paid for it. If you buy that item again,
        you will just increment the quantity of that item in the inventory_dict.
        If the owner does not have enough money to buy any of the items in
        the Inventory table or there are no items left in the table, print a message to indicate
        this to the user.

        Parameters:
        self
        item_name: String -- the name of the item to be bought

        Return:
        None
        """


        curs = Owner.db.cursor()
        if item_name != None:

            #find cheapest value
            curs.execute('''select "Item Name", Value, Quantity from Inventory where "Item Name"
                == ?''', (item_name,))
            candidates = curs.fetchall()
            name = sorted(candidates, key = lambda x: x[1])[0][0]
            value = sorted(candidates, key = lambda x: x[1])[0][1]
            quantity = sorted(candidates, key = lambda x: x[1])[0][2]
            price = round(.95*value, 2)

            #can the owner buy it?
            if price > self.money:
                print("You don't have enough money to buy that")
                return
            else:
                print(item_name, "was bought.")
            #update owner's stuff
            self.money = self.money - price
            if (name, price) in self.inventory_dict:
                self.inventory_dict[(name, price)] += 1
            else:
                self.inventory_dict[(name, price)] = 1

            #update database
            if quantity > 1:
                curs.execute('''update Inventory set Quantity = Quantity - 1 where "Item Name" = ?
                    and Value = ?''', (item_name,value))
                Owner.db.commit()
            else:
                curs.execute('''delete from Inventory where "Item Name" = ?
                    and Value = ?''', (item_name,value))
                Owner.db.commit()
        else:
            #find cheapest item
            curs.execute(''' select "Item Name", MIN(Value), Quantity from Inventory''')
            item = curs.fetchone()

            #can the owner buy it?
            price = round(.95*item[1], 2)
            if price > self.money:
                print("You don't have enough money to buy anything")
                return
            else:
                print(item[0], "was bought.")

            #update owner's stuff
            self.money = self.money - price
            if (item[0], price) in self.inventory_dict:
                self.inventory_dict[(item[0], price)] += 1
            else:
                self.inventory_dict[(item[0], price)] = 1

            #update database
            if item[2] > 1:
                curs.execute('''update Inventory set Quantity = Quantity - 1 where "Item Name" = ?
                    and Value = ?''', (item[0],item[1]))
                Owner.db.commit()
            else:
                curs.execute('''delete from Inventory where "Item Name" = ?
                    and Value = ?''', (item[0],item[1]))
                Owner.db.commit()


    def sell_item(self, item_name = None):
        """Sells the most expensive of the specified item_name (from the owner's
        inventory), and if no item_name is specified, sells the most expensive item
        in inventory.  The amount of of money you make when you sell something
        is 105% of its value. Increase the owner's money by that much, and add it to the
        table with the value being the price for which it was sold. If the item is already
        in the Inventory table and has the same price as you're selling yours for, increase
        the count of that item. Otherwise, make sure to add a new row with your price,
        item_name, and count of 1. Then, decrease the count of that item (or remove it if the
        count is 1) from the inventory_dict.

        Parameters:
        self
        item_name: String -- the name of the item to be bought

        Return:
        None
        """
        curs = Owner.db.cursor()
        if item_name != None:
            #check if item_name is in inventory_dict
            val = False
            for item in self.inventory_dict:
                if item[0] == item_name:
                    val = True
                    break

            #not in inventory_dict
            if val == False:
                print("You don't have that item to sell")
                return

            #in inventory_dict
            else:
                #select the inventory with highest value
                print(item_name, "was sold.")
                maximum = (-1,-1)
                for item in self.inventory_dict:
                    if item[0] == item_name:
                        if item[1] > maximum[1]:
                            maximum = item

                #update inventory_dict
                if self.inventory_dict[maximum] > 1:
                    self.inventory_dict[maximum] -= 1
                else:
                    del self.inventory_dict[maximum]

                #increase money by 105% of price
                self.money += 1.05*maximum[1]

                soldMaximum = (maximum[0], 1.05*maximum[1])
                #update database
                curs.execute('''select "Item Name", Value from Inventory where
                    "Item Name" = ? and Value = ?''',soldMaximum)
                check = curs.fetchone()

                #if soldMaximum in the database
                if check != None:
                    curs.execute('''update Inventory set Quantity = Quantity + 1 where
                        "Item Name" = ? and Value = ?''', soldMaximum)
                    Owner.db.commit()

                #if soldMaximum not in the database
                else:
                    row = soldMaximum + (1,)
                    curs.execute('''insert into Inventory ("Item Name",Value,Quantity)
                        values (?,?,?)''', row)
                    Owner.db.commit()

        else:
            if len(self.inventory_dict) == 0:
                print(self.name, "doesn't have any inventory.")
                return

            #find most expensive item
            maximum = (-1,-1)
            for item in self.inventory_dict:
                if item[1] > maximum[1]:
                    maximum = item
            print(maximum[0], "was sold.")

            #update inventory_dict
            if self.inventory_dict[maximum] > 1:
                self.inventory_dict[maximum] -= 1
            else:
                del self.inventory_dict[maximum]

            #update money
            self.money += 1.05*maximum[1]

            soldMaximum = (maximum[0], 1.05*maximum[1])
            #update database
            curs.execute('''select "Item Name", Value from Inventory where
                "Item Name" = ? and Value = ?''',soldMaximum)
            check = curs.fetchone()

            #if soldMaximum in the database
            if check != None:
                curs.execute('''update Inventory set Quantity = Quantity + 1 where
                    "Item Name" = ? and Value = ?''', soldMaximum)
                Owner.db.commit()

            #if soldMaximum not in the database
            else:
                row = soldMaximum + (1,)
                curs.execute('''insert into Inventory ("Item Name",Value,Quantity)
                    values (?,?,?)''', row)
                Owner.db.commit()




    def fire_sale(self):
        """Sells everything in the Owner's inventory. Because you are selling so much,
        you earn only 80% of the value of each item you sell. Remove all items from your
        inventory_dict and add them all to the Inventory table with value staying the
        same -- if the item is already in the table and has the same price as you're selling
        yours for, increase the count of that item. Otherwise, make sure to add a new row with
        that price. Update the owner's money accordingly.

        Parameters:
        self

        Return:
        None
        """
        curs = Owner.db.cursor()
        for item in self.inventory_dict:
            #is item in Inventory?
            curs.execute('''select "Item Name", "Value" from Inventory where
                "Item Name" = ? and Value = ?''', item)
            check = curs.fetchone()

            #item in Inventory
            if check != None:
                curs.execute('''update Inventory set Quantity = Quantity + ? where
                    "Item Name" = ? and Value = ?''', (self.inventory_dict[item],) + item)
                Owner.db.commit()
                self.money += .8*item[1]*self.inventory_dict[item]
            #item not in Inventory
            else:
                curs.execute('''insert into Inventory ("Item Name", Value, Quantity)
                    values (?,?,?)''', item + (self.inventory_dict[item],))
                Owner.db.commit()
                self.money += .8*item[1]*self.inventory_dict[item]
        self.inventory_dict = {}


    def net_worth(self):
        """Returns the total net worth of the Owner, which is the amount of
        money they have plus the sum of the value of everything in their inventory.

        Parameters:
        self

        Return:
        float -- the amount of money the user has plus the sum of the value of everything in
                 inventory
        """
        inventory_sum = 0
        for item in self.inventory_dict:
            inventory_sum += item[1]*self.inventory_dict[item]
        worth = inventory_sum + self.money
        return round(worth, 2)


    def buy_all(self, item_name = None):
        """Buys as many of the specified item as possible. If no item_name is given,
        defaults to the item with the lowest price. The
        price per item is 95% of the value. Update the Inventory table, inventory_dict,
        and the owner's money accordingly (as stated in the methods above).

        Parameters:
        self
        item_name: String -- name of the item to buy

        Return:
        None
        """
        curs = Owner.db.cursor()
        if item_name != None:
            #is item_name in Inventory?
            curs.execute('''select "Item Name", Value, Quantity from Inventory where
                "Item Name" = ?''', (item_name,))
            items = curs.fetchall()

            if items == []:
                print("That item does not exist")
                return
            else:
                for inv in sorted(items, key = lambda x: x[1]):
                    for purchase in list(range(1,inv[2]+1)):
                        if self.money <= 0 or self.money - round(.95*inv[1],2) <= 0:
                            print("You couldn't buy everything because you didn't have enough money")
                            return
                        cost = round(.95*inv[1],2)
                        self.money -= cost

                        #update inventory_dict
                        if (inv[0], cost) in self.inventory_dict:
                            self.inventory_dict[(inv[0], cost)] += 1
                        else:
                            self.inventory_dict[(inv[0], cost)] = 1

                        #update Inventory
                        if purchase < inv[2]:
                            curs.execute('''update Inventory set Quantity = Quantity - 1
                                where "Item Name" = ? and Value = ?''', inv[:2])
                            Owner.db.commit()
                        else:
                            curs.execute('''delete from Inventory where "Item Name" = ? and
                                Value = ?''', inv[:2])
                            Owner.db.commit()

        else:
            curs.execute(''' select "Item Name", Value, Quantity from Inventory''')
            table = curs.fetchall()
            sumDict = {}
            tableDict = {}
            for element in table:
                tableDict[(element[0], element[1])] = element[2]
            for key in tableDict:
                if key[0] in sumDict:
                    sumDict[key[0]] += key[1]*tableDict[key]
                else:
                    sumDict[key[0]] = key[1]*tableDict[key]

            #find the min value of sumDict
            minClass = min(list(sumDict.items()), key = lambda x: x[1])[0]
            curs.execute('''select "Item Name", value, Quantity from Inventory
                where "Item Name" = ?''', (minClass,))
            items = curs.fetchall()

            for inv in sorted(items, key = lambda x: x[1]):
                for purchase in list(range(1,inv[2]+1)):
                    if self.money <= 0 or self.money - round(.95*inv[1],2) <= 0:
                        print("You couldn't buy everything because you didn't have enough money")
                        return
                    cost = round(.95*inv[1],2)
                    self.money -= cost

                    #update inventory_dict
                    if (inv[0], cost) in self.inventory_dict:
                        self.inventory_dict[(inv[0], cost)] += 1
                    else:
                        self.inventory_dict[(inv[0], cost)] = 1

                    #update Inventory
                    if purchase < inv[2]:
                        curs.execute('''update Inventory set Quantity = Quantity - 1
                            where "Item Name" = ? and Value = ?''', inv[:2])
                        Owner.db.commit()
                    else:
                        curs.execute('''delete from Inventory where "Item Name" = ? and
                            Value = ?''', inv[:2])
                        Owner.db.commit()


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