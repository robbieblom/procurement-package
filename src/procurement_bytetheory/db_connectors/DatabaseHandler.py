from importlib.resources import files
import sqlite3


class DatabaseHandler:
    dbFile = files("procurement_bytetheory.data").joinpath("ProcurementGame.db")

    def __init__(self):
        dbFile = files("procurement_bytetheory.data").joinpath("ProcurementGame.db")
        self.db = sqlite3.connect(dbFile)

    def saveBusiness(self, business):
        curs = self.db.cursor()
        try:
            print('Attempting to insert a new Business...')
            curs.execute(
                """
                INSERT INTO Business
                VALUES ({id}, '{name}', {money_amount}, {marketId}, {inventoryId});
                """.format(id=business.id, name=business.name, money_amount=business.money_amount, marketId=business.market.id if business.market else -1, inventoryId=business.inventory.id if business.inventory else -1)
            )
            print('New business inserted.')
        except Exception as e:
            print(e)
            print('Record already exists.  Updating a Business...')
            curs.execute(
                """
                UPDATE Business
                SET id={id}, name='{name}', money_amount={money_amount}, market_id={marketId}, inventory_id={inventoryId}
                WHERE id={id};
                """.format(id=business.id, name=business.name, money_amount=business.money_amount, marketId=business.market.id, inventoryId=business.inventory.id)
            )
            print('Business updated')
        self.db.commit()
        curs.close()
        self.saveMarket(business.market)
        self.saveInventory(business.inventory)

    def saveMarket(self, market):
        self.saveMarketRecord(market)
        self.saveItems(market.items)
    
    def saveMarketRecord(self, market):
        curs = self.db.cursor()
        try:
            print('Attempting to insert a new Market...')
            curs.execute(
                """
                INSERT INTO Market
                VALUES ({id}, '{name}')
                """.format(id=market.id, name=market.name)
            )
            print('New market inserted.')
        except Exception as e:
            print(e)
            print('Record already exists.  Updating a Market...')
            curs.execute(
                """
                UPDATE Market
                SET id={id}, name='{name}'
                WHERE id={id};
                """.format(id=market.id, name=market.name)
            )
            print('Market updated')
        self.db.commit()
        curs.close()

    def saveInventory(self, inventory):
        curs = self.db.cursor()
        try:
            print('Attempting to insert a new Inventory...')
            curs.execute(
                """
                INSERT INTO Inventory
                VALUES ({id}, '{name}')
                """.format(id=inventory.id, name=inventory.name)
            )
            print('New inventory inserted.')
        except Exception as e:
            print(e)
            print('Record already exists.  Updating a Inventory...')
            curs.execute(
                """
                UPDATE Inventory
                SET id={id}, name='{name}'
                WHERE id={id};
                """.format(id=inventory.id, name=inventory.name)
            )
            print('Inventory updated')
        self.db.commit()
        curs.close()
        self.saveItems(inventory.items)

    def saveItem(self, item):
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

    def saveItems(self, items):
        for item in items:
            self.saveItem(item)
    
    def getBusinessById(self, id):
        curs = self.db.cursor()
        try:
            curs.execute(
                """
                SELECT id, name, money_amount, market_id
                FROM Business
                WHERE id = {}
                """.format(
                    id
                )
            )
            dbResponse = curs.fetchall()
            curs.close()
            return self.deserializer.deserializeBusiness(dbResponse[0])
        except Exception as e:
            print(e)
            raise Exception("No business with id {} exists", id)

    @classmethod
    def truncateTables(cls):
        db = sqlite3.connect(cls.dbFile)
        curs = db.cursor()
        curs.execute("""DELETE FROM Business""")
        curs.execute("""DELETE FROM Market""")
        curs.execute("""DELETE FROM Inventory""")
        curs.execute("""DELETE FROM Item""")
        db.commit()
        curs.close()
        db.close()

    @classmethod
    def get_all_items(cls, item_name=None):
        db = sqlite3.connect("../data/ProcurementGame.db")
        curs = db.cursor()

        items = []
        if item_name:
            pass
        else:
            curs.execute("""select * from Inventory""")
            items = curs.fetchall()
            db.commit()
            curs.close()
            db.close()

        return list(set([i[0] for i in items]))

    def get_cheapest_item(self, item_name=None):
        """If item_name is given then find cheapest of the given item.
        Otherwise, find the cheapest item across all items
        """
        curs = self.db.cursor()
        if item_name:
            curs.execute(
                """select "Item Name", Value, Quantity from Inventory where "Item Name"
            == ?""",
                (item_name,),
            )
            candidates = curs.fetchall()
            self.db.commit()
            curs.close()

            try:
                return sorted(candidates, key=lambda x: x[1])[0]
            except:
                return []
        else:
            curs.execute(""" select "Item Name", MIN(Value), Quantity from Inventory""")
            item = curs.fetchone()
            self.db.commit()
            curs.close()
            return item

    def execute_buy(self, item):
        curs = self.db.cursor()
        item_name, value, db_quantity = self.item_in_db(item)
        if db_quantity > 1:
            curs.execute(
                """update Inventory set Quantity = Quantity - 1 where "Item Name" = ?
                and Value = ?""",
                (item_name, value),
            )
            self.db.commit()
            curs.close()
        else:
            curs.execute(
                """delete from Inventory where "Item Name" = ?
                and Value = ?""",
                (item_name, value),
            )
            self.db.commit()
            curs.close()

    def execute_sell(self, item):
        curs = self.db.cursor()
        if self.item_in_db(item):
            curs.execute(
                """update Inventory set Quantity = Quantity + 1 where
                "Item Name" = ? and Value = ?""",
                [item[0], item[1]],
            )
        else:
            curs.execute(
                """insert into Inventory ("Item Name",Value,Quantity)
                values (?,?,?)""",
                [item[0], item[1], 1],
            )

        self.db.commit()
        curs.close()

    def item_in_db(self, item):
        curs = self.db.cursor()

        curs.execute(
            """select "Item Name", Value, Quantity from Inventory where
            "Item Name" = ? and Value = ?""",
            [item[0], item[1]],
        )
        item = curs.fetchone()

        self.db.commit()
        curs.close()

        return item
