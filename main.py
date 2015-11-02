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
from panda3d.core import LVector3, LVecBase4f
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
import math
import sys
import colorsys

from xml.dom.minidom import parse
import xml.dom.minidom

# Simple function to keep a value in a given range (by default 0 to 1)
def clamp(i, mn=0, mx=1):
    return min(max(i, mn), mx)

class MAMEDevice(ShowBase):

    def __init__(self, layout_dir):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.layout_dir = layout_dir
        self.loadXMLlayout()
        self.dyn_angle = 0
        self.target_angle = 0
        self.delta_angle = 5

        self.setup_MAME_IPC()
        self.setup_model()
        self.setup_scene()
        self.setup_event_handlers()

    def setup_MAME_IPC(self):
        self.light_elements = {}
        self.light_states = {}
        #TODO: create FIFO file if it does not yet exist...
        self.FIFO = open("/tmp/sdlmame_out")

    def loadXMLlayout(self):
        filename = self.layout_dir + "/" + self.layout_dir + ".3dlay"
        # Open XML document using minidom parser
        DOMTree = xml.dom.minidom.parse(filename)
        self.device_layout = DOMTree.documentElement
        self.device_id = self.device_layout.getAttribute('id')

    def setup_model(self):
        root = render.attachNewNode('device_root')
        root_elements = self.device_layout.childNodes
        self.device_title = self._getValue(self.device_layout, 'name', "untitled layout")
        self.parseModelElements(root, root_elements)

    def _getBoolean(self, element, attr, default):
        value = self._getValue(element, attr, default)
        if not isinstance(value, bool):
            if str(value) == "true":
                return True
            else:
                return False
        return value

    def _getVector(self, element, attr, default):
        value = self._getValue(element, attr, default)
        if not isinstance(value, tuple):
            value = [float(v.strip()) for v in str(value).split(',')]
        return value

    def _getValue(self, element, attr, default):
        if element.hasAttribute(attr):
            return element.getAttribute(attr)
        else:
            return default

    def parseModelElements(self, currentNode, elements):
        
        for element in elements:
            try:
                x = element.tagName
            except AttributeError:
                #This is a hack to ignore XML Text nodes...
                continue

            if element.tagName == 'group':
                id = self._getValue(element, 'id', None)
                position = self._getVector(element, 'position', (0.0, 0.0, 0.0))
                hpr = self._getVector(element, 'hpr', (0.0, 0.0, 0.0))
                newNode = currentNode.attachNewNode(id)
                newNode.setPosHpr(float(position[0]), float(position[1]), float(position[2]), float(hpr[0]), float(hpr[1]), float(hpr[2]))

            elif element.tagName == 'model':
                _id = self._getValue(element, 'id', None)
                filename = self._getValue(element, 'filename', None)
                color = self._getVector(element, 'color', (1,1,1,1))
                metalic = self._getBoolean(element, 'metalic', False)
                newNode = self.load_3D_Model(name=_id, filename=filename, color=LVecBase4f(color[0], color[1], color[2], color[3]), metalic=metalic, parent=currentNode)

            elif element.tagName == 'light':
                id = self._getValue(element, 'id', None)
                att = self._getVector(element, 'attenuation', (0.1, 0.04, 0.0))
                color = self._getVector(element, 'color', (1, 1, 1, 1))
                newNode = self.addLight(name=id, parent=currentNode, attenuation=LVector3(att[0], att[1], att[2]), color=LVecBase4f(color[0], color[1], color[2], color[3]))

            self.parseModelElements(newNode, element.childNodes)

    def setup_event_handlers(self):
        # listen to keys for controlling the lights
        self.accept("escape", sys.exit)
        self.accept("a", self.toggleLights, [[self.ambientLight]])
        self.accept("d", self.toggleLights, [[self.directionalLight]])
        self.accept("p", self.toggleAllLights)
        self.accept("l", self.togglePerPixelLighting)
        self.accept("e", self.toggleShadows)
        self.accept("z", self.addBrightness, [self.ambientLight, -.05])
        self.accept("x", self.addBrightness, [self.ambientLight, .05])
        self.accept("c", self.addBrightness, [self.directionalLight, -.05])
        self.accept("v", self.addBrightness, [self.directionalLight, .05])
        self.accept("h", self.manual_rotation, [render.find("**/dynamic"), 5])
        self.accept("g", self.manual_rotation, [render.find("**/dynamic"), -5])

    def setup_scene(self):
        # The main initialization of our class
        # This creates the on screen title that is in every tutorial
        self.title = OnscreenText(text=self.device_title,
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
            filename = 'egg/%s_%s' % (self.device_id, name)

        model = loader.loadModel('%s/%s' % (self.layout_dir, filename))
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
        self.light_elements[name] = light
        self.light_states[name] = '0'
        return light

    def manual_rotation(self, part, angle):
        part.setHpr(0, 0, angle + part.getR())

    def setDynamicHeading(self, angle):
        dynamic = render.find("**/dynamic")
        dynamic.setHpr(0, 0, angle)

    def toggleAllLights(self):
        all_light_names = self.light_elements.keys()
        self.toggleLights(all_light_names)

    # This function takes a list of lights and toggles their state. It takes in a
    # list so that more than one light can be toggled in a single command
    def toggleLights(self, lights):
    
        for lightName in lights:
            # If the given light is in our lightAttrib, remove it.
            # This has the effect of turning off the light
            light = self.light_elements[lightName]
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

    def update_lights(self):
        try:
            class_, pidnum, name, state = self.FIFO.readline().strip().split()
        except ValueError:
            return

        #This is for testing with Power Drift
        # (because we still do not correctly motor movements in Galaxy Force 2 Super Deluxe)
        if name == 'bank_motor_position':
            angle = ((int(state)-1)/6.0 - 0.5) * 120
            self.target_angle = angle
            return

        self.light_states[name] = state

        if name in self.light_elements.keys():
            light = self.light_elements[name]
            if self.light_states[name] == '1':
                render.setLight(light)
            else:
                render.clearLight(light)

    def update_motors(self):
        if self.dyn_angle != self.target_angle:
            self.setDynamicHeading(self.dyn_angle)
            if self.dyn_angle - self.target_angle > self.delta_angle:
                self.dyn_angle -= self.delta_angle/3.0
            elif self.dyn_angle - self.target_angle < -self.delta_angle:
                self.dyn_angle  += self.delta_angle/3.0
            else:
                self.dyn_angle = self.target_angle;

import sys
if len(sys.argv) != 2:
    print "\n\tusage: %s <device_id>\n\n" % sys.argv[0]
    exit(-1)

device_id = sys.argv[1]

# Make an instance of our class and run the demo
device = MAMEDevice(device_id)

while True:
    taskMgr.step()
    device.update_lights()
    device.update_motors()
    
    