# ChangePathFinding.py
# Wrapper class around pathfinding for zerks

# Imported libraries
import arcade

# Local libraries
import ChangeMachine
import ChangeZerk
import ChangeUtils

SLOP = 3

class ZerkPathFinder():
    def __init__(self, zerk, wallList, minX, maxX, minY, maxY, gridSize):
        
        self.zerk = zerk
        self.wallList = wallList
        self.path = None
        self.currentIndex = 0
        
        EmptyWallSpriteList = arcade.SpriteList()

        
        self.barrier_list = arcade.AStarBarrierList(self.zerk,
                                                    self.wallList,
                                                    gridSize,
                                                    minX, maxX, minY, maxY)
    # end init
    
    def ComputeForPort(self, port):
        #print('Compute')
        target = (port.enemyDockX, port.enemyDockY)
        #print(f'{self.zerk.position}')
        #print(f'{target}')
        
        self.path = arcade.astar_calculate_path(self.zerk.position,
                                                target,
                                                self.barrier_list,
                                                diagonal_movement=True)
        if self.path:
            x = 1
            #print(f'len = {len(self.path)}')
        else:
            print('Failed to get path')
         
        #self.currentIndex = 0
        # The 1st point is where we start, so skip it
        self.currentIndex = 1
    # end Compute
    
    def GetNextTarget(self, currentX, currentY):
        rl = None
        if self.path and (len(self.path)-1) >= self.currentIndex:
            currentTarget = self.path[self.currentIndex]
            sqrDist = pow(currentX - currentTarget[0], 2) + pow(currentY - currentTarget[1], 2)
            if pow(SLOP, 2) > sqrDist:
                #print('reached target')
                self.currentIndex += 1
                #if (len(self.path)-1) < self.currentIndex:
                # Pathfinding is week.  The last point is never very good.  Skip it and let the zerk move towards its actual target
                if (len(self.path)-2) < self.currentIndex:
                    #print('reached end of path')
                    self.path = None
                    rl = None
                else:
                    #print('Next vaue')
                    rl = self.path[self.currentIndex]
            else:
                #print('current value')
                rl = self.path[self.currentIndex]
        return rl
    # end GetNextTarget
    
    def DrawPath(self):
        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)
        
# end ZerkPathFinder

