from procurement_bytetheory.controllers.UIController import UIController
from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler


class MockView:
    def update(self, message, payload):
        if message:
            print("message", message)
            print("payload", payload)
        else:
            print("Updated with no message.")


def main():
    DatabaseHandler.truncateTables()

    # this will be how the frontend calls the package
    controller = UIController()
    controller.setView(MockView())

    controller.createBusiness("ACME Innovations", 500)
    controller.seedMarket()
    # controller.buyItemById(1)
    # controller.buyCheapest(itemName=None)
    # controller.buyCheapest(itemName="desk")
    # controller.buyCheapest(itemName="table")
    # controller.buyAsManyAsPossible(itemName=None)
    # controller.buyAsManyAsPossible(itemName="desk")
    controller.buyAsManyAsPossible()
    # controller.sellItem(itemName=None)
    # controller.sellItem(itemName="table")
    # controller.liquidateInventory()


if __name__ == "__main__":
    main()
