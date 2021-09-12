# ChangeMachine.py
# Library that defines all the machines:
#    Static objects that moving agents can interact with

# Imported libraries
import arcade
import random

# Local Libraries
import ChangeHeld
import ChangeUtils

# Define how big the area is that the player has to stand in to be able to interact with a port
PLAYER_SLOP = 3
AVAILABLE_PERCENT = .7

# A port allows an agent to interact with a machine.
class Port():
    def __init__(self):
        # Player Action: Give, Take, Distract, Special
        self.type = "Undefined"
        #  Agents that can interact with the port
        self.player = False
        self.enemy = False
        # Interaction Direction: Up, Right, Down, Left (Direction the player must move to interact with the port)
        self.direction = "Undefined"
        # Object Transfered: Token, Bill, Bag
        self.objectType = "Undefined"

        # Area the player must be standing in
        self.playerDockMinX = 0
        self.playerDockMaxX = 0
        self.playerDockMinY = 0
        self.playerDockMaxY = 0
        
        # Point the zerk wants to walk to (and how close to the point they must get)
        self.enemyDockX = 0
        self.enemyDockY = 0
        self.enemyDockSlop = 0

        # Machine that owns the port
        self.sourceMachine = None
    # end init

    def IsPlayerDocked(self, px, py):
        #print(f'player {px}, {py}')
        #print(f'X {self.playerDockMinX}, {self.playerDockMaxX}')
        #print(f'Y {self.playerDockMinY}, {self.playerDockMaxY}')
        if self.playerDockMinX <= px and px <= self.playerDockMaxX and self.playerDockMinY <= py and py <= self.playerDockMaxY:
            return True
        return False
    # end IsPlayerDocked

    def GetEnemyDock(self):
        rv = []
        rv.append(self.enemyDockX)
        rv.append(self.enemyDockY)
        return rv
    # end GetEnemyDock

    def PlayerGive(self, obj):
        rc = False
        if None != self.sourceMachine:
            rc = self.sourceMachine.PlayerGive(obj)
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        if None != self.sourceMachine:
            obj = self.sourceMachine.PlayerTake()
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        if None != self.sourceMachine:
            rc = self.sourceMachine.EnemyGive(obj)
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        if None != self.sourceMachine:
            obj = self.sourceMachine.EnemyTake()
        return obj
    # end PlayerTake

    def DoSpecial(self):
        msg = ""
        if None != self.sourceMachine:
            msg = self.sourceMachine.DoSpecial()
        return msg

    # Debug: Draw the player area and zerk point
    def DrawPort(self):
        if self.player:
            arcade.draw_lrtb_rectangle_filled(self.playerDockMinX, self.playerDockMaxX, self.playerDockMaxY, self.playerDockMinY, arcade.color.SKY_BLUE)

        if self.enemy:
            arcade.draw_circle_filled(self.enemyDockX, self.enemyDockY, self.enemyDockSlop, arcade.color.RED)
            # print(f'{self.enemyDockX}, {self.enemyDockY}, {self.enemyDockSlop}')
    # end DrawPort

    # Draw an arrow that points to the active side of the machine
    def DrawHelper(self):
        strip = []
        if "Up" == self.direction:
            strip.append((self.playerDockMinX, self.playerDockMinY))
            strip.append(((self.playerDockMinX+self.playerDockMaxX)/2, self.playerDockMaxY))
            strip.append((self.playerDockMaxX, self.playerDockMinY))
        if "Down" == self.direction:
            strip.append((self.playerDockMinX, self.playerDockMaxY))
            strip.append(((self.playerDockMinX+self.playerDockMaxX)/2, self.playerDockMinY))
            strip.append((self.playerDockMaxX, self.playerDockMaxY))
        if "Left" == self.direction:
            strip.append((self.playerDockMaxX, self.playerDockMinY))
            strip.append((self.playerDockMinX,(self.playerDockMinY+self.playerDockMaxY)/2))
            strip.append((self.playerDockMaxX, self.playerDockMaxY))
        if "Right" == self.direction:
            strip.append((self.playerDockMinX, self.playerDockMinY))
            strip.append((self.playerDockMaxX,(self.playerDockMinY+self.playerDockMaxY)/2))
            strip.append((self.playerDockMinX, self.playerDockMaxY))

        arcade.draw_line_strip(strip, arcade.color.GRAY, 2)
    # end DrawHelper

# end Port

