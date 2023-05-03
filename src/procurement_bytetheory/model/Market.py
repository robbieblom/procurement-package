from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler
from procurement_bytetheory.model.Item import Item
from importlib.resources import files
import csv


class Market:
    numMarkets = 0
    seedFile = files("procurement_bytetheory.data").joinpath("items.csv")

    def __init__(self, name, id=None, items=None, dbHandler=None):
        self.name = name

        self.id = id if id else Market.numMarkets + 1
        Market.numMarkets += 1

        self.items = items if items else [] # [item1, item2, ...]
        self.dbHandler = dbHandler if dbHandler else DatabaseHandler()

    def save(self):
        self.dbHandler.saveMarket(self)

    def seedMarket(self):
        seedItems = self.getSeedItems()
        self.addItemsToMarket(seedItems)

    def getSeedItems(self):
        csvin = csv.reader(open(Market.seedFile))
        seedItems = []
        for i, row in enumerate(csvin):
            if(i==0): continue
            name, value = [row[0], float(row[1])]
            newItem = Item(name, value)
            seedItems.append(newItem)
        return seedItems

    def addItemsToMarket(self, items):
        for item in items:
            self.addItemToMarket(item)
    
    def addItemToMarket(self, item):
        self.items.append(item)
        item.setMarket(self)

    def removeItemFromMarket(self, item):
        self.items.remove(item)
        item.setMarket(None)

    def hasItem(self, itemName):
        return itemName in [item.name for item in self.items]

    def getCheapestItemByName(self, itemName):
        if(self.items):
            return min([item for item in self.items if item.name == itemName])
        return None

    def getCheapestItemInMarket(self):
        if(self.items):
            return min(self.items)
        return None