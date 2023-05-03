from procurement_bytetheory.db_connectors.InventoryDbHandler import InventoryDbHandler


class Inventory:
    numInventories = 0

    def __init__(self, name, id=None, items=None, dbHandler=None):
        self.name = name

        self.id = id if id else Inventory.numInventories + 1
        Inventory.numInventories += 1

        self.items = items if items else []  # [item1, item2, ...]
        self.dbHandler = dbHandler if dbHandler else InventoryDbHandler()

    def save(self):
        self.dbHandler.saveInventory(self)

    def addItem(self, item):
        self.items.append(item)
        item.setInventory(self)

    def removeItem(self, item):
        self.items.remove(item)
        item.setInventory(None)

    def clear(self):
        for item in self.items:
            item.setInventory(None)
        self.items = []

    def isEmpty(self):
        return not bool(len(self.items))

    def hasItem(self, itemName):
        return itemName in [item.name for item in self.items]

    def getHighestValueItem(self, itemName=None):
        if itemName:
            return max([item for item in self.items if item.name == itemName])
        else:
            return max(self.items)

    def getValue(self):
        return sum([item.value for item in self.items])
