# ChangeScoringView.py
# View for animating the processing of the player's score after exiting a level

# Imported libraries
import arcade
import random

# Local libraries
import ChangeHeld
import ChangeUtils
import ChangeMachine
import SpareSomeChange

# Keep in sync with SpareSomeChange.py!!!!
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_GOAL_SIZE_X = 48
PLAYER_GOAL_SIZE_Y = 64

class ScoringView(arcade.View):
    def __init__(self, gameParam):
        super().__init__()
        self.gameParam = gameParam
        
        self.allSpriteList = None
        self.pointsSpriteList = None
        self.playerTokenBin = None
        
        self.levelAdvanced = False
        
        self.scoringAnimator = None
        self.displayingScoringAnimation = False
    # end init
    
    # Reset method for this class
    def setup(self):
        print('setup ScoringView')
        # Also called when switching to this view (?)
        self.allSpriteList = arcade.SpriteList()
        self.pointsSpriteList = arcade.SpriteList()
    # end setup

    def on_show(self):
        print('on_show ScoringView')
        
        # Create a player token bin
        x = .35 * SCREEN_WIDTH
        y = .5 * SCREEN_HEIGHT
        self.playerTokenBin = ChangeMachine.PlayerTokenBin(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
        
        for ii in range(self.gameParam.tokensInBin):
            token = ChangeHeld.Token()
            self.playerTokenBin.AppendToken(token)
        # end loop
        
        self.allSpriteList.append(self.playerTokenBin)
        
        # Put a list of point markers, dull or bright
        x = 100
        y = 100
        dx = 50
        for ii in range(9):
            point = ChangeHeld.Point(1)
            point.center_x = x
            point.center_y = y
            
            if ii <= (self.gameParam.points-1):
                point.Bright()
            else:
                point.Dull()
            
            self.pointsSpriteList.append(point)
            self.allSpriteList.append(point)
            
            x += dx
        
        # Create the animation
        self.scoringAnimator = ScoringAnimator()
        self.BuildAnimation()
        self.displayingScoringAnimation = True
        
        # Called when switching to this view
        arcade.set_background_color(arcade.color.BLACK)
        
        # Control mouse visibility
        self.window.set_mouse_visible(True)
    # end on_show
    
    def on_update(self, delta_time):
        if self.scoringAnimator:
            moreToShow = self.scoringAnimator.update()
            
            if False == moreToShow:
                self.displayingScoringAnimation = False
                self.scoringAnimator = None
                
                # Update Params for next level
                
                # Repeat of calculations made while building the animation
                lowerLimit = 9
                pointLimit = 9
                
                gainedPoints = self.gameParam.tokensInBin - lowerLimit
                if 0 < gainedPoints:
                    self.gameParam.points += gainedPoints
                if pointLimit <= self.gameParam.points:
                    print('Advance Level!')
                    self.levelAdvanced = True
                    self.gameParam.level += 1
                    self.gameParam.points = 0
                    self.gameParam.tokensInBin = 0
                    self.gameParam.tokensFromLastLevel = 0
                else:
                    self.gameParam.tokensInBin = 0
                    self.gameParam.tokensFromLastLevel = gainedPoints
    # end on_update
    
    def on_draw(self):
        # Called each draw cycle
        arcade.start_render()

        # Todo: Add text
        x = 200
        y = 500
        fontSize = 40
        text = "Scoring"
        arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        
        self.allSpriteList.draw()
        
        if self.playerTokenBin:
            self.playerTokenBin.DrawMachine()

        if False == self.displayingScoringAnimation:
            x = 200
            y = 400
            fontSize = 30
            text = "Press any key to CONTINUE"
            arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)
            
        if True == self.levelAdvanced:
            x = 400
            y = 300
            fontSize = 30
            text = f"Advance to Level {self.gameParam.level}"
            arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

        if 2 == self.gameParam.level:
            x = 140
            y = 20
            fontSize = 15
            text = f"Tip: If you press a number key on the title screen, it wil take you to that level!"
            arcade.draw_text(text, x, y, arcade.color.WHITE, fontSize)

    # end on_draw
    
    def on_key_press(self, symbol, modifiers):
        # https://api.arcade.academy/en/latest/arcade.key.html
        # Toggle views when any key is pressed

        if False == self.displayingScoringAnimation:
            # The animation is responsible for updating the other param values
            
            # Todo: Update params for next level
        
            self.gameParam.state = "Playing"
            
            nextView = SpareSomeChange.GameView(self.gameParam)
            nextView.setup()
            # A view has a pointer to the window that it is displayed in
            self.window.show_view(nextView)
    # on_key_press
    
    def BuildAnimation(self):
        self.scoringAnimator = ScoringAnimator()
        existingPoints = self.gameParam.points
        tokenCount = 0
        lowerLimit = 9
        pointLimit = 9
        timeStep = 0
        deltaT = 20

        # Give it a second before it starts
        timeStep = 40

        # If the token is in the lower bin, deleted them bottom up
        # if the token is in the upper bin, move then to the lower bin(bottom up) and activate a point for each.
        for token in self.playerTokenBin.heldTokenSpriteList:
            tokenCount += 1
            if lowerLimit >= tokenCount:
                self.scoringAnimator.AddRemoveStep(token, timeStep)
            else:
                moveToIndex = tokenCount - lowerLimit  # one index
                # Sanity check
                if pointLimit >= moveToIndex:
                    self.scoringAnimator.AddMoveToIndexStep(token, moveToIndex, self.playerTokenBin, timeStep)
                    pointIndex = moveToIndex - 1 + existingPoints # zero index
                    if pointLimit > pointIndex:
                        point = self.pointsSpriteList[pointIndex]
                        self.scoringAnimator.AddChangeTextureStep(point , point.brightTexture, timeStep)

            timeStep += deltaT
        # end Loop
    # BuildAnimation
    
