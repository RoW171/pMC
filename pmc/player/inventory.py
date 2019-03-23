__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-22"
__version__ = "0.0.1"

__all__ = ['Inventory']


class InventoryBase(list):
    def __init__(self, player):
        super(InventoryBase, self).__init__()
        self.player = player
        self.selectedIndex = 1
        self.selected = None

    def __getitem__(self, item):
        try: return super().__getitem__(item - 1)
        except (IndexError,): pass

    def get(self): return self.selected

    def set(self, index):
        if index <= len(self) and index != self.selectedIndex:
            self.player.game.audio('select')
            self.selectedIndex = index
            self.selected = self[self.selectedIndex]

    def move(self, movement):
        if movement > 0: self.forwards()
        else: self.backwards()

    def forwards(self):
        if self.selectedIndex < len(self): self.set(self.selectedIndex + 1)
        else: self.set(1)

    def backwards(self):
        if self.selectedIndex > 1: self.set(self.selectedIndex - 1)
        else: self.set(len(self))


class CreativeInventory(InventoryBase):
    def __init__(self, player):
        super(CreativeInventory, self).__init__(player)
        textures = self.player.game.textures
        for num, name, in enumerate(textures.inventory): self.append(Slot(self, num + 1, name, 0, textures[name]))
        self.selected = self[self.selectedIndex]

    def update(self): pass

    def cleanup(self): pass

    def addItem(self, tex): pass

    def removeItem(self, tex): pass

    def addSlot(self, tex): pass

    def removeSlot(self, slot): pass


class SurvivalInventory(InventoryBase):
    def __init__(self, player, space=None):
        super(SurvivalInventory, self).__init__(player)
        self.space = space if space is not None else self.player.game.data.gameplay.survival_inventory_space
        self.selected = self[self.selectedIndex]
        # TODO: think about what happens if inventory is empty

    def update(self):
        for slot in self:
            if slot.count == 0: self.removeSlot(slot)

    def cleanup(self):
        nList = []
        for slot in self:
            if slot is not None: nList.append(slot)
        for _ in range(self.space - len(nList)): nList.append(None)
        self.clear()
        self.extend(nList)

    def addItem(self, tex):
        for t in self:
            if t and t.texture == tex:
                t.add()
                return
        else: self.addSlot(tex)

    def removeItem(self, tex=None):
        if tex is None:
            self.selected.remove()
            return
        for t in self:
            if t.texture == tex:
                t.remove()
                return

    def addSlot(self, tex):
        slot = Slot(self, index=0, count=1, texture=tex, name='')
        # if type(slot) != Slot: slot = Slot(*slot)
        if slot in self:
            self.addItem(tex)
            return
        try: index = self.index(None)
        except (ValueError,): return False
        else:
            self[index] = slot
            return True

    def removeSlot(self, slot):
        self[self.index(slot)] = None
        self.cleanup()


Inventory = {
    0: CreativeInventory,
    1: SurvivalInventory
}


class Slot:
    def __init__(self, handler, index, name, count, texture):
        self.handler = handler
        self.index = index
        self.name = name
        self.count = count
        self.texture = texture

    def get(self):
        if isinstance(self.handler, CreativeInventory): return u"\u221E"
        else: return self.count

    def __repr__(self): return self.name

    __str__ = __repr__

    def add(self): self.count += 1

    def remove(self):
        if self.count >= 1: self.count -= 1
        else: self.handler.removeSlot(self)


if __name__ == '__main__': pass
