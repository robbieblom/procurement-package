from procurement_bytetheory.db_connectors.ItemDbHandler import ItemDbHandler
import json
import random

class Item:
    itemCount = 0

    def __init__(self, name, value, id=None, marketId=None, inventoryId=None, dbHandler=None):
        self.name = name
        self.value = value

        self.id = id if id else Item.itemCount + 1
        Item.itemCount += 1
        
        self.marketId = marketId
        self.inventoryId = inventoryId
        self.dbHandler = dbHandler if dbHandler else ItemDbHandler()

    def save(self):
        self.dbHandler.saveItem(self)

    @staticmethod
    def getItemById(id):
        dbHandler = ItemDbHandler()
        dbRecord = dbHandler.getItemById(id)
        return Item.deserializeToObject(dbRecord)

    @staticmethod
    def deserializeToObject(dbRecord):
        (id, name, value, market_id, inventory_id) = dbRecord
        return Item(name, value, id=id, marketId=market_id, inventoryId=inventory_id)

    def getDictionaryRepresentation(self):
        try :
            return {
                "id": self.id,
                "name": self.name,
                "value": self.value,
                "marketId": self.marketId,
                "metrics": {
                    "salesPrice": self.getSalesPrice(),
                    "purchasePrice": self.getPurchasePrice(),
                }
            }
        except: 
            return {
                "id": self.id,
                "name": self.name,
                "value": self.value,
                "marketId": None,
            }
        
    def serializeToJson(self):
        return json.dumps(self.getDictionaryRepresentation())

    def setMarket(self, marketId):
        self.marketId = marketId

    def setInventory(self, inventoryId):
        self.inventoryId = inventoryId

    def getPurchasePrice(self):
        purchasePriceFactor = self.getRandomFromRange(.92, .98)
        return round(purchasePriceFactor*self.value, 2)

    def getSalesPrice(self):
        salesPriceFactor = self.getRandomFromRange(1.02, 1.08)
        return round(salesPriceFactor*self.value, 2)

    def getFireSalePrice(self):
        return round(.85*self.value, 2)

    def getRandomFromRange(self, lowerBound, upperBound):
        randFactor = random.random()
        return randFactor*(upperBound - lowerBound) + lowerBound

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