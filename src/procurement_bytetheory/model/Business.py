from procurement_bytetheory.model.Market import Market
from procurement_bytetheory.db_connectors.BusinessDbHandler import BusinessDbHandler
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
        self.dbHandler = dbHandler if dbHandler else BusinessDbHandler()

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
        if(itemName != None and not self.market.hasItem(itemName)): return

        buyingCheapestOfSpecificItem = bool(itemName)
        if buyingCheapestOfSpecificItem:
            cheapestOfGivenItem = self.market.getCheapestItemByName(itemName)
            if(self.canAfford(cheapestOfGivenItem)):
                self.buy(cheapestOfGivenItem)
                self.buyAsManyAsPossible(cheapestOfGivenItem.name)
        else:
            itemToBuy = self.market.getCheapestItemInMarket()
            self.buyAsManyAsPossible(itemToBuy.name)

    def payPriceOfItem(self, price):
        self.money_amount = self.money_amount - price

    def addItemToInventory(self, item):
        self.inventory.addItem(item)

    def canAfford(self, item):
        if self.money_amount > item.getPurchasePrice():
            return True
        return False

    def buy(self, item):
        if self.canAfford(item):
            self.market.removeItemFromMarket(item)
            self.payPriceOfItem(item.getPurchasePrice())
            self.addItemToInventory(item)
        else:
            raise Exception("You don't have enough money to buy this!")

    def sellItem(self, itemName=None):
        """Sells the most expensive of the specified itemName.
        If no itemName is specified, sells the most expensive item.
        """
        sellingSpecificItem = bool(itemName)
        if sellingSpecificItem:
            if self.inventory.hasItem(itemName):
                highestValueItem = self.inventory.getHighestValueItem(itemName)
                self.executeSale(highestValueItem)
        else:
            if not self.inventory.isEmpty():
                highestValueItem = self.inventory.getHighestValueItem()
                self.executeSale(highestValueItem)

    def liquidateInventory(self):
        for item in self.inventory.items:
            self.collectPaymentFromMarketCustomer(item.getFireSalePrice())
        self.clearInventory()

    def collectPaymentFromMarketCustomer(self, salesPrice):
        self.money_amount += salesPrice

    def removeItemFromInventory(self, item):
        self.inventory.removeItem(item)

    def clearInventory(self):
        self.inventory.clear()

    def executeSale(self, item):
        self.collectPaymentFromMarketCustomer(item.getSalesPrice())
        self.removeItemFromInventory(item)

    def getNetWorth(self):
        return self.money_amount + self.inventory.getValue()
