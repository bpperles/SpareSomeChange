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
import ChangeScoringView
import ChangeLevel0
import ChangeLevel2
import ChangeLevel3


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

#PLAYER_MOVEMENT_SPEED = 5
PLAYER_MOVEMENT_SPEED = 3
GRAVITY = -.5


# A view for displaying the playable game
class GameView(arcade.View):
    def __init__(self, gameParam):
        super().__init__()
        self.gameParam = gameParam
    # end init

    # Reset method for this class
    def setup(self):
        print('Setup GameView')
        
        # since __init__() is missing (?) from the view class
        # Sprites I want to find directly
        self.PlayerSprite = None
        self.PlayerTokenBinSprite = None
        self.ExitDoorSprite = None
        self.ZerkBankSprite = None
        
        #self.PathFindingZerk = None
        #self.PathFindingPort = None
        #self.PathFinder = None
        
        # Lists of sprites for update and draw
        self.PlayerSpriteList = None
        self.ZerkSpriteList = None
        self.LoseTokenSpriteList = None
        self.MachineSpriteList = None
        self.PointsSpriteList = None
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
    
    def SetupLevel(self):
        self.PlayerSpriteList = arcade.SpriteList()
        self.ZerkSpriteList = arcade.SpriteList()
        self.LoseTokenSpriteList = arcade.SpriteList()
        self.MachineSpriteList = arcade.SpriteList()
        self.DistractionSpriteSubList = arcade.SpriteList()
        self.PointsSpriteList = arcade.SpriteList()
        self.WallSpriteList = arcade.SpriteList()

        self.AllWallsSpriteList = arcade.SpriteList()
        
        # Loop the levels
        levelToBuild = 0
        maxDefinedLevel = 3
        if 0 < self.gameParam.level:
            if 0 == self.gameParam.level % maxDefinedLevel:
                levelToBuild = maxDefinedLevel
            else:
                levelToBuild = self.gameParam.level % maxDefinedLevel

        if 1 == levelToBuild:
            self.BuildLevel1()
        elif maxDefinedLevel < levelToBuild:
            self.BuildLevel1()
        else:
            if 0 == levelToBuild:
                ChangeLevel0.BuildLevel0(
                    self.gameParam,
                    self.PlayerSpriteList,
                    self.ZerkSpriteList,
                    self.MachineSpriteList,
                    self.DistractionSpriteSubList,
                    self.AllWallsSpriteList)
            elif 2 == levelToBuild:
                ChangeLevel2.BuildLevel2(
                    self.gameParam,
                    self.PlayerSpriteList,
                    self.ZerkSpriteList,
                    self.MachineSpriteList,
                    self.DistractionSpriteSubList,
                    self.AllWallsSpriteList)
            elif 3 == levelToBuild:
                ChangeLevel3.BuildLevel3(
                    self.gameParam,
                    self.PlayerSpriteList,
                    self.ZerkSpriteList,
                    self.MachineSpriteList,
                    self.DistractionSpriteSubList,
                    self.AllWallsSpriteList)

            # Find Unique Objects
            if 0 < len(self.PlayerSpriteList):
                self.PlayerSprite = self.PlayerSpriteList[0]

            for machine in self.MachineSpriteList:
                if type(machine) is ChangeMachine.PlayerTokenBin:
                    self.PlayerTokenBinSprite = machine
                elif type(machine) is ChangeMachine.ExitDoor:
                    self.ExitDoorSprite = machine
                elif type(machine) is ChangeMachine.EnemyTokenBin:
                    self.ZerkBankSprite = machine
        # End else
        
        # Display the player's current points
        # Put a list of point markers, dull or bright
        x = 800
        y = 400
        dy = -50/4
        for ii in range(9):
            point = ChangeHeld.Point(.5)
            point.center_x = x
            point.center_y = y
            
            if ii <= (self.gameParam.points-1):
                point.Bright()
            else:
                point.Dull()
            
            self.PointsSpriteList.append(point)
            
            y += dy
        # end Loop

        # Ask the physics engine to keep the player out of the walls
        self.PlayerPhysicsEngine = arcade.PhysicsEngineSimple(self.PlayerSprite, self.AllWallsSpriteList)

        for zerk in self.ZerkSpriteList:
            zerk.InitPathfinder(self.AllWallsSpriteList, 0,SCREEN_WIDTH,0,SCREEN_HEIGHT)
        
    # end SetupLevel

    def BuildLevel1(self):

        # Build all sprites
        x = .1 * SCREEN_WIDTH
        y = .75 * SCREEN_HEIGHT
        self.PlayerSprite = ChangePlayer.Player(x, y)
        self.PlayerSpriteList.append(self.PlayerSprite)
        
        zerk = ChangeZerk.Zerk()
        zerk.center_x = .45 * SCREEN_WIDTH
        zerk.center_y = .5 * SCREEN_HEIGHT
        self.ZerkSpriteList.append(zerk)

        zerk2 = ChangeZerk.Zerk()
        zerk2.center_x = .65 * SCREEN_WIDTH
        zerk2.center_y = .5 * SCREEN_HEIGHT
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
        self.PlayerTokenBinSprite = ChangeMachine.PlayerTokenBin(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        for ii in range(self.gameParam.tokensFromLastLevel):
            token = ChangeHeld.Token()
            self.PlayerTokenBinSprite.AppendToken(token)
        self.MachineSpriteList.append(self.PlayerTokenBinSprite)
        self.AllWallsSpriteList.append(self.PlayerTokenBinSprite)

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
        self.MachineSpriteList.append(jukeBox)
        self.DistractionSpriteSubList.append(jukeBox)
        self.AllWallsSpriteList.append(jukeBox)

        x = .1 * SCREEN_WIDTH
        y = .3 * SCREEN_HEIGHT
        leftPhone = ChangeMachine.DummyPhone(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        leftPhone.Fill()
        self.MachineSpriteList.append(leftPhone)
        self.AllWallsSpriteList.append(leftPhone)

        x = .55 * SCREEN_WIDTH
        y = .5 * SCREEN_HEIGHT
        self.ExitDoorSprite = ChangeMachine.ExitDoor(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        self.MachineSpriteList.append(self.ExitDoorSprite)
        self.AllWallsSpriteList.append(self.ExitDoorSprite)


    # end BuildLevel1
    
    def on_show(self):
        print('on_show GameView')
        # Called when switching to this view

        self.SetupLevel()
        
        arcade.set_background_color(arcade.color.BLACK)
        
        # Control mouse visibility
        self.window.set_mouse_visible(True)
    # end on_show
    
    def on_update(self, delta_time):
        if "Playing" == self.gameParam.state:
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
                    specialPort = mc.GetSpecialPort()
                    if None != specialPort:
                        self.PlayerPortInteraction(specialPort, "Up")
                        
            if True == self.down_pressed and False == self.down_last_pressed:
                for mc in self.MachineSpriteList:
                    takePort = mc.GetTakePort()
                    if None != takePort:
                        self.PlayerPortInteraction(takePort, "Down")
                    givePort = mc.GetGivePort()
                    if None != givePort:
                        self.PlayerPortInteraction(givePort, "Down")
                    specialPort = mc.GetSpecialPort()
                    if None != specialPort:
                        self.PlayerPortInteraction(specialPort, "Down")
                        
            if True == self.right_pressed and False == self.right_last_pressed:
                for mc in self.MachineSpriteList:
                    takePort = mc.GetTakePort()
                    if None != takePort:
                        self.PlayerPortInteraction(takePort, "Right")
                    givePort = mc.GetGivePort()
                    if None != givePort:
                        self.PlayerPortInteraction(givePort, "Right")
                    specialPort = mc.GetSpecialPort()
                    if None != specialPort:
                        self.PlayerPortInteraction(specialPort, "Right")
                        
            if True == self.left_pressed and False == self.left_last_pressed:
                for mc in self.MachineSpriteList:
                    takePort = mc.GetTakePort()
                    if None != takePort:
                        self.PlayerPortInteraction(takePort, "Left")
                    givePort = mc.GetGivePort()
                    if None != givePort:
                        self.PlayerPortInteraction(givePort, "Left")
                    specialPort = mc.GetSpecialPort()
                    if None != specialPort:
                        self.PlayerPortInteraction(specialPort, "Left")

            # Update record
            self.up_last_pressed = self.up_pressed
            self.down_last_pressed = self.down_pressed
            self.right_last_pressed = self.right_pressed
            self.left_last_pressed = self.left_pressed
            
            # Update the player with the phyics engine
            self.PlayerPhysicsEngine.update()
            
            # Players are updated by the physics engine 
#            for player in self.PlayerSpriteList:
#                player.UpdatePlayer()

            # Have players and zerk interaction
            self.PlayerZerkInteraction()

            for zerk in self.ZerkSpriteList:
                self.ZerkDistractions()
                #if None == zerk.targetMachine and False == zerk.IsDistracted():
                if zerk.IsPickingNewTargets():
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

        # end IsPlaying
        
        # check for exiting the level, game over, and opening the exit door
        self.CheckGameState()
    # end on_update
    
    def on_draw(self):
        # Called each draw cycle
        arcade.start_render()
        
        # Draw textures for sprites
        self.PlayerSpriteList.draw()
        self.ZerkSpriteList.draw()
        self.LoseTokenSpriteList.draw()
        self.MachineSpriteList.draw()
        self.PointsSpriteList.draw()
        
        # Draw extra details on objects
        for machine in self.MachineSpriteList:
            machine.DrawMachine()
            
        # Note: This method also updates the position of the held object
        self.PlayerSprite.DrawHeldObject()

        # Note: This method also updates the position of the held object
        for zerk in self.ZerkSpriteList:
            zerk.DrawHeldObject()

        x = 690
        y = 325
        fontSize = 40
        text = f"Level {self.gameParam.level}"
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize, rotation=90)

        if "Paused" == self.gameParam.state:
            # Overload the screen with a transparent white
            arcade.draw_lrtb_rectangle_filled(left=0,
                                          right=SCREEN_WIDTH,
                                          top=SCREEN_HEIGHT,
                                          bottom=0,
                                          color=arcade.color.WHITE + (200,))            
            x = 220
            y = 300
            fontSize = 100
            text = "Paused"
            arcade.draw_text(text, x, y, arcade.color.BLACK, fontSize)
        elif "GameOver" == self.gameParam.state:
            # Overload the screen with a transparent white
            arcade.draw_lrtb_rectangle_filled(left=0,
                                          right=SCREEN_WIDTH,
                                          top=SCREEN_HEIGHT,
                                          bottom=0,
                                          color=arcade.color.WHITE + (200,))            
            x = 130
            y = 300
            fontSize = 100
            text = "Game Over"
            arcade.draw_text(text, x, y, arcade.color.BLACK, fontSize)
            x = 150
            y = 200
            fontSize = 30
            text = "Press ESC to return to title screen"
            arcade.draw_text(text, x, y, arcade.color.BLACK, fontSize)

    # end on_draw
    
    # Over-ride base class, called when key is pressed
    def on_key_press(self, key, modifiers):
        # https://api.arcade.academy/en/latest/arcade.key.html
        print('keypress')
        if "Paused" == self.gameParam.state:
            print('ispaused')
            self.gameParam.state = "Playing"
        elif "Playing" == self.gameParam.state:
            if key == arcade.key.UP:
                self.up_pressed = True
            elif key == arcade.key.DOWN:
                self.down_pressed = True
            elif key == arcade.key.LEFT:
                self.left_pressed = True
            elif key == arcade.key.RIGHT:
                self.right_pressed = True
            elif key == arcade.key.ESCAPE:
                if "Playing" == self.gameParam.state:
                    self.gameParam.state = "Paused"
            elif key == arcade.key.T:
                if self.PlayerTokenBinSprite:
                    print('Cheater!')
                    token = ChangeHeld.Token()
                    self.PlayerTokenBinSprite.AppendToken(token)
            elif key == arcade.key.L:
                print('Cheater!')
                if self.PlayerTokenBinSprite:
                    self.gameParam.state = "ExitLevel"
                    self.gameParam.level += 1
        elif "GameOver" == self.gameParam.state:
            if key == arcade.key.ESCAPE:
                # Return to title screen
                nextView = WelcomeView(self.gameParam)
                nextView.setup()
                # A view has a pointer to the window that it is displayed in
                self.window.show_view(nextView)
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
                elif "Special" == port.type:
                    msg = port.DoSpecial()
                    if "ExitLevel" == msg:
                        self.gameParam.state = "ExitLevel"
                    
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
                        self.PlayerSprite.ReachAnimation()
                        if False == zerk.IsDistracted():
                            zerk.ThrowTantrum()
    # end PlayerZerkInteraction
    
    # Check if the zerks are distracted by any of the machines
    def ZerkDistractions(self):
        # Bug: If the player restarts the distraction while the zerks are already
        # at the machine, the zerks do not get the new duration.  When their current
        # duration ends, the animation ends, but the machine has not released them,
        # so they stand (still) at the machine till the machine releases them.
        for distraction in self.DistractionSpriteSubList:
            if type(distraction) is ChangeMachine.JukeBox:
                if True == distraction.IsDistracting():
                    for zerk in self.ZerkSpriteList:
                        if False == zerk.IsDistracted():
                            port = distraction.FillEmptyDistractionPort(zerk)
                            if None != port:
                                zerk.BecomeDistracted(distraction, port)
            elif type(distraction) is ChangeMachine.DriverPhone:
                if True == distraction.IsDistracting():
                    for zerk in self.ZerkSpriteList:
                        if False == zerk.IsDistracted():
                            port = distraction.FillEmptyDistractionPort(zerk)
                            if None != port:
                                zerk.BecomeDistracted(distraction, port)
            if type(distraction) is ChangeMachine.PopcornMachine:
                if True == distraction.IsDistracting():
                    for zerk in self.ZerkSpriteList:
                        if False == zerk.IsDistracted():
                            port = distraction.FillEmptyDistractionPort(zerk)
                            if None != port:
                                zerk.BecomeDistracted(distraction, port)
    # end ZerkDistractions
    
    def CheckGameState(self):
        if "ExitLevel" == self.gameParam.state:
            if self.PlayerTokenBinSprite:
                self.gameParam.tokensInBin = len(self.PlayerTokenBinSprite.heldTokenSpriteList)
            nextView = ChangeScoringView.ScoringView(self.gameParam)
            nextView.setup()
            self.window.show_view(nextView)
        elif "Playing" == self.gameParam.state:
            # Open the door if there are enough tokens
            if self.PlayerTokenBinSprite:
                if 10 <= len(self.PlayerTokenBinSprite.heldTokenSpriteList):
                    if self.ExitDoorSprite:
                        if False == self.ExitDoorSprite.isOpen:
                            print('Opening exit door')
                            self.ExitDoorSprite.OpenDoor()
            # Check for Game Over case:
            if self.ZerkBankSprite:
                if self.ZerkBankSprite.IsFull():
                    self.gameParam.state = "GameOver"
        elif "GameOver" == self.gameParam.state:
            # Don't do anything, wait till the user hits a key
            x = 1
    # end CheckGameState
                    
# end GameView

class WelcomeView(arcade.View):
    def __init__(self, gameParam):
        super().__init__()
        self.gameParam = gameParam
        
        print(f'self.gameParam.tokensFromLastLevel = {self.gameParam.tokensFromLastLevel}')
        
    # end init
    
    # Reset method for this class
    def setup(self):
        print('setup WelcomeView')
        # Also called when switching to this view (?)
        self.AllSpriteList = arcade.SpriteList()
    # end setup

    def on_show(self):
        print('on_show WelcomeView')
        x = 100
        y = 300
        player = ChangePlayer.Player(x, y)
        self.AllSpriteList.append(player)
        
        zerk = ChangeZerk.Zerk()
        zerk.center_x = 200
        zerk.center_y = 300
        self.AllSpriteList.append(zerk)

        zerk2 = ChangeZerk.Zerk()
        zerk2.center_x = 300
        zerk2.center_y = 300
        self.AllSpriteList.append(zerk2)
        
        x = 400
        y = 300
        for ii in range(6):
            token = ChangeHeld.Token()
            token.center_x = x
            token.center_y = y
            self.AllSpriteList.append(token)
            x += 50
        
        
        # Called when switching to this view
        arcade.set_background_color(arcade.color.BLACK)
        
        # Control mouse visibility
        self.window.set_mouse_visible(True)
    # den on_show
    
    def on_draw(self):
        # Called each draw cycle
        arcade.start_render()


        x = 200
        y = 500
        fontSize = 50
        text = "Spare Change"
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        x = 200
        y = 400
        fontSize = 30
        text = "Press any key to START"
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        dy = -30

        x = 50
        y = 200
        fontSize = 20
        text = "Instructions:"
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        y += dy
        text = "Move using the arrow keys."
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)
        
        y += dy
        text = "Interact with a machine by standing next to it and tapping toward it."
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        y += dy
        text = "(The side of the machine maters.)"
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        y += dy
        text = "To advance to the next level, accumulate 9 points (awarded on exiting)."
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        y += dy
        text = "Don't let the Zerks get all the tokens!"
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        '''
        dy = -30
        fontSize = 20
        
        y += dy
        text = "Protect your garden from the rabbits using snowball throwing gnomes!"
        arcade.draw_text(text, x, y, arcade.color.BLACK, fontSize)
        y += dy
        '''
        
        self.AllSpriteList.draw()

    # end on_draw
    
    def on_key_press(self, key, modifiers):
        # https://api.arcade.academy/en/latest/arcade.key.html
        # Toggle views when any key is pressed,

        # Use number presses to pick the level.
        # Support the numbers on the keyboard and the number pad
        if key == arcade.key.NUM_0 or key == arcade.key.KEY_0:
            self.gameParam.level = 0
        elif key == arcade.key.NUM_1 or key == arcade.key.KEY_1:
            self.gameParam.level = 1
        elif key == arcade.key.NUM_2 or key == arcade.key.KEY_2:
            self.gameParam.level = 2
        elif key == arcade.key.NUM_3 or key == arcade.key.KEY_3:
            self.gameParam.level = 3
        else:
            # Default: Begin in the tutorial level
            self.gameParam.level = 0
        
        self.gameParam.state = "Playing"
        self.gameParam.points = 0
        self.gameParam.tokensInBin = 0
        self.gameParam.tokensFromLastLevel = 0
        
        nextView = GameView(self.gameParam)
        nextView.setup()
        # A view has a pointer to the window that it is displayed in
        self.window.show_view(nextView)
    # on_key_press
# end WelcomeView


# Window class (minimal because all the work is done in views)
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)
        # Store the mouse position and speed at each update
        print('__init__ MyGame')
        
    # end __init__

    # Manual reset method for this class
    def setup(self):
        print('setup MyGame')
        
        gameParam = ChangeUtils.GameParameters()
        gameParam.level = 0
        #gameParam.level = 1
        #gameParam.level = 2
        #gameParam.level = 3
        gameParam.state = "Welcome"
        
        #nextView = GameView(gameParam)
        
        #gameParam.tokensFromLastLevel = 5
        nextView = WelcomeView(gameParam)
        
        #gameParam.tokensInBin = 4
        #gameParam.points = 3
        #gameParam.points = 7
        #nextView = ChangeScoringView.ScoringView(gameParam)
        
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
