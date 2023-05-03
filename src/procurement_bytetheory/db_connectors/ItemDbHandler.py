from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler

class ItemDbHandler(DatabaseHandler):

    def __init__(self):
        super().__init__()

    def saveItem(self, item):
        # Note: temp table not needed because we're just upserting
        self.upsertItem(item)
    
    def saveItems(self, items):
        # Note: temp table not needed because we're just upserting
        self.upsertItems(items)

    def populateItemTempTable(self, items):
        curs = self.db.cursor()
        curs.execute(
            """
            DELETE FROM Temp_Item;
            """
        )

        for item in items:
            print('Inserting a new Item into temp table...')
            curs.execute(
                """
                INSERT INTO Temp_Item
                VALUES ({id}, '{name}', {value}, {marketId}, {inventoryId})
                """.format(id=item.id, name=item.name, value=item.value, marketId=item.market.id if item.market else -1, inventoryId=item.inventory.id if item.inventory else -1)
            )
            print('New item inserted into temp table.')
        
        self.db.commit()
        curs.close()

    def upsertItem(self, item):
        curs = self.db.cursor()
        try:
            print('Attempting to insert a new Item...')
            curs.execute(
                """
                INSERT INTO Item
                VALUES ({id}, '{name}', {value}, {marketId}, {inventoryId})
                """.format(id=item.id, name=item.name, value=item.value, marketId=item.market.id if item.market else -1, inventoryId=item.inventory.id if item.inventory else -1)
            )
            print('New item inserted.')
        except Exception as e:
            print(e)
            print('Record already exists.  Updating an Item...')
            curs.execute(
                """
                UPDATE Item
                SET id={id}, name='{name}', value={value}, market_id={marketId}, inventory_id={inventoryId}
                WHERE id={id};
                """.format(id=item.id, name=item.name, value=item.value, marketId=item.market.id if item.market else -1, inventoryId=item.inventory.id if item.inventory else -1)
            )
            print('Item updated')
        self.db.commit()
        curs.close()

    def upsertItems(self, items):
        for item in items:
            self.upsertItem(item)
    