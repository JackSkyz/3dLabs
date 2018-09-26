#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 15:16:25 2018

@author: jack-note
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
#from kivy.config import Config
#Config.set('graphics', 'width', '480')
#Config.set('graphics', 'height', '320')

class StartScreen(Screen):
    pass

class ControlScreen(Screen):
    pass

class ToolsScreen(Screen):
    pass

class FilesScreen(Screen):
    pass

class ModeScreen(Screen):
    pass

class RootScreen(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootScreen()

if __name__ == "__main__":
    MainApp().run()
