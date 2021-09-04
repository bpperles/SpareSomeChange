# SpaceSomeChange.py
# Inspired by the classic Apple IIe game: 'Spare Change'
# https://en.wikipedia.org/wiki/Spare_Change_(video_game)
# Origionaly created by Dan and Mike Zeller, published in 1983 by Broderbund.
# Created with the Arcade Python library.
# https://api.arcade.academy/en/latest/
# Written to explore:
#   GitHub
#   Creation my own python libraries
#   Arcade Views
#   Collision detection
#   Path finding
# Brian Perles
# Summer 2021

# Imported libraries
import arcade

# Local Libraries
import ChangeMachine
import ChangeHeld
import ChangePlayer
import ChangeZerk
import ChangeUtils


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 96x128
PLAYER_SPRITE_SIZE_X = 96
PLAYER_GOAL_SIZE_X = 48
PLAYER_GOAL_SIZE_Y = 64

# No longer used
# 64x64
WALL_SPRITE_SIZE_X = 64
WALL_GOAL_SIZE_X = 64

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = -.5

# A view for displaying the playable game
class GameView(arcade.View):
    def setup(self):
        print('Setup GameView')
        
        # since __init__() is missing (?) from the view class
        # Sprites I want to find directly
        self.PlayerSprite = None
        self.JukeBoxSprite = None
        self.ZerkBankSprite = None
        
        # Lists of sprites for update and draw
        self.PlayerSpriteList = None
        self.ZerkSpriteList = None
        self.LoseTokenSpriteList = None
        self.MachineSpriteList = None
        self.WallSpriteList = None

        # List of sprites for collision detection
        self.AllWallsSpriteList = None
        
        self.mousex = 0
        self.mousey = 0
        
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.left_last_pressed = False
        self.right_last_pressed = False
        self.up_last_pressed = False
        self.down_last_pressed = False

        # Engine for collision detection
        self.PlayerPhysicsEngine = None
    # end setup
    
    def SetupLevel(self, levelNumber):
        self.PlayerSpriteList = arcade.SpriteList()
        self.ZerkSpriteList = arcade.SpriteList()
        self.LoseTokenSpriteList = arcade.SpriteList()
        self.MachineSpriteList = arcade.SpriteList()
        self.WallSpriteList = arcade.SpriteList()

        self.AllWallsSpriteList = arcade.SpriteList()

        # Build all sprites
        x = .1 * SCREEN_WIDTH
        y = .75 * SCREEN_HEIGHT
        self.PlayerSprite = ChangePlayer.Player(x, y)
        self.PlayerSpriteList.append(self.PlayerSprite)
        
        zerk = ChangeZerk.Zerk()
        zerk.center_x = .6 * SCREEN_WIDTH
        zerk.center_y = .6 * SCREEN_HEIGHT
        self.ZerkSpriteList.append(zerk)

        zerk2 = ChangeZerk.Zerk()
        zerk2.center_x = .8 * SCREEN_WIDTH
        zerk2.center_y = .6 * SCREEN_HEIGHT
        self.ZerkSpriteList.append(zerk2)

        # Left token machine
        x = .1 * SCREEN_WIDTH
        y = .6 * SCREEN_HEIGHT
        tokenMachine1 = ChangeMachine.TokenMachine(x, y, "Left", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        tokenMachine1.Fill()
        self.MachineSpriteList.append(tokenMachine1)
        self.AllWallsSpriteList.append(tokenMachine1)

        # Right top token machine
        x = .75 * SCREEN_WIDTH
        y = .6 * SCREEN_HEIGHT
        tokenMachine3 = ChangeMachine.TokenMachine(x, y, "Left", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        tokenMachine3.Fill()
        self.MachineSpriteList.append(tokenMachine3)
        self.AllWallsSpriteList.append(tokenMachine3)

        # Top token Machine
        x = .45 * SCREEN_WIDTH
        y = .9 * SCREEN_HEIGHT
        tokenMachine2 = ChangeMachine.TokenMachine(x, y, "Right", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        tokenMachine2.Fill()
        self.MachineSpriteList.append(tokenMachine2)
        self.AllWallsSpriteList.append(tokenMachine2)

        # Right bottom token machine
        x = .75 * SCREEN_WIDTH
        y = .3 * SCREEN_HEIGHT
        tokenMachine4 = ChangeMachine.TokenMachine(x, y, "Right", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        tokenMachine4.Fill()
        self.MachineSpriteList.append(tokenMachine4)
        self.AllWallsSpriteList.append(tokenMachine4)

        x = .35 * SCREEN_WIDTH
        y = .5 * SCREEN_HEIGHT
        playerTokenBin = ChangeMachine.PlayerTokenBin(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        self.MachineSpriteList.append(playerTokenBin)
        self.AllWallsSpriteList.append(playerTokenBin)

        x = .9 * SCREEN_WIDTH
        y = .1 * SCREEN_HEIGHT
        enemyTokenBin = ChangeMachine.EnemyTokenBin(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        self.ZerkBankSprite = enemyTokenBin
        self.MachineSpriteList.append(enemyTokenBin)
        self.AllWallsSpriteList.append(enemyTokenBin)
        
        x = .9 * SCREEN_WIDTH
        y = .9 * SCREEN_HEIGHT
        cashRegister = ChangeMachine.CashRegister(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        cashRegister.Fill()
        self.MachineSpriteList.append(cashRegister)
        self.AllWallsSpriteList.append(cashRegister)
        
        x = .1 * SCREEN_WIDTH
        y = .9 * SCREEN_HEIGHT
        safe = ChangeMachine.Safe(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        self.MachineSpriteList.append(safe)
        self.AllWallsSpriteList.append(safe)

        x = .4 * SCREEN_WIDTH
        y = .1 * SCREEN_HEIGHT
        jukeBox = ChangeMachine.JukeBox(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        self.JukeBoxSprite = jukeBox
        self.MachineSpriteList.append(jukeBox)
        self.AllWallsSpriteList.append(jukeBox)

        x = .1 * SCREEN_WIDTH
        y = .3 * SCREEN_HEIGHT
        leftPhone = ChangeMachine.SlavePhone(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        leftPhone.Fill()
        self.MachineSpriteList.append(leftPhone)
        self.AllWallsSpriteList.append(leftPhone)

        x = .55 * SCREEN_WIDTH
        y = .5 * SCREEN_HEIGHT
        exitDoor = ChangeMachine.ExitDoor(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        self.MachineSpriteList.append(exitDoor)
        self.AllWallsSpriteList.append(exitDoor)

        # Ask the physics engine to keep the player out of the walls
        self.PlayerPhysicsEngine = arcade.PhysicsEngineSimple(self.PlayerSprite, self.AllWallsSpriteList)
        
    # end SetupLevel
    
    def on_show(self):
        print('on_show GameView')
        # Called when switching to this view

        self.SetupLevel(1)
        
        arcade.set_background_color(arcade.color.BLACK)
        
        # Control mouse visibility
        self.window.set_mouse_visible(True)
    # end on_show
    
    def on_update(self, delta_time):
        # Calculate speed based on the keys pressed
        self.PlayerSprite.change_x = 0
        self.PlayerSprite.change_y = 0

        # Update player speed based on keyboard input
        if self.up_pressed and not self.down_pressed:
            self.PlayerSprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.PlayerSprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.PlayerSprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.PlayerSprite.change_x = PLAYER_MOVEMENT_SPEED

        # Player - Machine interaction
        # Note: Do 'take' before 'give' so that if a machine has
        # two ports on the same size, the player can't give and take
        # in the same action
        # (The real solution is open/close mode switches on the machine)
        if True == self.up_pressed and False == self.up_last_pressed:
            for mc in self.MachineSpriteList:
                takePort = mc.GetTakePort()
                if None != takePort:
                    self.PlayerPortInteraction(takePort, "Up")
                givePort = mc.GetGivePort()
                if None != givePort:
                    self.PlayerPortInteraction(givePort, "Up")
                    
        if True == self.down_pressed and False == self.down_last_pressed:
            for mc in self.MachineSpriteList:
                takePort = mc.GetTakePort()
                if None != takePort:
                    self.PlayerPortInteraction(takePort, "Down")
                givePort = mc.GetGivePort()
                if None != givePort:
                    self.PlayerPortInteraction(givePort, "Down")
                    
        if True == self.right_pressed and False == self.right_last_pressed:
            for mc in self.MachineSpriteList:
                takePort = mc.GetTakePort()
                if None != takePort:
                    self.PlayerPortInteraction(takePort, "Right")
                givePort = mc.GetGivePort()
                if None != givePort:
                    self.PlayerPortInteraction(givePort, "Right")
                    
        if True == self.left_pressed and False == self.left_last_pressed:
            for mc in self.MachineSpriteList:
                takePort = mc.GetTakePort()
                if None != takePort:
                    self.PlayerPortInteraction(takePort, "Left")
                givePort = mc.GetGivePort()
                if None != givePort:
                    self.PlayerPortInteraction(givePort, "Left")

        # Update record
        self.up_last_pressed = self.up_pressed
        self.down_last_pressed = self.down_pressed
        self.right_last_pressed = self.right_pressed
        self.left_last_pressed = self.left_pressed
        
        # Update the player with the phyics engine
        self.PlayerPhysicsEngine.update()
        
        # Players are updated by the physics engine 
#        for player in self.PlayerSpriteList:
#            player.UpdatePlayer()

        # Have players and zerk interaction
        self.PlayerZerkInteraction()

        for zerk in self.ZerkSpriteList:
            self.ZerkDistractions()
            if None == zerk.targetMachine and False == zerk.isDistracted:
                zerk.PickTarget(self.MachineSpriteList)
            zerk.UpdateZerk()
            
        for token in self.LoseTokenSpriteList:
            token.update()

            # Check for an out of bounds token
            if token.center_x < 0:
                token.remove_from_sprite_lists()
            elif token.center_x > SCREEN_WIDTH:
                token.remove_from_sprite_lists()
            if token.center_y < 0:
                token.remove_from_sprite_lists()
            elif token.center_y > SCREEN_HEIGHT:
                token.remove_from_sprite_lists()

        for machine in self.MachineSpriteList:
            machine.UpdateMachine()
    # end on_update
    
    def on_draw(self):
        # Called each draw cycle
        arcade.start_render()
        
        # Draw textures for sprites
        self.PlayerSpriteList.draw()
        self.ZerkSpriteList.draw()
        self.LoseTokenSpriteList.draw()
        self.MachineSpriteList.draw()
        
        # Draw extra details on objects
        for machine in self.MachineSpriteList:
            machine.DrawMachine()
            
        # Note: This method also updates the position of the held object
        self.PlayerSprite.DrawHeldObject()

        # Note: This method also updates the position of the held object
        for zerk in self.ZerkSpriteList:
            zerk.DrawHeldObject()

    # end on_draw
    
    # Over-ride base class, called when key is pressed
    def on_key_press(self, key, modifiers):
        # https://api.arcade.academy/en/latest/arcade.key.html
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
    # end on_key_press

    # Over-ride base class, called when key is released
    def on_key_release(self, key, modifiers):
        # https://api.arcade.academy/en/latest/arcade.key.html
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            
        self.left_just_pressed = False
        self.right_just_pressed = False
        self.up_just_pressed = False
        self.down_just_pressed = False
    # end on_key_release

    # The player has has performed an interaction motion.
    # We are checking each port on each machine to see
    # if the player is docked and something can be made to happen.
    def PlayerPortInteraction(self, port, direction):
        if direction == port.direction:
            if port.IsPlayerDocked(self.PlayerSprite.center_x, self.PlayerSprite.center_y):
                if "Give" == port.type:
                    if self.PlayerSprite.IsCarrying():
                        obj = self.PlayerSprite.GiveObject()
                        if None != obj:
                            rc = port.PlayerGive(obj)
                            if False == rc:
                                # The machine didn't take it, so the player gets it back
                                self.PlayerSprite.RecieveObject(obj)
                elif "Take" == port.type:
                    if False == self.PlayerSprite.IsCarrying():
                        obj = port.PlayerTake()
                        if None != obj:
                            self.PlayerSprite.RecieveObject(obj)
    # end PlayerPortInteraction

    # Check to see if the player and the zerks can interact
    def PlayerZerkInteraction(self):
        # Allow the player to steal back tokens from the zerk
        if False == self.PlayerSprite.IsCarrying():
            for zerk in self.ZerkSpriteList:
                if zerk.IsCarrying():
                    distSqrt = pow(self.PlayerSprite.center_x - zerk.center_x, 2) + pow(self.PlayerSprite.center_y - zerk.center_y, 2)
                    targetSqrt = pow(PLAYER_GOAL_SIZE_X/2, 2)
                    # print(f'disSqrt = {disSqrt}')
                    # print(f'targetSqrt = {targetSqrt}')
                    if (targetSqrt > distSqrt):
                        print('Steal!')
                        obj = zerk.HeldObjectSpriteList.pop()
                        self.PlayerSprite.HeldObjectSpriteList.append(obj)
    # end PlayerZerkInteraction
    
    # Check if the zerks are distracted by any of the machines
    def ZerkDistractions(self):
        if None != self.JukeBoxSprite:
            if True == self.JukeBoxSprite.IsDistracting():
                for zerk in self.ZerkSpriteList:
                    if False == zerk.isDistracted:
                        port = self.JukeBoxSprite.FillEmptyDistractionPort(zerk)
                        if None != port:
                            valList = port.GetEnemyDock()
                            if 2 <= len(valList):
                                zerk.targetX = valList[0]
                                zerk.targetY = valList[1]
                                zerk.targetMachine = self.JukeBoxSprite
                                zerk.targetPort = port
                                
                                # Todo: Lose carried tokens
                                
                                zerk.isDistracted = True
                                zerk.distractedBy = self.JukeBoxSprite
    # end ZerkDistractions
# end GameView

# Window class (minimal because all the work is done in views)
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)
        # Store the mouse position and speed at each update
        print('__init__ MyGame')
        
    # end __init__

    def setup(self):
        print('setup MyGame')
        nextView = GameView()
        nextView.setup()
        
        self.show_view(nextView)
    # end setup        

# end MyGame

# Main function
def main():
    # Main function
    print(f'Welcome to Spare Some Change')

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "SpareSomeChange")
    window.setup()

    arcade.run()

    print(f'Goodbye')
    
# End main

# If this file is the primary module, call the main function
if __name__ == '__main__': main()
