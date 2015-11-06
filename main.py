#!/usr/bin/env python
# Prototype of a 3d artwork System for MAME
#
# This is free software, released under the terms of the
# GNU General Public License version 2 (or later).
#
# Author: Felipe Correa da Silva Sanches (juca@members.fsf.org)
#
# Based on one of the Panda3d examples
# by Jason Pratt (pratt@andrew.cmu.edu)

from panda3d.core import PerspectiveLens
from panda3d.core import AmbientLight, DirectionalLight, Spotlight
from panda3d.core import PointLight
from panda3d.core import Material
from panda3d.core import LVector3, LVecBase4f, VBase4
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import sys
from math import pi, sin, cos
from random import random
from xml.dom.minidom import parse
import xml.dom.minidom

class MotionControl():
    def __init__(self, element, _type, _from, _to, _min, _max, original_pos, original_hpr):
        self.element=element
        self._type=_type
        self._from=_from
        self._to=_to
        self._min=_min
        self._max=_max
        
        if _type == "linear":
            self.target_vector = original_pos
            self.SPEED = float(self._max - self._min)/10
        else:
            self.target_vector = original_hpr
            self.SPEED = 5.0


        self.current_vector = [0, 0, 0]
        for i in range(3):
            self.current_vector[i] = self.target_vector[i]

        self.t = 0.0

    def setValue(self, value):
        value = float(value)

        if value < self._min:
            value = self._min
        if value > self._max:
            value = self._max

        self.t = (float(value) - self._min)/(self._max - self._min)
        self.interpolate()

    def interpolate(self):
        for i in range(3):
            self.target_vector[i] = self._from[i] + self.t*(self._to[i] - self._from[i])

    def move(self, delta):
        if self.t + delta < 0:
            self.t = 0.0
        elif self.t + delta > 1:
            self.t = 1.0
        else:
            self.t += delta

        self.interpolate()

    def update(self):
        if self.current_vector != self.target_vector:
            if self._type == "linear":
                self.element.setPos(self.current_vector[0], self.current_vector[1], self.current_vector[2])
            else:
                self.element.setHpr(self.current_vector[0], self.current_vector[1], self.current_vector[2])

            for i in range(3):
                if self.current_vector[i] - self.target_vector[i] > self.SPEED:
                    self.current_vector[i] -= self.SPEED/3.0
                elif self.current_vector[i] - self.target_vector[i] < -self.SPEED:
                    self.current_vector[i] += self.SPEED/3.0
                else:
                    self.current_vector[i] = self.target_vector[i]

