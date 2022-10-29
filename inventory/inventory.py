import pygame

class Inventory:

    def __init__(self, items={}):
        self.items = items
    
    def add_to_item(self, item, quantity):
        self.items[item] += quantity
    
    def remove_from_item(self, item, quantity):
        self.items[item] -= quantity
    
    def add_item(self, item, quantity):
        """
        for inventory_item in self.items.keys():
            if inventory_item.check_equals(item):
                self.add_to_item(inventory_item, quantity)
                return"""
        self.items[item] = quantity
    
    def remove_item(self, item, quantity):
        for inventory_item in self.items.keys():
            if inventory_item.check_equals(item):
                if self.items[inventory_item] <= quantity:
                    del self.items[inventory_item]
                else:
                    self.remove_from_item(inventory_item, quantity)
                return
    
    def get_keys(self):
        return self.items.keys()
    
    

