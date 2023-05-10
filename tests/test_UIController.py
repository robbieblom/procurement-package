from procurement_bytetheory.model.Item import Item

class TestUIController:
    def test_buyItemById_itemRemovedFromMarket(self, seededController):
        newItem = Item("test_item", 100, id=100)
        seededController.business.market.addItemToMarket(newItem)
        seededController.business.market.save()

        seededController.buyItemById(100)
        assert newItem not in seededController.business.market.items
        # assert 4 == len(seededController.business.market.items)

    def test_buyItemById_itemAddedToInventory(self, seededController):
        newItem = Item("test_item", 100, id=100)
        seededController.business.market.addItemToMarket(newItem)
        seededController.business.market.save()
        seededController.business.inventory.save()

        seededController.buyItemById(100)
        assert newItem in seededController.business.inventory.items

    # def test_buyItemById_businessMoneyAmountDecreases(self, seededController):
    #     newItem = Item("test_item", 100, id=100)
    #     seededController.business.market.addItemToMarket(newItem)
    #     seededController.business.market.save()
    #     seededController.business.save()

    #     seededController.buyItemById(100)
    #     assert seededController.business.moneynewItem in seededController.business.inventory.items