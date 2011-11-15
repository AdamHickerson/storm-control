#!/usr/bin/python
#
# Handle lamp/laser and filter wheel for STORM2.
#
# Hazen 11/11
#

import time
import sys
from PyQt4 import QtCore, QtGui

import miscControl

# Debugging
import halLib.hdebug as hdebug

# UIs.
import qtdesigner.storm2_misc_ui as miscControlsUi

# Control
import olympus.ix2ucb as ix2ucb
import phidgets.phidget as phidget

#
# Misc Control Dialog Box
#
class AMiscControl(QtGui.QDialog):
    @hdebug.debug
    def __init__(self, parameters, tcp_control, parent = None):
        super(AMiscControl, self).__init__(parameters, tcp_control, parent)

        self.filter_wheel = ix2ucb.IX2UCB()
        self.lamp_servo = phidget.Phidget("c:/Program Files/Phidgets/")

        # we need to stall briefly to give time for 
        # the laser/lamp servo to initialize.
        time.sleep(0.1)

        # UI setup
        self.ui = miscControlsUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(parameters.setup_name + " Misc Control")

        # connect signals
        if self.have_parent:
            self.ui.okButton.setText("Close")
            self.ui.okButton.clicked.connect(self.handleOk)
        else:
            self.ui.okButton.setText("Quit")
            self.ui.okButton.clicked.connect(self.handleQuit)

        # setup laser/lamp
        self.ui.laserButton.clicked.connect(self.handleLaser)
        self.ui.lampButton.clicked.connect(self.handleLamp)
        if self.lamp_servo.atMinimum():
            self.ui.laserButton.setStyleSheet("QPushButton { color: red }")
            self.ui.lampButton.setStyleSheet("QPushButton { color: black }")
        else:
            self.ui.laserButton.setStyleSheet("QPushButton { color: black }")
            self.ui.lampButton.setStyleSheet("QPushButton { color: red }")

        # setup filter wheel
        self.filters = [self.ui.filter1Button,
                        self.ui.filter2Button,
                        self.ui.filter3Button,
                        self.ui.filter4Button,
                        self.ui.filter5Button,
                        self.ui.filter6Button]
        for filter in self.filters:
            filter.clicked.connect(self.handleFilter)
        self.filters[self.filter_wheel.getPosition()-1].click()

    @hdebug.debug
    def handleFilter(self):
        for i, filter in enumerate(self.filters):
            if filter.isChecked():
                filter.setStyleSheet("QPushButton { color: red}")
                self.filter_wheel.setPosition(i+1)
                self.parameters.filter_position = i
            else:
                filter.setStyleSheet("QPushButton { color: black}")

    @hdebug.debug
    def handleLamp(self):
        self.ui.laserButton.setStyleSheet("QPushButton { color: black }")
        self.ui.lampButton.setStyleSheet("QPushButton { color: red }")
        self.lamp_servo.goToMax()

    @hdebug.debug
    def handleLaser(self):
        self.ui.laserButton.setStyleSheet("QPushButton { color: red }")
        self.ui.lampButton.setStyleSheet("QPushButton { color: black }")
        self.lamp_servo.goToMin()
        
    @hdebug.debug
    def handleOk(self):
        self.hide()

    @hdebug.debug
    def newParameters(self, parameters):
        self.parameters = parameters
        names = parameters.filter_names
        if (len(names) == 6):
            for i in range(6):
                self.filters[i].setText(names[i])
        self.filters[self.parameters.filter_position].click()

    @hdebug.debug
    def quit(self):
        self.filter_wheel.shutDown()
        self.lamp_servo.shutDown()

#
# The MIT License
#
# Copyright (c) 2011 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
