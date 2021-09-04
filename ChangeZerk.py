# ChangeZerk.py
# The 'enemy' character

# Imported libraries
import arcade

# Local Libraries
import ChangeHeld
import ChangeMachine
import ChangePathFinding
import ChangeUtils

# Currently using the zombee texture
# 96x128
ZERK_SPRITE_SIZE_X = 96
ZERK_GOAL_SIZE_X = 48

#ZERK_SPEED = 1
ZERK_SPEED = 2

SLOP = 0

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
        
        self.pathFinder = None
        self.animator = None
        
        self.defaultTexture = arcade.load_texture('Resources/zombie_idle.png')
        self.reachTextureList = []
        self.reachTextureList.append(arcade.load_texture('Resources/zombie_jump.png'))
        
    # end init
    
    def InitPathfinder(self, wallList, minX, maxX, minY, maxY):
        # Pathfinding is not pefect.
        # The larger the grid size, the more the agent will overlap the walls.
        # The smaller value, the most likely the finder will fail to find a path.
#        gridSize = 8
        gridSize = 32
        self.pathFinder = ChangePathFinding.ZerkPathFinder(self, wallList, minX, maxX, minY, maxY, gridSize)
    # end InitPathfinder

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
                                self.pathFinder.ComputeForPort(self.targetPort)
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
                            self.pathFinder.ComputeForPort(self.targetPort)
                
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
                                self.pathFinder.ComputeForPort(self.targetPort)
    # end PickTarget

    def InteractWithMachine(self, port):
        if None != port:
            if "Give" == port.type:
                if 0 < len(self.HeldObjectSpriteList):
                    obj = self.HeldObjectSpriteList.pop()
                    rc = port.EnemyGive(obj)
                    self.ReachAnimation()
                    if False == rc:
                        # Give failed, keep the object
                        self.HeldObjectSpriteList.append(obj)
            elif "Take" == port.type:
                if 0 == len(self.HeldObjectSpriteList):
                    obj = port.EnemyTake()
                    self.ReachAnimation()
                    if None != obj:
                        self.HeldObjectSpriteList.append(obj)
    # end InteractWithMachine(

    # NOT CALLED WHEN USING PHYISCS ENGINE!!!!
    def UpdateZerk(self):
        # For now, just make the zerk move towards its target point
        speed = ZERK_SPEED
        self.CheckDistraction()
        if None != self.targetMachine:
            # Move by pathfinder
            pathTarget = self.pathFinder.GetNextTarget(self.center_x, self.center_y)
            if pathTarget:
                #print('moving towards path target')
                # Move towards path target
                if speed >= abs(self.center_x - pathTarget[0]):
                    self.center_x = pathTarget[0]
                elif self.center_x < pathTarget[0]:
                    self.center_x += speed
                else:
                    self.center_x -= speed
                if speed >= abs(self.center_y - pathTarget[1]):
                    self.center_y = pathTarget[1]
                elif self.center_y < pathTarget[1]:
                    self.center_y += speed
                else:
                    self.center_y -= speed
            else:
                sqrDist = pow(self.center_x - self.targetX, 2) + pow(self.center_y - self.targetY, 2)
                if (2*2) > sqrDist:
                    # Reached target, clear target (seperate call will choose new target
                    self.InteractWithMachine(self.targetPort)
                    self.targetMachine = None
                else:
                    # Move towards target
                    if speed >= abs(self.center_x - self.targetX):
                        self.center_x = self.targetX
                    elif self.center_x < self.targetX:
                        self.center_x += speed
                    else:
                        self.center_x -= speed
                    if speed >= abs(self.center_y - self.targetY):
                        self.center_y = self.targetY
                    elif self.center_y < self.targetY:
                        self.center_y += speed
                    else:
                        self.center_y -= speed
        if self.animator:
            self.animator.update()
    # end update

    def DrawHeldObject(self):
        if 0 < len(self.HeldObjectSpriteList):
            heldObject = self.HeldObjectSpriteList[0]
            if None != heldObject:
                heldObject.center_x = self.center_x
                heldObject.center_y = self.center_y-10
            self.HeldObjectSpriteList.draw()
        
        # Debug
        #self.pathFinder.DrawPath()
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

    def ReachAnimation(self):
        # Starts automatically
        self.animator = ChangeUtils.SpriteAnimator(self, self.defaultTexture, self.reachTextureList, 10, 10)
    # end ReachAnimation

# end Zerk
