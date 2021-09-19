# ChangeLevel3.py
# Define function for creating objects for level 3
# Popcorn machine!

# Imported libraries
import arcade

# Local Libraries
import ChangeMachine
import ChangeHeld
import ChangePlayer
import ChangeZerk
import ChangeUtils

# Keep in sync with SpareSomeChange.py
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_GOAL_SIZE_X = 48
PLAYER_GOAL_SIZE_Y = 64


def BuildLevel3(gameParam,
                PlayerSpriteList,
                ZerkSpriteList,
                MachineSpriteList,
                DistractionSpriteSubList,
                AllWallsSpriteList):
    # Build all sprites
    x = .1 * SCREEN_WIDTH
    y = .75 * SCREEN_HEIGHT
    player = ChangePlayer.Player(x, y)
    PlayerSpriteList.append(player)
    
    zerk = ChangeZerk.Zerk()
    zerk.center_x = .45 * SCREEN_WIDTH
    zerk.center_y = .5 * SCREEN_HEIGHT
    ZerkSpriteList.append(zerk)

    zerk2 = ChangeZerk.Zerk()
    zerk2.center_x = .65 * SCREEN_WIDTH
    zerk2.center_y = .5 * SCREEN_HEIGHT
    ZerkSpriteList.append(zerk2)

    # Left token machine
    x = .1 * SCREEN_WIDTH
    y = .6 * SCREEN_HEIGHT
    tokenMachine1 = ChangeMachine.TokenMachine(x, y, "Left", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    tokenMachine1.Fill()
    MachineSpriteList.append(tokenMachine1)
    AllWallsSpriteList.append(tokenMachine1)

    # Right top token machine
    x = .75 * SCREEN_WIDTH
    y = .6 * SCREEN_HEIGHT
    tokenMachine3 = ChangeMachine.TokenMachine(x, y, "Left", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    tokenMachine3.Fill()
    MachineSpriteList.append(tokenMachine3)
    AllWallsSpriteList.append(tokenMachine3)

    # Top token Machine
    x = .45 * SCREEN_WIDTH
    y = .9 * SCREEN_HEIGHT
    tokenMachine2 = ChangeMachine.TokenMachine(x, y, "Right", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    tokenMachine2.Fill()
    MachineSpriteList.append(tokenMachine2)
    AllWallsSpriteList.append(tokenMachine2)

    # Right bottom token machine
    x = .75 * SCREEN_WIDTH
    y = .3 * SCREEN_HEIGHT
    tokenMachine4 = ChangeMachine.TokenMachine(x, y, "Right", PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    tokenMachine4.Fill()
    MachineSpriteList.append(tokenMachine4)
    AllWallsSpriteList.append(tokenMachine4)

    x = .35 * SCREEN_WIDTH
    y = .4 * SCREEN_HEIGHT
    PlayerTokenBin = ChangeMachine.PlayerTokenBin(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    for ii in range(gameParam.tokensFromLastLevel):
        token = ChangeHeld.Token()
        PlayerTokenBin.AppendToken(token)
    MachineSpriteList.append(PlayerTokenBin)
    AllWallsSpriteList.append(PlayerTokenBin)

    x = .9 * SCREEN_WIDTH
    y = .1 * SCREEN_HEIGHT
    ZerkBankSprite = ChangeMachine.EnemyTokenBin(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    MachineSpriteList.append(ZerkBankSprite)
    AllWallsSpriteList.append(ZerkBankSprite)
    
    x = .9 * SCREEN_WIDTH
    y = .9 * SCREEN_HEIGHT
    cashRegister = ChangeMachine.CashRegister(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    cashRegister.Fill()
    MachineSpriteList.append(cashRegister)
    AllWallsSpriteList.append(cashRegister)
    
    x = .1 * SCREEN_WIDTH
    y = .9 * SCREEN_HEIGHT
    safe = ChangeMachine.Safe(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    MachineSpriteList.append(safe)
    AllWallsSpriteList.append(safe)

    x = .65 * SCREEN_WIDTH
    y = .9 * SCREEN_HEIGHT
    popcornMachine = ChangeMachine.PopcornMachine(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    MachineSpriteList.append(popcornMachine)
    DistractionSpriteSubList.append(popcornMachine)
    AllWallsSpriteList.append(popcornMachine)

    x = .1 * SCREEN_WIDTH
    y = .3 * SCREEN_HEIGHT
    leftPhone = ChangeMachine.DummyPhone(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    leftPhone.Fill()
    MachineSpriteList.append(leftPhone)
    AllWallsSpriteList.append(leftPhone)

    x = .55 * SCREEN_WIDTH
    y = .4 * SCREEN_HEIGHT
    ExitDoor = ChangeMachine.ExitDoor(x, y, PLAYER_GOAL_SIZE_X, PLAYER_GOAL_SIZE_Y)
    MachineSpriteList.append(ExitDoor)
    AllWallsSpriteList.append(ExitDoor)

    # For level 0, turning the helper arrows
    #for machine in MachineSpriteList:
    #    machine.displayPortHelper = True

# end BuildLevel3
