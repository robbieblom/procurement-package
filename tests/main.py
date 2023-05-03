from procurement_bytetheory.controllers.UIController import UIController
from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler


class MockView:
    def update(self, message):
        if message:
            print(message)
        else:
            print("Updated with no message.")

def main():
    DatabaseHandler.truncateTables()

    # this will be how the frontend calls the package
    controller = UIController()
    controller.setView(MockView())

    controller.createBusiness("ACME Innovations", 500)
    controller.seedMarket()
    # controller.buyCheapest(itemName=None)
    # controller.buyCheapest(itemName='desk')
    # controller.buyAsManyAsPossible(itemName=None)
    controller.buyAsManyAsPossible(itemName='desk')
    # controller.sellItem()
    # controller.liquidateInventory()


if __name__ == "__main__":
    main()
