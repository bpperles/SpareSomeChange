# ChangeUtils.py
# General utilities that I found useful to write

# Imported libraries
import arcade
import random

# return zero index random number
def myRandom(max):
    return random.randrange(max)
# myRandom
def myRandom2(min, max):
    return random.randrange(min, max)
# myRandom2

# Key values that are passed between views
class GameParameters():
    def __init__(self):
        # Welcome, Playing, Paused, GameOver, ExitLevel, Scoring
        self.state = "Unknown"
        self.level = 0
        self.points = 0
        self.tokensInBin = 0
        self.tokensFromLastLevel = 0
    # end init
# end GameParam


# A stand alone utility class that will cause a sprite to display an animation for a peroid of time
# and then revert back when finished. Needs to have its Update() method manually called each cycle.
# Does not trigger any drawing, just changes the sprite's texture.
# Inputs:
# sprite: The sprite to be managed.
# staticTexture: Texture to be applyed when total time is exspired
# animationTextureList: List of textures to be applied, in order. Will loop if there is extra time
# totalDuration: Total update cycles for animation to run
# cycleDuration: Number of update cycles before animation is advanced
# Ideas for improvements:
# Allow for infinite looping
# Take list of cycle durations, one for each animation texture
class SpriteAnimator():
    def __init__(self, sprite, staticTexture, animationTextureList, totalDuration, cycleDuration):
        self.sprite = sprite
        self.staticTexture = staticTexture
        self.animationTextureList = animationTextureList
        self.textureCount = len(self.animationTextureList)
        self.totalDuration = totalDuration
        self.totalCountDown = self.totalDuration
        self.cycleCountDown = 0
        self.cycleDuration = cycleDuration
        if 0 < self.textureCount and None != self.staticTexture:
            self.isRunning = True
            self.cycleCountDown = self.cycleDuration
            self.currentTexture = 0
            self.sprite.texture = self.animationTextureList[self.currentTexture]
    # end init

    def IsRunning(self):
        return self.isRunning

    def Stop(self):
        self.isRunning = False
        self.sprite.texture = self.staticTexture

    def Pause(self):
        self.isRunning = False

    def Resume(self):
        self.isRunning = True
        self.sprite.texture = self.animationTextureList[self.currentTexture]

    def update(self):
        if self.IsRunning():
            self.totalCountDown -= 1
            self.cycleCountDown -= 1
            if 0 >= self.totalCountDown:
                self.isRunning = False
                self.sprite.texture = self.staticTexture
            elif 0 >= self.cycleCountDown:
                self.currentTexture += 1
                if (self.textureCount-1) < self.currentTexture:
                    self.currentTexture = 0
                self.sprite.texture = self.animationTextureList[self.currentTexture]
                self.cycleCountDown = self.cycleDuration

# End SpriteAnimator

# Creates a popcorn pop-ing effect
# (I don't don't how to apply gravity to the particles, so they have a very short lifecycle)
class PopcornParticles():
    def __init__(self, x, y, width, height):

        self.emitterList = []

        # Since particles go in all directions, use the inner two-thirds
        self.minX = int(x - width/3)
        self.maxX = int(x + width/3)
        self.minY = int(y - height/3)
        self.maxY = int(y + height/3)
        
        self.coolDownStart = 5
        self.coolDownCount = 0

    # end init
    
    def AddEmitter(self):
        # File is 64x64
        cueBallTextureFile = "Resources/Popcorn.png"
        particalCount = 5
        particlespeed = 1.5
        particalLifeTime = .5
        particalTextureScale = .125
        particalAlpha = 255

        x = myRandom2(self.minX, self.maxX)
        y = myRandom2(self.minY, self.maxY)

        # Copied from Arcade partical examples
        newEmitter = arcade.Emitter(
            center_xy=(x,y),
            emit_controller=arcade.EmitBurst(particalCount),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=cueBallTextureFile,
                change_xy=arcade.rand_in_circle((0.0, 0.0), particlespeed),
                lifetime=particalLifeTime,
                scale=particalTextureScale,
                alpha=particalAlpha
            )
        )
        self.emitterList.append(newEmitter)
    # End AddEmitter
        
    def update(self):
        self.coolDownCount -= 1
        if 0 >= self.coolDownCount:
            # I don't really understand emitters, so just keep creating new emitters at new locations
            self.AddEmitter()
            self.coolDownCount = self.coolDownStart

        for emitter in self.emitterList:
            emitter.update()
    # end update

    def on_draw(self):
        for emitter in self.emitterList:
            emitter.draw()
    # end on_draw
    
# End PopcornParticles

# Simliar to the popcorn effect, add exploding tokens to the zerk bank
# (I don't don't how to apply gravity to the particles, so they have a very short lifecycle)
class TokenParticles():
    def __init__(self, x, y, width, height):

        self.emitterList = []

        # Since particles go in all directions, use the inner two-thirds
        self.minX = int(x - width/3)
        self.maxX = int(x + width/3)
        self.minY = int(y - height/3)
        self.maxY = int(y + height/3)
        
        self.coolDownStart = 30
        self.coolDownCount = 0

    # end init
    
    def AddEmitter(self):
        # File is 64x64
        cueBallTextureFile = "Resources/Token.png"
        particalCount = 7
        particlespeed = 1
        particalLifeTime = 1.15
        particalTextureScale = .25
        particalAlpha = 255

        x = myRandom2(self.minX, self.maxX)
        y = myRandom2(self.minY, self.maxY)

        # Copied from Arcade partical examples
        newEmitter = arcade.Emitter(
            center_xy=(x,y),
            emit_controller=arcade.EmitBurst(particalCount),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=cueBallTextureFile,
                change_xy=arcade.rand_in_circle((0.0, 0.0), particlespeed),
                lifetime=particalLifeTime,
                scale=particalTextureScale,
                alpha=particalAlpha
            )
        )
        self.emitterList.append(newEmitter)
    # End AddEmitter
        
    def update(self):
        self.coolDownCount -= 1
        if 0 >= self.coolDownCount:
            # I don't really understand emitters, so just keep creating new emitters at new locations
            self.AddEmitter()
            self.coolDownCount = self.coolDownStart

        for emitter in self.emitterList:
            emitter.update()
    # end update

    def on_draw(self):
        for emitter in self.emitterList:
            emitter.draw()
    # end on_draw
    
# End TokenParticles
