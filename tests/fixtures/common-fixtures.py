import pytest
from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler
from procurement_bytetheory.model.Business import Business
from procurement_bytetheory.model.Inventory import Inventory
from procurement_bytetheory.model.Market import Market
from procurement_bytetheory.model.Item import Item

@pytest.fixture
def baseEnvironment():
    DatabaseHandler.truncateTables()
    Business.numBusinesses = 0
    Inventory.numInventories = 0
    Market.numMarkets = 0
    Item.itemCount = 0

