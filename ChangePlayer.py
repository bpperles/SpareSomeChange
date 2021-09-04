# ChangePlayer.py
# The sprite for the player character

# Imported libraries
import arcade

# Local Libraries
import ChangeHeld
import ChangeUtils

class Player(arcade.Sprite):
    def __init__(self, x, y):
        # Object variables
        # This sprite fills the whole image, so its calculated bounding box matches its actual size
        # (If the bounding box is different than the sprite size, the player's center does not line up with the port interaction zones.)
        # 96 x 128
        filename = "Resources/femalePerson_idle_expanded.png"
        #filename = "Resources/femalePerson_idle.png"
        
        scale = .5
        super().__init__(filename, scale)
        
        self.center_x = x
        self.center_y = y
        
        # Limited to one object
        self.HeldObjectSpriteList = arcade.SpriteList()
    
        self.animator = None
        
        self.defaultTexture = arcade.load_texture('Resources/femalePerson_idle_expanded.png')
        #self.defaultTexture = arcade.load_texture('Resources/femalePerson_idle.png')
        self.reachTextureList = []
        #self.reachTextureList.append(arcade.load_texture('Resources/femalePerson_jump_expanded.png'))
        self.reachTextureList.append(arcade.load_texture('Resources/femalePerson_reach_expanded.png'))
        #self.reachTextureList.append(arcade.load_texture('Resources/femalePerson_jump.png'))
    
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
        
        if self.animator:
            self.animator.update()
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
        self.ReachAnimation()
    # end RecieveObject

    def GiveObject(self):
        if True == self.IsCarrying():
            self.ReachAnimation()
            return self.HeldObjectSpriteList.pop()
        return None
    # end RecieveObject

    def ReachAnimation(self):
        # Starts automatically
        self.animator = ChangeUtils.SpriteAnimator(self, self.defaultTexture, self.reachTextureList, 10, 10)
    # end ReachAnimation

# end Player
