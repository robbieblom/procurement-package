from PyInquirer import prompt
from FloatValidator import FloatValidator
from Owner import Owner

class ActionsPrompt():
    def __init__(self, owners = {}):
        self.owners = owners

    def ask_action(self):
        actions_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'What would you like to do next?',
            'choices': ['Create owner', 'Buy inventory', 'Sell inventory', 'Check net worth', 'Quit']
        }
        answer = prompt(actions_prompt)
        if(answer['action'] == 'Create owner'):
            return self.create_owner()
        elif(answer['action'] == 'Buy inventory'):
            return self.buy_inventory()
        elif(answer['action'] == 'Sell inventory'):
            return self.sell_inventory()
        elif(answer['action'] == 'Check net worth'):
            return self.check_net_worth()
        elif(answer['action'] == 'Quit'):
            return False
        else:
            return False

    def create_owner(self):
        create_owner_prompt = [
            {
                'type': 'input',
                'name': 'owner_name',
                'message': 'Great! What\'s your owner\'s name?',
            },
            {
                'type': 'input',
                'name': 'money_amount',
                'message': 'How much money does your owner have?',
                'validate': FloatValidator
            }
        ]
        answers = prompt(create_owner_prompt)
        if(answers["owner_name"].lower() == "quit" or answers["money_amount"].lower() == "quit"):
            return False
        else:
            newOwner = Owner(answers["owner_name"], int(answers["money_amount"]))
            self.owners[answers["owner_name"]] = newOwner
            print("Owner created!\n")
            return True

    def buy_inventory(self):
        owner_name = self.which_owner() 
        if(not owner_name): return False

        curs = Owner.db.cursor()
        curs.execute('''select * from Inventory''')
        items = curs.fetchall()
        curs.close()
        items = list( set([ i[0] for i in items] ) )
                
        which_items_prompt = [
            {
                'type': 'list',
                'name': 'which_item(s)',
                'message': 'Which item(s) do you want to buy?',
                'choices': items + ['One of whatever\'s cheapest', 'As many units of the cheapest item as possible', 'Quit']
            }
        ]
        items_answer = prompt(which_items_prompt)
        item_name = items_answer['which_item(s)']

        if(item_name == "One of whatever\'s cheapest"):
            self.owners[owner_name].buy_cheapest()
            return True
        elif(item_name == "As many units of the cheapest item as possible"):
            self.owners[owner_name].buy_all()
            return True
        elif(item_name == "Quit"):
            return False
        else:
            self.owners[owner_name].buy_cheapest(item_name)
            return True

    def sell_inventory(self):
        owner_name = self.which_owner() 
        if(not owner_name): return False

        items = [i[0] for i in self.owners[owner_name].inventory_dict]
        which_items_prompt = [
            {
                'type': 'list',
                'name': 'which_item(s)',
                'message': 'Which item(s) do you want to sell?',
                'choices': items + ['One of whatever has the highest price', 'All of it', 'Quit']
            }
        ]
        items_answer = prompt(which_items_prompt)
        item_name = items_answer['which_item(s)']

        if(item_name == "One of whatever has the highest price"):
            self.owners[owner_name].sell_item()
            return True
        elif(item_name == "All of it"):
            self.owners[owner_name].fire_sale()
            return True
        elif(item_name == "Quit"):
            return False
        else:
            self.owners[owner_name].sell_item(item_name)
            return True

    def check_net_worth(self):
        owner_name = self.which_owner() 
        if(not owner_name): return False
        self.owners[owner_name].net_worth()
        return True

    def which_owner(self):
        which_owner_prompt = [
            {
                'type': 'list',
                'name': 'which_owner',
                'message': 'For which owner?',
                'choices': [ o.name for o in self.owners.values() ] + ['Quit']
                # 'validate': lambda val: val == val not in owners
            }
        ]
        owner_answer = prompt(which_owner_prompt)
        if(owner_answer['which_owner'] == "Quit"):
            return False
        else:
            return owner_answer['which_owner']