class MAMEDevice(ShowBase):

    def __init__(self, layout_dir):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.layout_dir = layout_dir
        self.loadXMLlayout()

        self.setup_MAME_IPC()
        self.setup_model()
        self.setup_scene()
        self.setup_event_handlers()

        # Add procedures to the task manager.
        self.taskMgr.add(self.update_camera, "UpdateCameraTask")
        self.taskMgr.add(self.update_motion, "UpdateMotionTask")
        self.taskMgr.add(self.update_stroboscopic_lights, "UpdateStroboscopicLightsTask")
        self.taskMgr.add(self.check_outputs, "CheckOutputsTask")

    def setup_MAME_IPC(self):
        self.light_elements = {}
        self.stroboscopic_lights = []
        self.nodes_by_id = {}
        self.motion = {}
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
                newNode.setPosHpr(float(position[0]),
                                  float(position[1]),
                                  float(position[2]),
                                  float(hpr[0]),
                                  float(hpr[1]),
                                  float(hpr[2]))
                if id:
                    self.nodes_by_id[id] = newNode

            elif element.tagName == 'model':
                id = self._getValue(element, 'id', None)
                name = self._getValue(element, 'name', None)
                filename = self._getValue(element, 'filename', None)
                position = self._getVector(element, 'position', (0.0, 0.0, 0.0))
                hpr = self._getVector(element, 'hpr', (0.0, 0.0, 0.0))
                color = self._getVector(element, 'color', (1,1,1,1))
                spec = self._getVector(element, 'specular', (1,1,1,1))
                metalic = self._getBoolean(element, 'metalic', False)
                shininess = self._getValue(element, 'shininess', 20)
                scale = self._getValue(element, 'scale', 0.005)
                newNode = self.load_3D_Model(id=id,
                                             name=name,
                                             filename=filename,
                                             position=position,
                                             hpr=hpr,
                                             color=LVecBase4f(color[0], color[1], color[2], color[3]),
                                             metalic=metalic,
                                             shininess=shininess,
                                             specular=LVecBase4f(spec[0], spec[1], spec[2], spec[3]),
                                             scale=scale,
                                             parent=currentNode)

            elif element.tagName == 'light':
                id = self._getValue(element, 'id', None)
                att = self._getVector(element, 'attenuation', (0.1, 0.04, 0.0))
                color = self._getVector(element, 'color', (1, 1, 1, 1))
                position = self._getVector(element, 'position', (0.0, 0.0, 0.0))
                specular = self._getVector(element, 'specular', (1, 1, 1, 1))
                stroboscopic = self._getBoolean(element, 'stroboscopic', False)
                spot = self._getBoolean(element, 'spot', False)
                lookat = self._getValue(element, 'lookat', None)
                newNode = self.addLight(id=id,
                                        parent=currentNode,
                                        position=position,
                                        attenuation=LVector3(att[0], att[1], att[2]),
                                        specular=specular,
                                        stroboscopic=stroboscopic,
                                        spot=spot,
                                        lookat=lookat,
                                        color=LVecBase4f(color[0], color[1], color[2], color[3]))

            elif element.tagName == 'camera':
                id = self._getValue(element, 'id', None)
                position = self._getVector(element, 'position', (0.0, 0.0, 0.0))
                lookat = self._getValue(element, 'lookat', "device_root")
                fov = float(self._getValue(element, 'fov', 80))
                newNode = self.setupCamera(id=id, parent=currentNode, position=position, lookat=lookat, fov=fov)

            elif element.tagName == 'motion':
                id = self._getValue(element, 'id', None)
                target = self._getValue(element, 'target', None)
                _type = self._getValue(element, 'type', None)
                _min = float(self._getValue(element, 'min', None))
                _max = float(self._getValue(element, 'max', None))
                _from = self._getVector(element, 'from', None)
                _to = self._getVector(element, 'to', None)
                newNode = self.setupMotion(id=id, target=target, _type=_type,
                                           _min=_min, _max=_max,
                                           _from=_from, _to=_to)

            self.parseModelElements(newNode, element.childNodes)

    def setup_event_handlers(self):
        # listen to keys for controlling the lights
        self.accept("escape", sys.exit)
        self.accept("p", self.toggleAllLights)
        self.accept("h", self.manual_rotation, [0.1])
        self.accept("g", self.manual_rotation, [-0.1])

    def setup_scene(self):
        # This creates the on screen title that is in every tutorial
        self.title = OnscreenText(text=self.device_title,
                                  style=1, fg=(1, 1, 0, 1), shadow=(0, 0, 0, 0.5),
                                  pos=(0.87, -0.95), scale = .07)

        self.load_3D_Model(filename = "../common/egg/disco_hall", color=(0.5, 0.6, 0.5, 1), position=(0, 80, -10), hpr=(90, 0, 0), scale=1)

        # First we create an ambient light. All objects are affected by ambient light equally
        # Create and name the ambient light
        self.ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
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

    def load_3D_Model(self, position, hpr, color, metalic=False, scale=0.005, id=None, name=None, filename=None, parent=None, shininess=None, specular=None):
        if parent is None:
            parent = render

        if name:
            filename = 'egg/%s_%s' % (self.device_id, name)

        model = loader.loadModel('%s/%s' % (self.layout_dir, filename))
        model.reparentTo(parent)
        model.setColor(color)
        model.setPosHpr(position[0], position[1], position[2], hpr[0], hpr[1], hpr[2])
        model.setScale(float(scale))

        if metalic:
            m = Material()
            m.setShininess(shininess)
            m.setSpecular(specular)
            model.setMaterial(m)

        if id:
            self.nodes_by_id[id] = model
        return model

    def addLight(self, id, parent, attenuation, position, color, specular, stroboscopic, spot, lookat):
        if spot:
            slight = Spotlight(id)
            slight.setColor(VBase4(1, 1, 1, 1))
            lens = PerspectiveLens()
            slight.setLens(lens)
            light = render.attachNewNode(slight)
            light.setPos(LVector3(position[0], position[1], position[2]))
            if lookat == None:
                light.lookAt(parent)
            else:
                light.lookAt(render.find("**/"+lookat))
        else:
            light = parent.attachNewNode(PointLight(id))
            light.node().setAttenuation(attenuation)
            light.setPos(LVector3(position[0], position[1], position[2]))
        light.node().setColor(color)
        light.node().setSpecularColor(specular)
        render.setLight(light)
        self.light_elements[id] = light
        if stroboscopic:
            self.stroboscopic_lights.append(id)

        if id:
            self.nodes_by_id[id] = light
        return light

    def setupMotion(self, id, target, _type,
                          _from, _to, _min=0.0, _max=1.0):
        assert(not type in ['linear', 'angular'])
        assert(target != None)
        assert(_from != None)
        assert(_to != None)

        element = self.nodes_by_id[target]
        self.motion[id] = MotionControl(element, _type, _from, _to, _min, _max, element.getPos(), element.getHpr())

    def setupCamera(self, id, parent, position, lookat, fov):
        #TODO: register multiple cameras and add UI controls to cycle through them
        self.camLens.setFov(fov)
        self.camera.setPos(LVector3(position[0], position[1], position[2]))
        self.camera.lookAt(self.nodes_by_id[lookat])

    def manual_rotation(self, delta):
        keys = self.motion.keys()
        if len(keys) > 0:
            m = self.motion[keys[0]]
            m.move(delta)

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

    def check_outputs(self, task):
        try:
            class_, pidnum, name, state = self.FIFO.readline().strip().split()
        except ValueError:
            return Task.cont

        if name in self.motion.keys():
            self.motion[name].setValue(state)
        elif name in self.light_elements.keys():
            light = self.light_elements[name]
            if state == '1':
                render.setLight(light)
            else:
                render.clearLight(light)

        return Task.cont

    def update_stroboscopic_lights(self, taskid):
        for light_name in self.stroboscopic_lights:
            light = self.light_elements[light_name]
            #render.setLight(light)
            #continue
            
            if render.hasLight(light):
                if random()*100 < 80:
                    render.clearLight(light)
            else:
                if random()*100 < 5:
                    render.setLight(light)
            
        return Task.cont

    def update_motion(self, task):
        for k in self.motion.keys():
            self.motion[k].update()
        return Task.cont

    def update_camera(self, task):
        target = render.find("**/static")
        angleDegrees = task.time * 12.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(0 + 20 * sin(angleRadians), 60 + -20.0 * cos(angleRadians), 5)
        self.camera.lookAt(target, (0,0,2))
        return Task.cont

import sys
if len(sys.argv) != 2:
    print "\n\tusage: %s <device_id>\n\n" % sys.argv[0]
    exit(-1)

device_id = sys.argv[1]

# Make an instance of our class and run the demo
device = MAMEDevice(device_id)
device.run()
