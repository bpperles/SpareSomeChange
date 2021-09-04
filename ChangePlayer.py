# ChangePlayer.py
# The sprite for the player character

# Imported libraries
import arcade

# Local Libraries
import ChangeHeld

class Player(arcade.Sprite):
    def __init__(self, x, y):
        # Object variables
        # This sprite fills the whole image, so its calculated bounding box matches its actual size
        # (If the bounding box is different than the sprite size, the player's center does not line up with the port interaction zones.)
        filename = "Resources/femalePerson_idle_expanded.png"
        scale = .5
        super().__init__(filename, scale)
        
        self.center_x = x
        self.center_y = y
        
        # Limited to one object
        self.HeldObjectSpriteList = arcade.SpriteList()
    
    # end init
    
    # NOT CALLED WHEN USING PHYISCS ENGINE!!!!
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y    
    # end update

    def DrawHeldObject(self):
        if 0 < len(self.HeldObjectSpriteList):
            heldObject = self.HeldObjectSpriteList[0]
            if None != heldObject:
                heldObject.center_x = self.center_x
                heldObject.center_y = self.center_y-10
            self.HeldObjectSpriteList.draw()
    # end DrawHeldTokens

    def IsCarrying(self):
        if 0 < len(self.HeldObjectSpriteList):
            heldObject = self.HeldObjectSpriteList[0]
            if None != heldObject:
                return True
        return False
    # IsCarrying
    
    def GetCarryingType(self):
        if 0 < len(self.HeldObjectSpriteList):
            heldObject = self.HeldObjectSpriteList[0]
            if None != heldObject:
                return heldObject.GetType()
        return "Empty"
    # end GetCarryingType

    def RecieveObject(self, object):
        while 0 < len(self.HeldObjectSpriteList):
            self.HeldObjectSpriteList.pop()
        # Held object is positioned as a side effect of drawing it
        self.HeldObjectSpriteList.append(object)
    # end RecieveObject

    def GiveObject(self):
        if True == self.IsCarrying():
            return self.HeldObjectSpriteList.pop()
        return None
    # end RecieveObject

# end Player
