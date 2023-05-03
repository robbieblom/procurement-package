from procurement_bytetheory.controllers.Observer import Observer
from procurement_bytetheory.model.Business import Business


class UIController(Observer):
    def __init__(self):
        super().__init__()
        self.view = None
        self.business = None

    def setView(self, view):
        self.view = view

    def setBusiness(self, business):
        self.business = business

    def update(self, message=""):
        self.view.update(message)

    def createBusiness(self, name, moneyAmount):
        newBusiness = Business(name, moneyAmount)
        newBusiness.attachObserver(self)
        newBusiness.save()
        newBusiness.notifyObservers("Business created")
        self.setBusiness(newBusiness)

    def seedMarket(self):
        self.business.market.seedMarket()
        self.business.market.save()

    def buyCheapest(self, itemName=None):
        self.business.buyCheapest(itemName)
        self.business.save()

    def buyAsManyAsPossible(self, itemName=None):
        self.business.buyAsManyAsPossible(itemName)
        self.business.save()

    def sellItem(self, itemName=None):
        self.business.sellItem(itemName)
        self.business.save()

    def liquidateInventory(self):
        self.business.liquidateInventory()
        self.business.save()
