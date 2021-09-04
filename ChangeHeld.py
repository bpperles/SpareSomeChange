# ChangeHeld.py
# Set of objects that can be carried by the player or zerks

# Imported libraries
import arcade

# If a holdable object gets lose, it may fall off the screen
GRAVITY = -.5

# Base class
class Holdable(arcade.Sprite):
    def __init__(self, filename, scaling):
        # Object variables
        super().__init__(filename, scaling)
        
        self.gravity = 0
        self.type = "Undefined"
    # end init
    
    def update(self):
        
        # GRAVITY
        self.change_y += self.gravity
        
        self.center_x += self.change_x
        self.center_y += self.change_y
    
    # end update

    def GetType(self):
        return self.type
    # end GetType

# end Holdable

# The main collectable
class Token(Holdable):
    def __init__(self):
        # Object variables
        scale = .25
        # 64 x 64
        super().__init__("Resources/Token.png", scale)
        
        self.type = "Token"
   # end init
    
    def update(self):
        super().update()
    # end update
    
    def Fall(self):
        self.gravity = GRAVITY
    # end Fall
    
# end Token

# For recharging token machines
class Bill(Holdable):
    def __init__(self):
        # Object variables
        scale = .5
        super().__init__("Resources/Bill.png", scale)
        
        self.type = "Bill"
   # end init
    
    def update(self):
        super().update()
    # end update
    
    def Fall(self):
        self.gravity = GRAVITY
    # end Fall
    
# end Bill

# For recharging the cash register
class Bag(Holdable):
    def __init__(self):
        # Object variables
        scale = .5
        filename = "Resources/Bag.png"
        super().__init__(filename, scale)
        
        self.type = "Bag"
   # end init
    
    def update(self):
        super().update()
    # end update
    
    def Fall(self):
        self.gravity = GRAVITY
    # end Fall
    
# end Bag
