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
