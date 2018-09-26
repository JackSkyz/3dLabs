from kivy.app import App
from kivy.lang import Builder

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')


root = Builder.load_string('''
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:set spac 20
#:set pad 10
#:set x_screen 480
#:set y_screen 800

BoxLayout:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: (1,1,1,1)
        Rectangle:
            pos: self.pos
            size: self.size
            source: './imagenes/background.jpg'
            
            
        Color:
            rgba: (0.25,0.25,0.25,0.7)
        Rectangle:
            pos: (0, x_screen - 30)
            size: self.size
    
    BoxLayout:
        orientation: 'vertical'

        ScreenManager:
            transition: NoTransition()
            size_hint: 1, .8
            id: sm
            Screen:
                name: 'game'
                Label:
                    text: 'Game'

            Screen:
                name: 'settings'
                Label:
                    text: 'Settings' 
    
    BoxLayout:
        
        CheckBox:
            group: 'buttons'
            text: "Settings"
            on_state: sm.current = 'game'
            state: 'down'
            allow_no_selection: False
        
        CheckBox:
            group: 'buttons'
            text: "Settings"
            on_state: sm.current = 'settings'
            allow_no_selection: False
            
        CheckBox:
            group: 'buttons'
            text: "Settings"
            on_state: sm.current = 'settings'
            allow_no_selection: False
            
        CheckBox:
            group: 'buttons'
            text: "Settings"
            on_state: sm.current = 'settings'
            allow_no_selection: False
            
        CheckBox:
            group: 'buttons'
            text: "Settings"
            on_state: sm.current = 'settings'
            allow_no_selection: False
        


    

''')


class MyApp(App):

    def build(self):
        return root


MyApp().run()
