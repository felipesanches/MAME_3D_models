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

gforce2_data = {
        'id': "gforce2",
        'name': "Galaxy Force II Super Deluxe"
}

class MAMEDevice(ShowBase):

    def __init__(self, device_data):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.device_data = device_data
        self.setup_scene()
        self.setup_model()
        self.setup_event_handlers()

    def setup_model(self):
        heading = 130
        self.spaceship = render.attachNewNode("spaceShip")
        self.spaceship.setPosHpr(0, 60, -10, heading, -90, 0)

        self.static_spaceship = render.attachNewNode("staticSpaceShip")
        self.static_spaceship.setPosHpr(0, 60, -10, heading, -90, 0)

        self.load_3D_Model(name='glass', color=(0.7, 0.7, 0.7, 0.7), parent=self.spaceship)
        self.load_3D_Model(name='shinny_metal', color=(0.6, 0.6, 0.6, 1), metalic=True, parent=self.spaceship)
        bm = self.load_3D_Model(name='dark_black_metal', color=(0.3, 0.3, 0.35, 1), parent=self.spaceship)
        self.bluePointLight = self.addLight(name="bluePointLight", parent=bm, attenuation=LVector3(.1, 0.04, 0.0), color=(0, 0, .35, 1))

        self.load_3D_Model(name='static_shinny_metal', color=(0.6, 0.6, 0.6, 1), metalic=True, parent=self.static_spaceship)
        self.load_3D_Model(name='static_golden', color=(0.8, 0.5, 0.2, 1), metalic=True, parent=self.static_spaceship)
        self.load_3D_Model(name='static_red', color=(0.8, 0, 0, 1), parent=self.static_spaceship)

    def setup_event_handlers(self):
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

    def setup_scene(self):
        # The main initialization of our class
        # This creates the on screen title that is in every tutorial
        self.title = OnscreenText(text=self.device_data['name'],
                                  style=1, fg=(1, 1, 0, 1), shadow=(0, 0, 0, 0.5),
                                  pos=(0.87, -0.95), scale = .07)

        self.load_3D_Model(filename = "../common/egg/disco_hall", color=(0.5, 0.6, 0.5, 1), position=(0, 80, -10), hpr=(90, 0, 0), scale=1)

        # First we create an ambient light. All objects are affected by ambient light equally
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

        # Finally we store the light on the root of the scene graph.
        # This will cause them to affect everything in the scene.
        render.setLight(self.ambientLight)
        render.setLight(self.directionalLight)

        # Per-pixel lighting and shadows are initially off
        self.perPixelEnabled = False
        self.shadowsEnabled = False

    def load_3D_Model(self, filename=None, name=None, parent=None, color=(1,1,1,1), position=(0,0,0), hpr=(0,0,0),
                      scale=0.005, metalic=False, shininess=20, specular=(0.6, 0.6, 0.9, 1)):
        if parent is None:
            parent = render

        if name:
            filename = 'egg/%s_%s' % (self.device_data['id'], name)

        model = loader.loadModel(filename)
        model.setColor(color)
        model.setPosHpr(position[0], position[1], position[2], hpr[0], hpr[1], hpr[2])
        model.setScale(scale)

        if metalic:
            m = Material()
            m.setShininess(shininess)
            m.setSpecular(specular)
            model.setMaterial(m)

        model.reparentTo(parent)
        return model

    def addLight(self, name, parent, attenuation=LVector3(.1, 0.04, 0.0), color=(1, 1, 1, 1), specular=(1, 1, 1, 1)):
        light = parent.attachNewNode(PointLight(name))
        light.node().setAttenuation(attenuation)
        light.node().setColor(color)
        light.node().setSpecularColor(specular)
        render.setLight(light)
        return light

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
demo = MAMEDevice(gforce2_data)

fifo = open("/tmp/sdlmame_out")
states = {'start_lamp': '0'}

while True:
    try:
        class_, pidnum, what, state = fifo.readline().strip().split()
        states[what] = state
    
        if states['start_lamp'] == '1':
            render.setLight(demo.bluePointLight)
        else:
            render.clearLight(demo.bluePointLight)
    except ValueError:
        pass

    taskMgr.step()