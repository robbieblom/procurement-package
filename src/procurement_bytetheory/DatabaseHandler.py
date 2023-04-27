import sqlite3
import csv

class DatabaseHandler():

    def __init__(self) -> None:
        self.db = sqlite3.connect("Inventory.db")

    @classmethod
    def create_db(cls, input_file_name):
        """Creates a local SQLite database using the sqlite3 module and then creates a table called
        Inventory in the database. There will be three columns: item_name, Price, and Quantity. 
        The composite key of the table will be (item_name, value).
        Price and Quantity will both be stored as integers in the database.

        Parameters:
        file_name: String -- the name of the csv file that contains the inventory
        
        Return:
        None
        """
        db = sqlite3.connect("Inventory.db")
        curs = db.cursor()

        csvin = csv.reader(open(input_file_name))
        curs.execute('''CREATE TABLE if not exists Inventory (
                    'Item Name' text check('Item Name' != ""),
                    Value Integer not null,
                    Quantity Integer not null,
                    primary key ('Item Name', Value)
                    ); ''')
        for i, row in enumerate(csvin):
            if(i == 0):
                continue
            curs.execute('''insert into Inventory values (?,?,?);''', tuple(row))
        
        db.commit()
        curs.close()
        db.close()


    @classmethod
    def drop_db(cls):
        db = sqlite3.connect("Inventory.db")
        curs = db.cursor()

        curs.execute('''drop table Inventory''')

        db.commit()
        curs.close()
        db.close()

    
    @classmethod
    def get_all_items(cls, item_name = None):
        db = sqlite3.connect("Inventory.db")
        curs = db.cursor()

        items = []
        if(item_name):
            pass
        else:
            curs.execute('''select * from Inventory''')
            items = curs.fetchall()
            db.commit()
            curs.close()
            db.close()

        return list( set([ i[0] for i in items] ) )

    
    def get_cheapest_item(self, item_name = None):
        """ If item_name is given then find cheapest of the given item.
            Otherwise, find the cheapest item across all items
        """
        curs = self.db.cursor()
        if(item_name):
            curs.execute('''select "Item Name", Value, Quantity from Inventory where "Item Name"
            == ?''', (item_name,))
            candidates = curs.fetchall()
            self.db.commit()
            curs.close()

            try:
                return sorted(candidates, key = lambda x: x[1])[0]
            except:
                return []
        else:
            curs.execute(''' select "Item Name", MIN(Value), Quantity from Inventory''')
            item = curs.fetchone()
            self.db.commit()
            curs.close()
            return item
            
    
    def execute_buy(self, item):        
        curs = self.db.cursor()
        item_name, value, db_quantity = self.item_in_db(item)
        if(db_quantity > 1):
            curs.execute('''update Inventory set Quantity = Quantity - 1 where "Item Name" = ?
                and Value = ?''', (item_name,value))
            self.db.commit()
            curs.close()
        else:
            curs.execute('''delete from Inventory where "Item Name" = ?
                and Value = ?''', (item_name,value))
            self.db.commit()
            curs.close()


    def execute_sell(self, item):
        curs = self.db.cursor()
        if(self.item_in_db(item)):
            curs.execute('''update Inventory set Quantity = Quantity + 1 where
                "Item Name" = ? and Value = ?''', [item[0], item[1]])
        else:
            curs.execute('''insert into Inventory ("Item Name",Value,Quantity)
                values (?,?,?)''', [ item[0], item[1], 1 ])

        self.db.commit()
        curs.close()

    
    def item_in_db(self, item):
        curs = self.db.cursor()

        curs.execute('''select "Item Name", Value, Quantity from Inventory where
            "Item Name" = ? and Value = ?''',[ item[0], item[1] ])
        item = curs.fetchone()
    
        self.db.commit()
        curs.close()

        return item
        