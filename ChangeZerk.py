# ChangeZerk.py
# The 'enemy' character

# Imported libraries
import arcade

# Local Libraries
import ChangeHeld
import ChangeMachine
import ChangeUtils

# Currently using the zombee texture
# 96x128
ZERK_SPRITE_SIZE_X = 96
ZERK_GOAL_SIZE_X = 48


class Zerk(arcade.Sprite):
    def __init__(self):
        # Object variables
        filename = "Resources/zombie_idle.png"
        scale = ZERK_GOAL_SIZE_X / ZERK_SPRITE_SIZE_X
        super().__init__(filename, scale)

        # limited to one object
        self.HeldObjectSpriteList = arcade.SpriteList()
    
        # Place that zerk wants to get to
        self.targetMachine = None
        self.targetPort = None
        self.targetX = 0
        self.targetY = 0

        # If something grabs the zerks attension
        self.isDistracted = False
        self.distractedBy = None
    # end init

    # Allow the zerk to pick a new goal
    def PickTarget(self, machineSpriteList):
        self.targetMachine = None
        self.targetPort = None
        
        GoToBank = False
        
        # If carrying a token, go directly to the Zerk Bank
        if self.IsCarrying() and "Token" == self.GetCarryingType():
            # If carrying a token, there is a 50% chance of going directly to the zerk bank
            chance = ChangeUtils.myRandom(2)
            if 0 == chance:
                GoToBank = True
            
        if GoToBank:
            for machine in machineSpriteList:
                if type(machine) is ChangeMachine.EnemyTokenBin:
                    foundGivePort = machine.GetGivePort()
                    if None != foundGivePort:
                        if foundGivePort.enemy:
                            valList = foundGivePort.GetEnemyDock()
                            if 2 <= len(valList):
                                self.targetX = valList[0]
                                self.targetY = valList[1]
                                self.targetMachine = machine
                                self.targetPort = foundGivePort
        else:
            # Pick a random machine and go there
            pick = ChangeUtils.myRandom(len(machineSpriteList))
            foundMachine = machineSpriteList[pick]
            if None != foundMachine:
                # Try and go to the take port
                foundTakePort = foundMachine.GetTakePort()
                if None != foundTakePort:
                    if foundTakePort.enemy:
                        valList = foundTakePort.GetEnemyDock()
                        if 2 <= len(valList):
                            self.targetX = valList[0]
                            self.targetY = valList[1]
                            self.targetMachine = foundMachine
                            self.targetPort = foundTakePort
                
                # if not yet succeeded, try and go to the give port
                if None == self.targetMachine:
                    foundGivePort = foundMachine.GetGivePort()
                    if None != foundGivePort:
                        if foundGivePort.enemy:
                            valList = foundGivePort.GetEnemyDock()
                            if 2 <= len(valList):
                                self.targetX = valList[0]
                                self.targetY = valList[1]
                                self.targetMachine = foundMachine
                                self.targetPort = foundGivePort
    # end PickTarget

    def InteractWithMachine(self, port):
        if None != port:
            if "Give" == port.type:
                if 0 < len(self.HeldObjectSpriteList):
                    obj = self.HeldObjectSpriteList.pop()
                    rc = port.EnemyGive(obj)
                    if False == rc:
                        # Give failed, keep the object
                        self.HeldObjectSpriteList.append(obj)
            elif "Take" == port.type:
                if 0 == len(self.HeldObjectSpriteList):
                    obj = port.EnemyTake()
                    if None != obj:
                        self.HeldObjectSpriteList.append(obj)
    # end InteractWithMachine(

    # NOT CALLED WHEN USING PHYISCS ENGINE!!!!
    def UpdateZerk(self):
        # For now, just make the zerk move towards its target point
        speed = 1
        self.CheckDistraction()
        if None != self.targetMachine:
            sqrDist = pow(self.center_x - self.targetX, 2) + pow(self.center_y - self.targetY, 2)
            if (2*2) > sqrDist:
                # Reached target, clear target (seperate call will choose new target
                self.InteractWithMachine(self.targetPort)
                self.targetMachine = None
            else:
                # Move towards target
                if self.center_x < self.targetX:
                    self.center_x += speed
                else:
                    self.center_x -= speed
                if self.center_y < self.targetY:
                    self.center_y += speed
                else:
                    self.center_y -= speed
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

    def CheckDistraction(self):
        if self.isDistracted and None != self.distractedBy:
            if False == self.distractedBy.IsDistracting():
                self.isDistracted = False
                self.distractedBy = None
    # end CheckDistraction

# end Zerk
