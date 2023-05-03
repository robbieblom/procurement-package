from procurement_bytetheory.model.Market import Market
from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler
from procurement_bytetheory.model.Subject import Subject
from procurement_bytetheory.model.Inventory import Inventory


class Business(Subject):
    numBusinesses = 0

    def __init__(self, name, money_amount=400, id=None, inventory=None, market=None, dbHandler=None):
        super().__init__()

        self.name = name
        self.money_amount = money_amount

        self.id = id if id else Business.numBusinesses + 1
        Business.numBusinesses += 1

        self.inventory = inventory if inventory else Inventory("ACME Innovations Inventory")
        self.market = market if market else Market("USA")
        self.dbHandler = dbHandler if dbHandler else DatabaseHandler()

    def save(self):
        self.dbHandler.saveBusiness(self)

    def buyCheapest(self, itemName=None):
        """Buys the cheapest item with the specified itemName, and if no itemName is specified,
        buys one of the cheapest items in the market.
        """
        buyingCheapestOfSpecificItem = bool(itemName)
        if buyingCheapestOfSpecificItem:
            cheapestOfGivenItem = self.market.getCheapestItemByName(itemName)
            self.buy(cheapestOfGivenItem)
        else:
            cheapestItemInMarket = self.market.getCheapestItemInMarket()
            self.buy(cheapestItemInMarket)

    def buyAsManyAsPossible(self, itemName=None):
        """Buys as many of the specified item as possible. If no itemName is given,
        defaults to the item with the lowest price.
        """
        buyingCheapestOfSpecificItem = bool(itemName)

        if buyingCheapestOfSpecificItem:
            cheapestOfGivenItem = self.market.getCheapestItemByName(itemName)
            while self.canAfford(cheapestOfGivenItem):
                self.buy(cheapestOfGivenItem)
                cheapestOfGivenItem = self.market.getCheapestItemByName(itemName)
        else:
            itemToBuy = self.market.getCheapestItemInMarket()
            while self.canAfford(itemToBuy):
                self.buy(itemToBuy)
                itemToBuy = self.market.getCheapestItemByName(itemToBuy.name)

    def payPriceOfItem(self, price):
        self.money_amount = self.money_amount - price

    def addItemToInventory(self, item):
        self.inventory.addItem(item)

    def canAfford(self, item):
        if self.money_amount > item.getPrice():
            return True
        return False

    def buy(self, item):
        if self.canAfford(item):
            self.market.removeItemFromMarket(item)
            self.payPriceOfItem(item.getPrice())
            self.addItemToInventory(item)
        else:
            raise Exception("You don't have enough money to buy this!")

    def sellItem(self, itemName=None):
        """Sells the most expensive of the specified itemName.
        If no itemName is specified, sells the most expensive item.
        The amount of of money you make when you sell something
        is 105% of its value.
        """
        sellingSpecificItem = bool(itemName)
        if sellingSpecificItem:
            if self.inventory.hasItem(itemName):
                highestValueSku = self.inventory.getHighestValueSku(itemName)
                self.executeSale(highestValueSku)
        else:
            if not self.inventory.isEmpty():
                highestValueSku = self.inventory.getHighestValueSku()
                self.executeSale(highestValueSku)

    def liquidateInventory(self):
        """Sells all items in inventory at 80% of their value."""
        for item in self.inventory:
            self.collectPayment(item.price)
            self.removeItemFromInventory

    def collectPayment(self, salesPrice):
        self.money_amount += salesPrice

    def removeItemFromInventory(self, item):
        self.inventory.removeItem(item)

    def executeSale(self, sku):
        self.collectPayment(sku.value * 1.05)
        self.removeItemFromInventory(sku)

    def getNetWorth(self):
        return self.money_amount + self.inventory.getValue()
