#!/usr/bin/env python

# Author: Jason Pratt (pratt@andrew.cmu.edu)
# Author: Felipe Sanches (juca@members.fsf.org)

from direct.showbase.ShowBase import ShowBase
from panda3d.core import PerspectiveLens
from panda3d.core import NodePath
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import PointLight
from panda3d.core import TextNode
from panda3d.core import Material
from panda3d.core import LVector3
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
import math
import sys
import colorsys

# Simple function to keep a value in a given range (by default 0 to 1)
def clamp(i, mn=0, mx=1):
    return min(max(i, mn), mx)

class GalaxyForce(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        # The main initialization of our class
        # This creates the on screen title that is in every tutorial
        self.title = OnscreenText(text="Galaxy Force II Super Deluxe",
                                  style=1, fg=(1, 1, 0, 1), shadow=(0, 0, 0, 0.5),
                                  pos=(0.87, -0.95), scale = .07)

        self.disco = loader.loadModel("egg/disco_hall")
        self.disco.reparentTo(render)
        self.disco.setPosHpr(0, 80, -10, 90, 0, 0)
        self.disco.setColor((0.5, 0.6, 0.5, 1))

        # First we create an ambient light. All objects are affected by ambient
        # light equally
        # Create and name the ambient light
        self.ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
        # Set the color of the ambient light
        self.ambientLight.node().setColor((.1, .1, .1, 1))
        # add the newly created light to the lightAttrib

        # Now we create a directional light. Directional lights add shading from a
        # given angle. This is good for far away sources like the sun
        self.directionalLight = render.attachNewNode(
            DirectionalLight("directionalLight"))
        self.directionalLight.node().setColor((.35, .35, .35, 1))
        # The direction of a directional light is set as a 3D vector
        self.directionalLight.node().setDirection(LVector3(1, 1, -2))
        # These settings are necessary for shadows to work correctly
        self.directionalLight.setZ(6)
        dlens = self.directionalLight.node().getLens()
        dlens.setFilmSize(41, 21)
        dlens.setNearFar(50, 75)
        # self.directionalLight.node().showFrustum()
        
        self.glass = loader.loadModel('egg/gforce2_glass')
        self.glass.setColor((0.7, 0.7, 0.7, 0.7))
        self.glass.setPos(0, 0, 0)
        self.glass.setScale(.005)

        self.shinny_metal = loader.loadModel('egg/gforce2_shinny_metal')
        self.shinny_metal.setColor((0.6, 0.6, 0.6, 1))
        self.shinny_metal.setPos(0, 0, 0)
        self.shinny_metal.setScale(.005)

        metalic = Material()
        metalic.setShininess(20.0)
        metalic.setSpecular((0.6, 0.6, 0.9, 1))
#        metalic.setAmbient((0.7, 0.7, 0.7, 1))
        self.shinny_metal.setMaterial(metalic)

        self.black_metal = loader.loadModel('egg/gforce2_dark_black_metal.egg')
        self.black_metal.setColor((0.3, 0.3, 0.35, 1))
        self.black_metal.setPos(0, 0, 0)
        self.black_metal.setScale(.005)

        # The blue point light
        # Point lights are lights that radiate from a single point, like a light bulb.
        # Like spotlights, they are given position by attaching them to NodePaths in the world
        self.bluePointLight = self.black_metal.attachNewNode(
            PointLight("bluePointLight"))
        self.bluePointLight.node().setAttenuation(LVector3(.1, 0.04, 0.0))
        self.bluePointLight.node().setColor((0, 0, .35, 1))
        self.bluePointLight.node().setSpecularColor((1, 1, 1, 1))

        self.spaceship = render.attachNewNode("spaceShip")
        self.spaceship.setPosHpr(0, 60, -10, 0, -90, 0)

        self.glass.reparentTo(self.spaceship)
        self.shinny_metal.reparentTo(self.spaceship)
        self.black_metal.reparentTo(self.spaceship)

        # Finally we store the light on the root of the scene graph.
        # This will cause them to affect everything in the scene.
        render.setLight(self.ambientLight)
        render.setLight(self.directionalLight)
        render.setLight(self.bluePointLight)

        # Per-pixel lighting and shadows are initially off
        self.perPixelEnabled = False
        self.shadowsEnabled = False

        # listen to keys for controlling the lights
        self.accept("escape", sys.exit)
        self.accept("a", self.toggleLights, [[self.ambientLight]])
        self.accept("d", self.toggleLights, [[self.directionalLight]])
        self.accept("p", self.toggleLights, [[self.bluePointLight]])
        self.accept("l", self.togglePerPixelLighting)
        self.accept("e", self.toggleShadows)
        self.accept("z", self.addBrightness, [self.ambientLight, -.05])
        self.accept("x", self.addBrightness, [self.ambientLight, .05])
        self.accept("c", self.addBrightness, [self.directionalLight, -.05])
        self.accept("v", self.addBrightness, [self.directionalLight, .05])
        self.accept("h", self.rotateShip, [self.spaceship, 5])
        self.accept("g", self.rotateShip, [self.spaceship, -5])

    def rotateShip(self, part, angle):
        part.setH(angle + part.getH())

    # This function takes a list of lights and toggles their state. It takes in a
    # list so that more than one light can be toggled in a single command
    def toggleLights(self, lights):
        for light in lights:
            # If the given light is in our lightAttrib, remove it.
            # This has the effect of turning off the light
            if render.hasLight(light):
                render.clearLight(light)
            # Otherwise, add it back. This has the effect of turning the light
            # on
            else:
                render.setLight(light)

    # This function turns per-pixel lighting on or off.
    def togglePerPixelLighting(self):
        if self.perPixelEnabled:
            self.perPixelEnabled = False
            render.clearShader()
        else:
            self.perPixelEnabled = True
            render.setShaderAuto()


    # This function turns shadows on or off.
    def toggleShadows(self):
        if self.shadowsEnabled:
            self.shadowsEnabled = False
            self.directionalLight.node().setShadowCaster(False)
        else:
            if not self.perPixelEnabled:
                self.togglePerPixelLighting()
            self.shadowsEnabled = True
            self.directionalLight.node().setShadowCaster(True, 512, 512)

    # This function reads the color of the light, uses a built-in python function
    #(from the library colorsys) to convert from RGB (red, green, blue) color
    # representation to HSB (hue, saturation, brightness), so that we can get the
    # brighteness of a light, change it, and then convert it back to rgb to chagne
    # the light's color
    def addBrightness(self, light, amount):
        color = light.node().getColor()
        h, s, b = colorsys.rgb_to_hsv(color[0], color[1], color[2])
        brightness = clamp(b + amount)
        r, g, b = colorsys.hsv_to_rgb(h, s, brightness)
        light.node().setColor((r, g, b, 1))

    # Returns the brightness of a light as a string to put it in the instruction
    # labels
    def getBrightnessString(self, light):
        color = light.node().getColor()
        h, s, b = colorsys.rgb_to_hsv(color[0], color[1], color[2])
        return "%.2f" % b


# Make an instance of our class and run the demo
demo = GalaxyForce()
demo.run()
