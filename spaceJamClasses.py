from panda3d.core import Vec3
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from collideObjectBase import *
from typing import Callable

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, 0, 1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(SphereCollideObject):
    droneCount = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, 0, 2)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(universe, self).__init__(loader, modelPath, parentNode, nodeName, 0, 1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class spaceShip(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, task, render, accept: Callable[[str, Callable], None]):
        super(spaceShip, self).__init__(loader, modelPath, parentNode, nodeName, 0, 2)
        self.taskManager = task
        self.render = render
        self.accept = accept

        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.SetKeyBindings()

        self.reloadTime = .25
        self.missileDistance= 4000 # until it explodes
        self.missileBay = 1 # only 1 missile in the bay to be launched

    def SetKeyBindings(self):
        self.accept("w", self.Thrust, [1])
        self.accept("w-up", self.Thrust, [0])

        self.accept("a", self.LeftTurn, [1])
        self.accept("a-up", self.LeftTurn, [0])

        self.accept("d", self.RightTurn, [1])
        self.accept("d-up", self.RightTurn, [0])

        self.accept("shift", self.MoveUp, [1])
        self.accept("shift-up", self.MoveUp, [0])

        self.accept("enter", self.MoveDown, [1])
        self.accept("enter-up", self.MoveDown, [0])

        self.accept("arrow_left", self.RollLeft, [1])
        self.accept("arrow_left-up", self.RollLeft, [0])

        self.accept("arrow_right", self.RollRight, [1])
        self.accept("arrow_right-up", self.RollRight, [0])

        self.accept('f', self.Fire)

    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskManager.remove('forward-thrust')


    def ApplyThrust(self, task):
        rate = 10
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'left-turn')

        else:
            self.taskManager.remove('left-turn')
    
    def ApplyLeftTurn(self, task):
        #half a degree every frame
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'right-turn')

        else:
            self.taskManager.remove('right-turn')
    
    def ApplyRightTurn(self, task):
        #half a degree every frame
        rate = -0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def MoveUp(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyMoveUp, 'upward-thrust')
        else:
            self.taskManager.remove('upward-thrust')

    
    def ApplyMoveUp(self, task):
        rate = .6
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def MoveDown(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyMoveDown, 'downward-thrust')
        else:
            self.taskManager.remove('downward-thrust')

    
    def ApplyMoveDown(self, task):
        rate = -.6
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def RollLeft(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollLeft, 'left-roll')
        else:
            self.taskManager.remove('left-roll')

    
    def ApplyRollLeft(self, task):
        rate = .6
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def RollRight(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollRight, 'right-roll')
        else:
            self.taskManager.remove('right-roll')

    
    def ApplyRollRight(self, task):
        rate = .6
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont
    
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward()) # fires in direction ship is facing

            # Normalizing a vector makes it consistent all the time
            aim.normalize()

            fireSolution = aim * travRate
            InFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag ='Missile' + str(Missile.missileCount)

            posVec = self.modelNode.getPos() + InFront # spawn the missile in front of the nose of the ship

            #create missile
            currentMissile = Missile(self.loader, './assets/phaser/phaser.egg', self.render, tag, posVec, 4.0)

            # "fluid = 1" makes collision be checked between the last interval and this interval to make sure theres nothing in-between both chcecks thath wasn't hit.
            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
    
    

class spaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(spaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class xz():
    circleIncrement = 0

class yz():
    circleIncrement = 0

class xy():
    circleIncrement = 0

class Missile(SphereCollideObject):
    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    Intervals = {}
    missileCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)

        Missile.missileCount += 1

        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode

        # we retrieve the solid for our collisionNode.
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()

        print ("fire Torpedo #" + str(Missile.missileCount))

        
    
