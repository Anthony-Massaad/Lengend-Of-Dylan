import pygame

class Inventory:

    def __init__(self, items={}):
        self.items = items
    
    def add_to_item(self, item, quantity):
        self.items[item] += quantity
    
    def remove_from_item(self, item, quantity):
        self.items[item] -= quantity
    
    def add_item(self, item, quantity):
        if self.items.get(item) is None: 
            self.items[item] = quantity
            return
        self.add_to_item(item, quantity)
    
    def remove_item(self, item, quantity):
        if self.items[item] <= quantity:
            del self.items[item]
            return
        self.remove_from_item(item, quantity)

