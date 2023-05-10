import pytest
from procurement_bytetheory.db_connectors.DatabaseHandler import DatabaseHandler
from procurement_bytetheory.controllers.UIController import UIController

class MockView:
    def update(self, message, payload):
        if message:
            print("message", message)
            print("payload", payload)
        else:
            print("Updated with no message.")
            
@pytest.fixture
def instantiatedController():
    controller = UIController()
    controller.setView(MockView())
    yield controller

@pytest.fixture
def controllerWithBusinessCreated(baseEnvironment, instantiatedController):
    instantiatedController.createBusiness("ACME Innovations", 500)
    yield instantiatedController

@pytest.fixture
def seededController(controllerWithBusinessCreated):
    controllerWithBusinessCreated.seedMarket()
    yield controllerWithBusinessCreated