# An static object that has ports that agents interact with
class BaseMachine(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.givePort = None
        self.takePort = None
        self.specialPort = None
        self.displayPortHelper = False
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def GetSpecialPort(self):
        return self.specialPort
    # end GetSpecialPort

    def PlayerGive(self, obj):
        rc = False
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        return obj
    # end PlayerTake

    def DoSpecial(self):
        msg = ""
        return msg
    # end DoSpecial

    def Fill(self):
        x = 1
    # end Fill

    def DrawMachine(self):
        
        if True == self.displayPortHelper:
            if None != self.givePort:
                self.givePort.DrawHelper()
            if None != self.takePort:
                self.takePort.DrawHelper()
            if None != self.specialPort:
                self.specialPort.DrawHelper()
            
        
        # Debug
        drawPorts = False
        if drawPorts:
            # Debug: Draw the ports
            if None != self.givePort:
                self.givePort.DrawPort()
            if None != self.takePort:
                self.takePort.DrawPort()
            if None != self.specialPort:
                self.specialPort.DrawPort()
    # end DrawMachine
    
    def UpdateMachine(self):
        x = 1
    # end UpdateMachine

# end BaseMachine

# Machine that gives tokens and takes bills to rechange
class TokenMachine(BaseMachine):
    def __init__(self, x, y, billTakeDirection, playerWidth, playerHeight):
        filename = "Resources/TokenMachine1.png"
        if "Right" == billTakeDirection:
            filename = "Resources/TokenMachine2.png"
        scale = 1
        super().__init__(filename, scale)

        self.center_x = x
        self.center_y = y

        self.heldTokenSpriteList = arcade.SpriteList()
        self.heldTokenMax = 2
        self.displayHeldToken = True
        
        # Todo: Can only be recharged so many times
        
        self.givePort = Port()
        self.takePort = Port()
        
        # ------ Agent Give Port -----------
        self.givePort.type = "Give"
        self.givePort.player = True
        self.givePort.enemy = False
        self.givePort.direction = billTakeDirection
        self.givePort.objectType = "Bill"
        
        # Reach to the right or left
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myLeftX = self.left
        myRightX = self.right
        myCenterY = self.center_y

        # Player Reach to the right or left
        if ("Left" == self.givePort.direction):
            self.givePort.playerDockMinX = myRightX + (playerWidth / 2) - PLAYER_SLOP
            self.givePort.playerDockMaxX = myRightX + (playerWidth / 2) + PLAYER_SLOP
            self.givePort.playerDockMinY = myCenterY - (subHeight / 2)
            self.givePort.playerDockMaxY = myCenterY + (subHeight / 2)
        else:
            self.givePort.playerDockMinX = myLeftX - (playerWidth / 2) - PLAYER_SLOP
            self.givePort.playerDockMaxX = myLeftX - (playerWidth / 2) + PLAYER_SLOP
            self.givePort.playerDockMinY = myCenterY - (subHeight / 2)
            self.givePort.playerDockMaxY = myCenterY + (subHeight / 2)

        # N/A
        self.givePort.enemyDockX = 0
        self.givePort.enemyDockY = 0
        self.givePort.enemyDockSlop = 0
        
        self.givePort.sourceMachine = self
        
        # ------ Agent Take Port -----------
        self.takePort.type = "Take"
        self.takePort.player = True
        self.takePort.enemy = True
        self.takePort.direction = "Up"
        self.takePort.objectType = "Token"
        
        # Reach Up
        width = self.right - self.left
        subWidth = width * AVAILABLE_PERCENT
        myCenterX = self.center_x
        myBottomY = self.bottom

        # Player Reach Up
        self.takePort.playerDockMinX = myCenterX - (subWidth / 2)
        self.takePort.playerDockMaxX = myCenterX + (subWidth / 2)
        self.takePort.playerDockMinY = myBottomY - (playerHeight / 2) - PLAYER_SLOP
        self.takePort.playerDockMaxY = myBottomY - (playerHeight / 2) + PLAYER_SLOP
        
        # Enemy Reach Up
        self.takePort.enemyDockX = myCenterX
        self.takePort.enemyDockY = myBottomY - (playerHeight / 2)
        self.takePort.enemyDockSlop = 2
        
        self.takePort.sourceMachine = self
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        # Recieve bill
        rc = False
        if "Bill" == obj.GetType():
            # Don't hold on to the bill
            self.Fill()
            rc = True
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        if 0 < len(self.heldTokenSpriteList):
            obj = self.heldTokenSpriteList.pop()

        # Hack
#        if 0 >= len(self.heldTokenSpriteList):
#            self.Fill()
                   
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        # same logic
        obj = self.PlayerTake()
        return obj
    # end PlayerTake
    
    def Fill(self):
        if self.heldTokenMax > len(self.heldTokenSpriteList):
               for ii in range(len(self.heldTokenSpriteList), self.heldTokenMax):
                   spacing = 20
                   token = ChangeHeld.Token()
                   token.center_x = int(self.center_x - spacing/2 + ii*spacing)
                   token.center_y = int(self.center_y - (self.right-self.left)/4.5)
                   self.heldTokenSpriteList.append(token)
    # end Fill

    def DrawMachine(self):
        super().DrawMachine()
        
        # Draw held objects
        if True == self.displayHeldToken:
            self.heldTokenSpriteList.draw()
    # end DrawMachine

# end TokenMachine

# Place where player can put their tokens (and zerks can steal them).
# If filled up enough, the exit opens.
class PlayerTokenBin(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        filename = "Resources/PlayerTokenBin.png"
        scale = 1
        super().__init__(filename, scale)
        
        self.center_x = x
        self.center_y = y
        
        self.heldTokenSpriteList = arcade.SpriteList()
        self.heldTokenMax = 18
        self.displayHeldToken = True
        
        self.allowZerkToSteal = True
        
        self.givePort = Port()
        self.takePort = Port()
        
        # ------ Agent Give Port -----------
        self.givePort.type = "Give"
        self.givePort.player = True
        self.givePort.enemy = False
        self.givePort.direction = "Down"
        self.givePort.objectType = "Token"
        
        # Reach Down
        width = self.right - self.left
        subWidth = width * AVAILABLE_PERCENT
        myCenterX = self.center_x
        myTopY = self.top

        self.givePort.playerDockMinX = myCenterX - (subWidth / 2)
        self.givePort.playerDockMaxX = myCenterX + (subWidth / 2)
        self.givePort.playerDockMinY = myTopY + (playerHeight / 2) - PLAYER_SLOP
        self.givePort.playerDockMaxY = myTopY + (playerHeight / 2) + PLAYER_SLOP

        # N/A
        self.givePort.enemyDockX = 0
        self.givePort.enemyDockY = 0
        self.givePort.enemyDockSlop = 0
        
        self.givePort.sourceMachine = self
        
        # ------ Agent Take Port -----------
        self.takePort.type = "Take"
        self.takePort.player = False
        self.takePort.enemy = True
        self.takePort.direction = "Up"
        self.takePort.objectType = "Token"

        # Reach Up
        width = self.right - self.left
        subWidth = width * AVAILABLE_PERCENT
        myCenterX = self.center_x
        myBottomY = self.bottom

        # N/A
        self.takePort.playerDockMinX = 0
        self.takePort.playerDockMaxX = 0
        self.takePort.playerDockMinY = 0
        self.takePort.playerDockMaxY = 0
        
        # Enemy Reach Up
        self.takePort.enemyDockX = myCenterX
        self.takePort.enemyDockY = myBottomY - (playerHeight / 2)
        self.takePort.enemyDockSlop = 2
        
        self.takePort.sourceMachine = self
        
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        rc = False
        if "Token" == obj.GetType():
            if len(self.heldTokenSpriteList) < self.heldTokenMax:
                self.AppendToken(obj)
                rc = True
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        # N/A
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        if 0 < len(self.heldTokenSpriteList) and self.allowZerkToSteal:
            obj = self.heldTokenSpriteList.pop()
        return obj
    # end PlayerTake

    # Add a token to the bin and calculate its position to be displayed
    def AppendToken(self, newToken):
        # As tokens are given to the bin, place them in a grid
        self.heldTokenSpriteList.append(newToken)
        self.PositionToken(newToken, len(self.heldTokenSpriteList))
    # end AddToken

    # Calculate and set the position of a token for a given index
    def PositionToken(self, token, index):
        spacing = 15
        # This just works
        size = index-1
        gap = int(size/9)
        row = int(size/3)
        col = size % 3
        #print(f'row = {row}')
        #print(f'col = {col}')
        oX = int(-spacing + col*spacing)
        oY = int(row*spacing + (spacing + 1.4*gap*spacing)) # Center in each of the cubes
        token.center_x = self.center_x + oX
        token.center_y = self.bottom + oY
    # end PositionToken

    def DrawMachine(self):
        super().DrawMachine()

        # Draw held objects
        if True == self.displayHeldToken:
            self.heldTokenSpriteList.draw()
    # end DrawMachine

# end PlayerTokenBin

# A place for zerks to put their tokens.
# If it gets too full, the game is over.
class EnemyTokenBin(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        filename = "Resources/ZerkBank.png"
        scale = 1
        super().__init__(filename, scale)

        self.center_x = x
        self.center_y = y

        self.heldTokenSpriteList = arcade.SpriteList()
        self.heldTokenMax = 9
        self.displayHeldToken = True
        
        self.givePort = Port()
        self.takePort = None
        
        # ------ Agent Give Port -----------
        self.givePort.type = "Give"
        self.givePort.player = False
        self.givePort.enemy = True
        self.givePort.direction = "Down"
        self.givePort.objectType = "Token"

        # Reach Down
        width = self.right - self.left
        subWidth = width * AVAILABLE_PERCENT
        myCenterX = self.center_x
        myTopY = self.top

        # N/A
        self.givePort.playerDockMinX = 0
        self.givePort.playerDockMaxX = 0
        self.givePort.playerDockMinY = 0
        self.givePort.playerDockMaxY = 0
        
        # Enemy Reach Down
        self.givePort.enemyDockX = myCenterX
        self.givePort.enemyDockY = myTopY + (playerHeight / 2)
        self.givePort.enemyDockSlop = 2
        
        self.givePort.sourceMachine = self
        
        self.wiggleCycle = 5
        self.wiggleDuration = 8 * self.wiggleCycle
        
        self.defaultTexture = arcade.load_texture('Resources/ZerkBank.png')
        self.wiggleTextureList = []
        self.wiggleTextureList.append(arcade.load_texture('Resources/ZerkBankB.png'))
        self.wiggleTextureList.append(arcade.load_texture('Resources/ZerkBank.png'))
        self.wiggleAnimator = None
        
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        # N/A
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        if "Token" == obj.GetType():
            if len(self.heldTokenSpriteList) < self.heldTokenMax:
                
                spacing = 15
                # use zero index by getting the size before appending
                size = len(self.heldTokenSpriteList)
                row = int(size/3)
                col = size % 3
                #print(f'row = {row}')
                #print(f'col = {col}')
                oX = int(-spacing + col*spacing)
                oY = int(-spacing + row*spacing)
                obj.center_x = self.center_x + oX
                obj.center_y = self.center_y + oY

                # Starts automatically
                self.wiggleAnimator = ChangeUtils.SpriteAnimator(self, self.defaultTexture, self.wiggleTextureList, self.wiggleDuration, self.wiggleCycle)
                
                self.heldTokenSpriteList.append(obj)
                rc = True
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        # N/A
        return obj
    # end PlayerTake

    def DrawMachine(self):
        super().DrawMachine()

        # Draw held objects
        if True == self.displayHeldToken:
            self.heldTokenSpriteList.draw()
            
        if None != self.wiggleAnimator:
            self.wiggleAnimator.update()
    # end DrawMachine

# end EnemyTokenBin

# A place where the player can get bills.
# It is recharged with money bags.
class CashRegister(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        filename = "Resources/CashReg.png"
        scale = 1
        super().__init__(filename, scale)

        self.center_x = x
        self.center_y = y

        self.heldBillSpriteList = arcade.SpriteList()
        self.heldBillMax = 5
        self.displayHeldBill = True
        
        # Todo: Must be opened before bills can be taken out
        
        self.givePort = Port()
        self.takePort = Port()
        
        # ------ Agent Give Port -----------
        self.givePort.type = "Give"
        self.givePort.player = True
        self.givePort.enemy = False
        self.givePort.direction = "Right"
        self.givePort.objectType = "Bag"
        
        # Reach to the right or left
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myLeftX = self.left
        myCenterY = self.center_y

        # Player Reach to the right
        self.givePort.playerDockMinX = myLeftX - (playerWidth / 2) - PLAYER_SLOP
        self.givePort.playerDockMaxX = myLeftX - (playerWidth / 2) + PLAYER_SLOP
        self.givePort.playerDockMinY = myCenterY - (subHeight / 2)
        self.givePort.playerDockMaxY = myCenterY + (subHeight / 2)

        # N/A
        self.givePort.enemyDockX = 0
        self.givePort.enemyDockY = 0
        self.givePort.enemyDockSlop = 0
        
        self.givePort.sourceMachine = self
        
        # ------ Agent Take Port -----------
        self.takePort.type = "Take"
        self.takePort.player = True
        self.takePort.enemy = False
        self.takePort.direction = "Right"
        self.takePort.objectType = "Bill"
        
        # Reach to the right
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myLeftX = self.left
        myCenterY = self.center_y

        self.takePort.playerDockMinX = myLeftX - (playerWidth / 2) - PLAYER_SLOP
        self.takePort.playerDockMaxX = myLeftX - (playerWidth / 2) + PLAYER_SLOP
        self.takePort.playerDockMinY = myCenterY - (subHeight / 2)
        self.takePort.playerDockMaxY = myCenterY + (subHeight / 2)
        
        # N/A
        self.takePort.enemyDockX = 0
        self.takePort.enemyDockY = 0
        self.takePort.enemyDockSlop = 0
        
        self.takePort.sourceMachine = self
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        # Recieve bag
        rc = False
        if "Bag" == obj.GetType():
            # Don't hold on to the bag
            self.Fill()
            rc = True
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        if 0 < len(self.heldBillSpriteList):
            obj = self.heldBillSpriteList.pop()

        # Hack
#        if 0 >= len(self.heldBillSpriteList):
#            self.Fill()
                   
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        # N/A
        return obj
    # end PlayerTake
    
    def Fill(self):
        if self.heldBillMax > len(self.heldBillSpriteList):
            # As bills are created, display a stack in the 'drawer'
            for ii in range(len(self.heldBillSpriteList), self.heldBillMax):
                spacing = 3
                bill = ChangeHeld.Bill()
                bill.center_x = int(self.center_x - (self.right - self.left)/4)
                bill.center_y = int(self.bottom + (ii+2)*((self.top-self.bottom)/9))
                self.heldBillSpriteList.append(bill)
    # end Fill

    def DrawMachine(self):
        super().DrawMachine()

        # Draw held objects
        if True == self.displayHeldBill:
            self.heldBillSpriteList.draw()
    # end DrawMachine

# end CashRegister

# A place where players can get money bags. (Of which it has an infinite supply.)
class Safe(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        #filename = ":resources:images/tiles/doorClosed_mid.png"
        filename = "resources/Safe.png"
        scale = 1
        super().__init__(filename, scale)

        self.center_x = x
        self.center_y = y

        self.heldBagSpriteList = arcade.SpriteList()
        self.heldBagMax = 99
        self.displayHeldBag = False
        
        # Todo: Must be opened before the user can take.
        
        self.givePort = None
        self.takePort = Port()
        
        # ------ Agent Take Port -----------
        self.takePort.type = "Take"
        self.takePort.player = True
        self.takePort.enemy = False
        self.takePort.direction = "Left"
        self.takePort.objectType = "Bag"
        
        # Reach to the Left
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myRightX = self.right
        myCenterY = self.center_y

        self.takePort.playerDockMinX = myRightX + (playerWidth / 2) - PLAYER_SLOP
        self.takePort.playerDockMaxX = myRightX + (playerWidth / 2) + PLAYER_SLOP
        self.takePort.playerDockMinY = myCenterY - (subHeight / 2)
        self.takePort.playerDockMaxY = myCenterY + (subHeight / 2)
        
        # N/A
        self.takePort.enemyDockX = 0
        self.takePort.enemyDockY = 0
        self.takePort.enemyDockSlop = 0
        
        self.takePort.sourceMachine = self
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        # Infinte supply
        obj = ChangeHeld.Bag()
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        # N/A
        return obj
    # end PlayerTake
    
    def Fill(self):
        # N/A
        x = 1
    # end Fill

    def DrawMachine(self):
        super().DrawMachine()

        # Draw held objects
        if True == self.displayHeldBag:
            self.heldBagSpriteList.draw()
    # end DrawMachine

# end Safe

# A pay phone that sometimes has a token in the change slot.
# Can be linked to a master phone to from a zerk distraction.
class DummyPhone(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        filename = "Resources/Phone.png"
        scale = 1
        super().__init__(filename, scale)
        
        self.center_x = x
        self.center_y = y
        
        self.heldTokenSpriteList = arcade.SpriteList()
        self.heldTokenMax = 1
        self.displayHeldToken = False
        
        self.givePort = None
        self.takePort = Port()
        
        # ------ Agent Take Port -----------
        self.takePort.type = "Take"
        self.takePort.player = True
        self.takePort.enemy = True
        self.takePort.direction = "Up"
        self.takePort.objectType = "Token"

        # Reach Up
        width = self.right - self.left
        subWidth = width * AVAILABLE_PERCENT
        myCenterX = self.center_x
        myBottomY = self.bottom

        # Player Reach Up
        self.takePort.playerDockMinX = myCenterX - (subWidth / 2)
        self.takePort.playerDockMaxX = myCenterX + (subWidth / 2)
        self.takePort.playerDockMinY = myBottomY - (playerHeight / 2) - PLAYER_SLOP
        self.takePort.playerDockMaxY = myBottomY - (playerHeight / 2) + PLAYER_SLOP
        
        # Enemy Reach Up
        self.takePort.enemyDockX = myCenterX
        self.takePort.enemyDockY = myBottomY - (playerHeight / 2)
        self.takePort.enemyDockSlop = 2
        
        self.takePort.sourceMachine = self
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        if 0 < len(self.heldTokenSpriteList):
            obj = self.heldTokenSpriteList.pop()
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        if 0 < len(self.heldTokenSpriteList):
            obj = self.heldTokenSpriteList.pop()
        return obj
    # end PlayerTake

    def Fill(self):
        if self.heldTokenMax > len(self.heldTokenSpriteList):
            chance = ChangeUtils.myRandom(2)
            if 0 == chance:
                token = ChangeHeld.Token()
                token.center_x = int(self.center_x)
                token.center_y = int(self.center_y)
                self.heldTokenSpriteList.append(token)
    # end Fill

    def DrawMachine(self):
        super().DrawMachine()

        # Draw held objects
        if True == self.displayHeldToken:
            self.heldTokenSpriteList.draw()
    # end DrawMachine

# end DummyPhone

# A pay phone that sometimes has a token in the change slot.
# Can be linked to a master phone to from a zerk distraction.
class DriverPhone(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        filename = "Resources/Phone.png"
        scale = 1
        super().__init__(filename, scale)
        
        self.center_x = x
        self.center_y = y
        
        self.heldTokenSpriteList = arcade.SpriteList()
        self.heldTokenMax = 1
        self.displayHeldToken = False
        
        self.pairedPhone = None
        self.isActive = False
        self.isRinging = False
        self.isOffHook = False
        self.isTalking = False
        self.talkCountStart = 30*25
        self.talkCountDown = 0

        self.hungUpTexture = arcade.load_texture('Resources/Phone.png')
        self.ringingTexture = arcade.load_texture('Resources/PhoneC.png')
        self.offHookTexture = arcade.load_texture('Resources/PhoneD.png')
        self.ringingTextureList = []
        self.ringingTextureList.append(self.ringingTexture)
        self.ringingTextureList.append(self.hungUpTexture)
        self.ringCountStart = 5
        self.animator = None

        self.givePort = Port()
        self.takePort = Port()
        self.distractPort1 = Port()
        
        self.dockedZerk1 = None
        
        # ------ Agent Give Port -----------
        self.givePort.type = "Give"
        self.givePort.player = True
        self.givePort.enemy = False
        self.givePort.direction = "Right"
        self.givePort.objectType = "Token"
        
        # Reach to the Left
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myLeftX = self.left
        myCenterY = self.center_y

        self.givePort.playerDockMinX = myLeftX - (playerWidth / 2) - PLAYER_SLOP
        self.givePort.playerDockMaxX = myLeftX - (playerWidth / 2) + PLAYER_SLOP
        self.givePort.playerDockMinY = myCenterY - (subHeight / 2)
        self.givePort.playerDockMaxY = myCenterY + (subHeight / 2)
        
        # N/A
        self.givePort.enemyDockX = 0
        self.givePort.enemyDockY = 0
        self.givePort.enemyDockSlop = 0
        
        self.givePort.sourceMachine = self
        
        # ------ Agent Take Port -----------
        self.takePort.type = "Take"
        self.takePort.player = True
        self.takePort.enemy = True
        self.takePort.direction = "Up"
        self.takePort.objectType = "Token"

        # Reach Up
        width = self.right - self.left
        subWidth = width * AVAILABLE_PERCENT
        myCenterX = self.center_x
        myBottomY = self.bottom

        # Player Reach Up
        self.takePort.playerDockMinX = myCenterX - (subWidth / 2)
        self.takePort.playerDockMaxX = myCenterX + (subWidth / 2)
        self.takePort.playerDockMinY = myBottomY - (playerHeight / 2) - PLAYER_SLOP
        self.takePort.playerDockMaxY = myBottomY - (playerHeight / 2) + PLAYER_SLOP
        
        # Enemy Reach Up
        self.takePort.enemyDockX = myCenterX
        self.takePort.enemyDockY = myBottomY - (playerHeight / 2)
        self.takePort.enemyDockSlop = 2
        
        self.takePort.sourceMachine = self
        
        # ------ Distract Port #1 -----------
        self.distractPort1.type = "Distract"
        self.distractPort1.player = False
        self.distractPort1.enemy = True
        self.distractPort1.direction = "Left"
        self.distractPort1.objectType = "Distract"
        
        # On the right
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myRightX = self.right
        myCenterY = self.center_y

        # N/A
        self.distractPort1.playerDockMinX = 0
        self.distractPort1.playerDockMaxX = 0
        self.distractPort1.playerDockMinY = 0
        self.distractPort1.playerDockMaxY = 0
        
        self.distractPort1.enemyDockX = myRightX + (playerWidth / 2)
        self.distractPort1.enemyDockY = myCenterY
        self.distractPort1.enemyDockSlop = 2
        
        self.distractPort1.sourceMachine = self
    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        rc = False
        if obj:
            self.MakeCall()
            self.Fill()
            rc = True
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        if 0 < len(self.heldTokenSpriteList):
            obj = self.heldTokenSpriteList.pop()
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        if 0 < len(self.heldTokenSpriteList):
            obj = self.heldTokenSpriteList.pop()
        return obj
    # end PlayerTake

    def Fill(self):
        if self.heldTokenMax > len(self.heldTokenSpriteList):
            chance = ChangeUtils.myRandom(2)
            if 0 == chance:
                token = ChangeHeld.Token()
                token.center_x = int(self.center_x)
                token.center_y = int(self.center_y)
                self.heldTokenSpriteList.append(token)
    # end Fill

    def DrawMachine(self):
        super().DrawMachine()

        # Draw held objects
        if True == self.displayHeldToken:
            self.heldTokenSpriteList.draw()
    # end DrawMachine

    def MakeCall(self):
        print('MakeCall')
        if self.pairedPhone:
            if False == self.isActive and False == self.pairedPhone.isActive:
                self.isActive = True
                self.talkCountDown = self.talkCountStart
                self.StartRinging()
                self.pairedPhone.StartRinging()
    # end MakeCall
    
    def IsDistracting(self):
        return self.isActive
    # end IsPlayering
    
    def FillEmptyDistractionPort(self, zerk):
        rp = None
        if None == self.dockedZerk1:
            rp = self.distractPort1
            self.dockedZerk1 = zerk
        elif self.pairedPhone and None == self.pairedPhone.dockedZerk1:
            rp = self.pairedPhone.distractPort1
            self.pairedPhone.dockedZerk1 = zerk
        return rp
    # end FillEmptyDistractionPort

    def GetTimeReminain(self):
        rt = 0
        if self.isActive:
            rt = self.talkCountDown
        elif self.pairedPhone and self.pairedPhone.isActive:
            rt = self.pairedPhone.talkCountDown
        return rt
    # end GetTimeReminain

    def StartRinging(self):
        self.isRinging = True

        # It starts automatically
        # No off time, wait for zerk to get to dock
        self.animator = ChangeUtils.SpriteAnimator(self, self.hungUpTexture, self.ringingTextureList, 100000, self.ringCountStart)
    # end StartRinging
    
    def StopRinging(self):
        self.isRinging = False
        self.animator.Stop()
    # end Stop Ringing

    def HangUp(self):
        self.texture = self.hungUpTexture
        self.isOffHook = False
        self.isTalking = False
    # end HangUp

    def PickUp(self):
        self.StopRinging()
        self.texture = self.offHookTexture
        self.isOffHook = True
        
        # Either phone could be the last one picked up
        if self.pairedPhone and self.pairedPhone.isOffHook:
            if self.isActive:
                self.isTalking = True
            elif self.pairedPhone.isActive:
                self.pairedPhone.isTalking = True
    # end Pickup
    
    def UpdateMachine(self):
        if self.isRinging:
            self.animator.update()
        elif self.isTalking:
            self.talkCountDown -= 1
            if 0 >= self.talkCountDown:
                self.isActive = False
                self.dockedZerk1 = None
                self.HangUp()
                if self.pairedPhone:
                    self.pairedPhone.dockedZerk1 = None
                    self.pairedPhone.HangUp()
    # end UpdateMachine

# end DriverPhone

class ExitDoor(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        filename = "Resources/Exit_Closed.png"
        scale = 1
        super().__init__(filename, scale)
        
        self.center_x = x
        self.center_y = y
        
        self.givePort = None
        self.takePort = None
        self.specialPort = None
        self.inactiveSpecialPort = Port()
        
        self.isOpen = False
        self.openTexture = arcade.load_texture('Resources/Exit_Open.png')
        
        # ------ Special Port (created inactive) -----------
        self.inactiveSpecialPort.type = "Special"
        self.inactiveSpecialPort.player = True
        self.inactiveSpecialPort.enemy = False
        self.inactiveSpecialPort.direction = "Up"
        self.inactiveSpecialPort.objectType = "ExitLevel"
        
        # Reach up
        width = self.right - self.left
        subWidth = width * AVAILABLE_PERCENT
        myCenterX = self.center_x
        myBottomY = self.bottom

        self.inactiveSpecialPort.playerDockMinX = myCenterX - (subWidth / 2)
        self.inactiveSpecialPort.playerDockMaxX = myCenterX + (subWidth / 2)
        self.inactiveSpecialPort.playerDockMinY = myBottomY - (playerHeight / 2) - PLAYER_SLOP
        self.inactiveSpecialPort.playerDockMaxY = myBottomY - (playerHeight / 2) + PLAYER_SLOP

        # N/A
        self.inactiveSpecialPort.enemyDockX = 0
        self.inactiveSpecialPort.enemyDockY = 0
        self.inactiveSpecialPort.enemyDockSlop = 0
        
        self.inactiveSpecialPort.sourceMachine = self
        
    # end init

    def DoSpecial(self):
        msg = "ExitLevel"
        return msg
    # end DoSpecial
    
    def OpenDoor(self):
        if False == self.isOpen:
            self.specialPort = self.inactiveSpecialPort
            self.texture = self.openTexture
            self.isOpen = True
    # end OpenDoor

    def DrawMachine(self):
        super().DrawMachine()
    # end DrawMachine

# end ExitDoor

# I'd like to create a DistractionMachine base class, but I can't justify it.
class JukeBox(BaseMachine):
    def __init__(self, x, y, playerWidth, playerHeight):
        filename = "Resources/JukeBox.png"
        scale = 1
        super().__init__(filename, scale)

        self.center_x = x
        self.center_y = y

        self.givePort = Port()
        self.takePort = None

        self.distractPort1 = Port()
        self.distractPort2 = Port()
        
        self.dockedZerk1 = None
        self.dockedZerk2 = None

        # ------ Agent Give Port -----------
        self.givePort.type = "Give"
        self.givePort.player = True
        self.givePort.enemy = False
        self.givePort.direction = "Left"
        self.givePort.objectType = "Token"
        
        # Reach to the Left
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myRightX = self.right
        myCenterY = self.center_y

        self.givePort.playerDockMinX = myRightX + (playerWidth / 2) - PLAYER_SLOP
        self.givePort.playerDockMaxX = myRightX + (playerWidth / 2) + PLAYER_SLOP
        self.givePort.playerDockMinY = myCenterY - (subHeight / 2)
        self.givePort.playerDockMaxY = myCenterY + (subHeight / 2)
        
        # N/A
        self.givePort.enemyDockX = 0
        self.givePort.enemyDockY = 0
        self.givePort.enemyDockSlop = 0
        
        self.givePort.sourceMachine = self
        
        # ------ Distract Port #1 -----------
        self.distractPort1.type = "Distract"
        self.distractPort1.player = False
        self.distractPort1.enemy = True
        self.distractPort1.direction = "Left"
        self.distractPort1.objectType = "Distract"
        
        # On the right
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myRightX = self.right
        myCenterY = self.center_y

        # N/A
        self.distractPort1.playerDockMinX = 0
        self.distractPort1.playerDockMaxX = 0
        self.distractPort1.playerDockMinY = 0
        self.distractPort1.playerDockMaxY = 0
        
        self.distractPort1.enemyDockX = myRightX + (playerWidth / 2)
        self.distractPort1.enemyDockY = myCenterY
        self.distractPort1.enemyDockSlop = 2
        
        self.distractPort1.sourceMachine = self

        # ------ Distract Port #2 -----------
        self.distractPort2.type = "Distract"
        self.distractPort2.player = False
        self.distractPort2.enemy = True
        self.distractPort2.direction = "Left"
        self.distractPort2.objectType = "Distract"
        
        # Two to the right
        height = self.top - self.bottom
        subHeight = height * AVAILABLE_PERCENT
        myRightX = self.right
        myCenterY = self.center_y

        # N/A
        self.distractPort2.playerDockMinX = 0
        self.distractPort2.playerDockMaxX = 0
        self.distractPort2.playerDockMinY = 0
        self.distractPort2.playerDockMaxY = 0
        
        self.distractPort2.enemyDockX = myRightX + (playerWidth / 2) + .3 * playerWidth + playerWidth  
        self.distractPort2.enemyDockY = myCenterY
        self.distractPort2.enemyDockSlop = 2
        
        self.distractPort2.sourceMachine = self
        
        self.IsPlaying = False
        #self.playCountStart = 30*60
        self.playCountStart = 30*45
        
        self.offTexture = arcade.load_texture('Resources/JukeBox.png')
        self.flashingTextureList = []
        self.flashingTextureList.append(arcade.load_texture('Resources/JukeBoxA.png'))
        self.flashingTextureList.append(arcade.load_texture('Resources/JukeBoxB.png'))
        self.flashCountStart = 10
        self.animator = None

    # end init
    
    def GetGivePort(self):
        return self.givePort
    # end GetGivePort
    
    def GetTakePort(self):
        return self.takePort
    # end GetGivePort

    def PlayerGive(self, obj):
        rc = False
        if None != obj:
            if "Token" == obj.GetType():
                self.StartJukeBox()
                rc = True
        return rc
    # end PlayerGive

    def PlayerTake(self):
        obj = None
        # N/A
        return obj
    # end PlayerTake

    def EnemyGive(self, obj):
        rc = False
        # N/A
        return rc
    # end PlayerGive

    def EnemyTake(self):
        obj = None
        # N/A
        return obj
    # end PlayerTake
    
    def Fill(self):
        # N/A
        x = 1
    # end Fill

    def DrawMachine(self):
        super().DrawMachine()
    # end DrawMachine

    def StartJukeBox(self):
        self.IsPlaying = True
        self.playCountDown = self.playCountStart

        # It starts automatically
        self.animator = ChangeUtils.SpriteAnimator(self, self.offTexture, self.flashingTextureList, self.playCountStart, self.flashCountStart)
    # end StartJukeBox
    
    def IsDistracting(self):
        return self.IsPlaying
    # end IsPlayering
    
    def FillEmptyDistractionPort(self, zerk):
        rp = None
        if None == self.dockedZerk1:
            rp = self.distractPort1
            self.dockedZerk1 = zerk
        elif None == self.dockedZerk2:
            rp = self.distractPort2
            self.dockedZerk2 = zerk
        return rp
    # end FillEmptyDistractionPort

    def GetTimeReminain(self):
        return self.playCountDown
    # end GetTimeReminain

    def UpdateMachine(self):
        if self.IsPlaying:
            self.playCountDown -= 1
            if 0 < self.playCountDown:
                self.animator.update()
            else:
                self.IsPlaying = False
                self.animator.Stop()
                self.animator = None
                self.dockedZerk1 = None
                self.dockedZerk2 = None
    # end UpdateMachine

# end JukeBox
