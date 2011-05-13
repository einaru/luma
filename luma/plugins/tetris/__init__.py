# -*- coding: utf-8 -*-

from base.util.IconTheme import iconFromTheme
from .Tetris import Tetris

lumaPlugin = True
pluginName = "tetris"
pluginUserString = "Tetris"
version = "0.1"
author = "Jan Bodnar"
description = "Tetris from http://zetcode.com/tutorials/pyqt4/thetetrisgame/"

def getIcon():
    return iconFromTheme('luma-tetris-plugin', ':/icons/plugins/tetris')
    

def getPluginWidget(parent, mainwin):
    widget = Tetris()
    return widget
    

def getPluginSettingsWidget(parent):
    return None

def postprocess():
    return

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
