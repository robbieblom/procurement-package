from procurement_bytetheory.db_connectors.ItemDbHandler import ItemDbHandler

class Item:
    itemCount = 0

    def __init__(self, name, value, id=None, market=None, inventory=None, dbHandler=None):
        self.name = name
        self.value = value

        self.id = id if id else Item.itemCount + 1
        Item.itemCount += 1
        
        self.market = market
        self.inventory = inventory
        self.dbHandler = dbHandler if dbHandler else ItemDbHandler()

    def save(self):
        self.dbHandler.saveItem(self)

    def setMarket(self, market):
        self.market = market

    def setInventory(self, inventory):
        self.inventory = inventory

    def getPurchasePrice(self):
        return .95*self.value

    def getSalesPrice(self):
        return 1.05*self.value

    def getFireSalePrice(self):
        return .8*self.value

    def __eq__(self, other):
        return True if self.id == other.id else False

    def __gt__(self, other):
        return True if self.value > other.value else False

    def __ge__(self, other):
        return True if self.value >= other.value else False

    def __lt__(self, other):
        return True if self.value < other.value else False
    
    def __ge__(self, other):
        return True if self.value <= other.value else False