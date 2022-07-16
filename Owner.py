import sqlite3
import csv

class Owner:
    db = None

    def __init__(self, name, money = 500.0, inventory_dict = {}):
        """money and inventory_dict have initital default values, but any other money amount can be
        passed in to the init method

        Parameters:
        self
        name: String
        money: float -- the Owner's money, is 500.0 if not given
        inventory_dict: dict -- keeps track of Owner's inventory, is {} when first initialized. {(item, price): count)}
        """

        self.name = name
        self.money = money
        self.inventory_dict = inventory_dict


    @classmethod
    def create_db(cls, file_name):
        """Creates a local SQLite database using the sqlite3 module and then creates a table called
        Inventory in the database. There will be three columns: item_name, Price, and Quantity. 
        The composite key of the table will be (item_name, value).
        Price and Quantity will both be stored as integers in the database.

        Parameters:
        file_name: String -- the name of the csv file that contains the inventory
        
        Return:
        None
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
        Owner.db = db

    @classmethod
    def drop_db(cls):
        curs = Owner.db.cursor()
        curs.execute('''drop table Inventory''')
        curs.close()
        Owner.db.close()
        

    def buy_cheapest(self, item_name = None):
        """Buys the cheapest item with the specified item_name, and if no item_name is specified,
        buys one of the cheapest items in the Inventory table. The price to buy something is
        95% of its value.

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
                print("You don't have enough money to buy that.\n")
                return
            else:
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
                print("You just bought one ", item_name + ".\n")
        else:
            #find cheapest item
            curs.execute(''' select "Item Name", MIN(Value), Quantity from Inventory''')
            item = curs.fetchone()

            #can the owner buy it?
            price = round(.95*item[1], 2)
            if price > self.money:
                print("You don't have enough money to buy anything.\n")
                return
            else:
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
                print("You just bought one", item[0] + ".\n")


    def sell_item(self, item_name = None):
        """Sells the most expensive of the specified item_name (from the owner's
        inventory), and if no item_name is specified, sells the most expensive item
        in inventory.  The amount of of money you make when you sell something
        is 105% of its value.

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
                print("You don't have that item to sell.\n")
                return

            #in inventory_dict
            else:
                #select the inventory with highest value
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
                
                print("You just sold one unit of", item_name + ".\n")

        else:
            if len(self.inventory_dict) == 0:
                print(self.name, "doesn't have any inventory.\n")
                return

            #find most expensive item
            maximum = (-1,-1)
            for item in self.inventory_dict:
                if item[1] > maximum[1]:
                    maximum = item

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

            print("You just sold one unit of", maximum[0] + ".\n")




    def fire_sale(self):
        """Sells everything in the Owner's inventory. Because you are selling so much,
        you earn only 80% of the value of each item you sell. 

        Parameters:
        self

        Return:
        None
        """
        curs = Owner.db.cursor()
        if len(self.inventory_dict) == 0:
            print(self.name, "doesn't have any inventory.\n")
        else:
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
            print("You just sold everything.\n")


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
        print("The net worth of", self.name, "is", str(round(worth, 2)) + ".\n")
        return round(worth, 2)


    def buy_all(self, item_name = None):
        """Buys as many of the specified item as possible. If no item_name is given,
        defaults to the item with the lowest price. The price per item is 95% of the value.

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
                print("That item does not exist.\n")
                return
            else:
                for inv in sorted(items, key = lambda x: x[1]):
                    for i, purchase in enumerate( list(range(1,inv[2]+1)) ):
                        if self.money <= 0 or self.money - round(.95*inv[1],2) <= 0:
                            print("Item:", inv[0] + ".", "Number bought:", str(i) + ".")
                            print("You couldn't buy all of the item because you didn't have enough money.\n")
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

                        print("Item:", inv[0] + ".", "Number bought:", str(i) + ".\n")

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
                for i, purchase in enumerate( list(range(1,inv[2]+1)) ):
                    if self.money <= 0 or self.money - round(.95*inv[1],2) <= 0:
                        print("Item:", inv[0] + ".", "Number bought:", str(i) + ".")
                        print("You couldn't buy everything because you didn't have enough money.\n")
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

                    print("Item:", inv[0] + ".", "Number bought:", str(i) + ".\n")