# end ScoringView

# A single animation step
class AnimiationStep():
    def __init__(self):
        self.timeStep = 0
        # None, Remove, MoveToIndex, ChangeTexture
        self.action = "None"
        self.object = None
        self.newIndex = 0
        self.playerTokenBin = None
        self.newTexture = None
    # end init

# end AnimationStep

# A class that stores a list of animation steps and can apply them at the correct time
class ScoringAnimator():
    def __init__(self):
        # List of all animation steps, in time order (There can be multiple animation steps for the same time step)
        self.stepList = []
        # Largest time that has been rendered
        self.currentTime = 0
        # Last animation step that has been rendered
        self.currentStepIndex = -1 # Start at -1 because the 1st thing we do is add one and access a zero index list
    # end init

    # Destroy the pointed object
    def AddRemoveStep(self, object, timeStep):
        step = AnimiationStep()
        step.timeStep = timeStep
        step.action = "Remove"
        step.object = object
        self.stepList.append(step)
    # end AddRemoveStep

    # Move the pointed object to a new location (defined via index) in the player token bin
    def AddMoveToIndexStep(self, object, newIndex, playerTokenBin, timeStep):
        step = AnimiationStep()
        step.timeStep = timeStep
        step.action = "MoveToIndex"
        step.object = object
        step.newIndex = newIndex
        step.playerTokenBin = playerTokenBin
        self.stepList.append(step)
    # end AddRemoveStep

    # Apply a different texture to an object (sprite)
    def AddChangeTextureStep(self, object, newTexture, timeStep):
        step = AnimiationStep()
        step.timeStep = timeStep
        step.action = "ChangeTexture"
        step.object = object
        step.newTexture = newTexture
        self.stepList.append(step)
    # end AddRemoveStep

    # Apply the effect of the input step
    def ActOnStep(self, step):
        if step and step.object:
            if "Remove" == step.action:
                step.object.remove_from_sprite_lists()
            elif "MoveToIndex" == step.action:
                if step.playerTokenBin:
                    #print(f'step.newIndex = {step.newIndex}')
                    step.playerTokenBin.PositionToken(step.object, step.newIndex) 
            elif "ChangeTexture" == step.action:
                step.object.texture = step.newTexture
    # end ActOnStep

    # Move forward one time tick
    # Return False if all steps in the list have been played
    def update(self):
        moreToShow = True
        self.currentTime += 1
        #print(f'self.currentTime = {self.currentTime}')
        # Advance through all uncompleted ordered steps that are less than or equal to the current time.
        nextStepIndex = self.currentStepIndex + 1
        while nextStepIndex <= (len(self.stepList)-1) and self.stepList[nextStepIndex].timeStep <= self.currentTime:
            #print(f'Acting on {nextStepIndex}')
            self.ActOnStep(self.stepList[nextStepIndex])
            self.currentStepIndex = nextStepIndex
            nextStepIndex = self.currentStepIndex + 1

        # Have we reached the last step?
        if self.currentStepIndex >= (len(self.stepList)-1):
            moreToShow = False

        return moreToShow
    # end update

# ScoringAnimator




