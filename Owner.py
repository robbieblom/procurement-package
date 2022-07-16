from DatabaseHandler import DatabaseHandler

class Owner:
    db = None

    def __init__(self, name, money=400, inventory_dict={}):
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
        self.dbHandler = DatabaseHandler()


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
        
        if(item_name):
            cheapest_item = self.dbHandler.get_cheapest_item(item_name)
            if(self.can_afford(cheapest_item)):
                self.execute_buy(cheapest_item)
                print("You just bought one", cheapest_item[0] + ".\n")
                return
            else:
                print("You don't have enough money to buy another one of these.\n")
                return    
        else:
            cheapest_item_of_all = self.dbHandler.get_cheapest_item()
            if(self.can_afford(cheapest_item_of_all)):
                self.execute_buy(cheapest_item_of_all)
                print("You just bought one", cheapest_item_of_all[0] + ".\n")
                return
            else:
                print("You don't have enough money to buy anything.\n")
                return


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
        if(item_name):
            if(self.has_item(item_name)):
                highest_value_item = self.get_highest_value_item(item_name)
                self.execute_sell(highest_value_item)
                print("You just sold one unit of", item_name + ".\n")
                return
            else:
                print("You don't have that item to sell.\n")
                return
        else:
            if(self.has_inventory()):
                highest_value_item = self.get_highest_value_item()
                self.execute_sell(highest_value_item)
                print("You just sold one unit of", highest_value_item[0] + ".\n")
                return
            else:
                print(self.name, "doesn't have any inventory.\n")
                return


    def fire_sale(self):
        """Sells everything in the Owner's inventory. Because you are selling so much,
        you earn only 80% of the value of each item you sell. 

        Parameters:
        self

        Return:
        None
        """
        if(self.has_inventory()):
            self.execute_fire_sell()
            print("You just sold everything.\n")
        else:
            print(self.name, "doesn't have any inventory.\n")


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
        if(item_name):
            # note that there will always be at least one item
            # in db because of ActionsPrompt
            while(self.dbHandler.get_cheapest_item(item_name)):
                self.buy_cheapest(item_name)
        else:
            cheapest_item_of_all = self.dbHandler.get_cheapest_item()
            while(self.dbHandler.get_cheapest_item(cheapest_item_of_all[0])):
                self.buy_cheapest(item_name)


    def can_afford(self, item):
        price = .95*item[1]
        if(self.money > price):
            return True
        else:
            return False


    def execute_buy(self, item):
        item_name, price = (item[0], .95*item[1])

        #update owner's stuff
        self.money = self.money - .95*item[1]
        if( (item[0], .95*item[1]) ) in self.inventory_dict:
            self.inventory_dict[ (item_name, price) ] += 1
        else:
            self.inventory_dict[ (item_name, price) ] = 1

        #update database
        self.dbHandler.execute_buy(item)


    def has_item(self, item_name):
        for item in self.inventory_dict:
            if item[0] == item_name:
                return True
        return False


    def get_highest_value_item(self, item_name = None):
        """ If item_name is given then find most expensive of the given item.
            Otherwise, find the most expensive item across all items
        """
        highest_value_item = (-1,-1, -1)
        if(item_name):
            for item in self.inventory_dict:
                if(item[0] == item_name and item[1] > highest_value_item[1]) :
                    highest_value_item = item
        else:
            for item in self.inventory_dict:
                if(item[1] > highest_value_item[1]):
                    highest_value_item = item

        return [highest_value_item[0], highest_value_item[1] ]


    def execute_sell(self, item):
        item_name, value = [ item[0], item[1] ]

        #update inventory_dict
        if self.inventory_dict[(item_name, value)] > 1:
            self.inventory_dict[(item_name, value)] -= 1
        else:
            del self.inventory_dict[(item_name, value)]

        #increase money by 105% of value
        self.money += 1.05*value

        self.dbHandler.execute_sell(item)


    def execute_fire_sell(self):
        for item in self.inventory_dict:
            value = item[1]
            self.money += .8*value
            self.dbHandler.execute_sell(item)

        self.inventory_dict = {}
        



    def has_inventory(self):
        return len(self.inventory_dict) != 0