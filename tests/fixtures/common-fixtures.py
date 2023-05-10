import pytest
from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler

            
@pytest.fixture
def baseEnvironment():
    DatabaseHandler.truncateTables()
