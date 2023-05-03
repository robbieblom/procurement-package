from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler


class Inventory:
    numInventories = 0

    def __init__(self, name, id=None, items=None, dbHandler=None):
        self.name = name
        
        self.id = id if id else Inventory.numInventories + 1
        Inventory.numInventories += 1

        self.items = items if items else []  # [item1, item2, ...]
        self.dbHandler = dbHandler if dbHandler else DatabaseHandler()

    def save(self):
        self.dbHandler.saveInventory(self)

    def addItem(self, item):
        self.items.append(item)

    def removeItem(self, item):
        self.items.remove(item)

    def hasItem(self, itemName):
        return itemName in [item.name for item in self.items]

    def getHighestValueSku(self, itemName):
        return max([item.value for item in self.items if item.name == itemName])

    def getValue(self):
        return sum([item.value for item in self.items])
