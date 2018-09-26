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
            rgba: (0.25,0.25,0.25,0.65)
        Rectangle:
            pos: (0, x_screen - 30)
            size: self.size
    
    BoxLayout:
        orientation: 'vertical'

        ScreenManager:
            transition: NoTransition()
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
        size_hint: (1, 0.35)
        spacing: spac
        padding: [pad, 0, pad, pad]
        
        CheckBox:
            group: 'buttons'
            text: ""
            on_state: sm.current = 'game'
            state: 'down'
            allow_no_selection: False
            
            canvas:
                Color:
                    rgba: self.color
                Rectangle:
                    source: './imagenes/B_1_inicio.png'
                    size: sp(128), sp(128)
                    pos: int(self.center_x - sp(64)), int(self.center_y - sp(64))
        
        CheckBox:
            group: 'buttons'
            text: ""
            on_state: sm.current = 'settings'
            allow_no_selection: False
            canvas:
                Color:
                    rgba: self.color
                Rectangle:
                    source: './imagenes/B_2_control.png'
                    size: sp(128), sp(128)
                    pos: int(self.center_x - sp(64)), int(self.center_y - sp(64))
        
        
        CheckBox:
            group: 'buttons'
            text: ""
            on_state: sm.current = 'settings'
            allow_no_selection: False
            canvas:
                Color:
                    rgba: self.color
                Rectangle:
                    source: './imagenes/B_3_herramientas.png'
                    size: sp(128), sp(128)
                    pos: int(self.center_x - sp(64)), int(self.center_y - sp(64))
            
        CheckBox:
            group: 'buttons'
            text: ""
            on_state: sm.current = 'settings'
            allow_no_selection: False
            canvas:
                Color:
                    rgba: self.color
                Rectangle:
                    source: './imagenes/B_4_archivos.png'
                    size: sp(128), sp(128)
                    pos: int(self.center_x - sp(64)), int(self.center_y - sp(64))
            
        CheckBox:
            group: 'buttons'
            text: ""
            on_state: sm.current = 'settings'
            allow_no_selection: False
            canvas:
                Color:
                    rgba: self.color
                Rectangle:
                    source: './imagenes/B_5_modo.png'
                    size: sp(128), sp(128)
                    pos: int(self.center_x - sp(64)), int(self.center_y - sp(64))


    

''')



class MyApp(App):

    def build(self):
        return root


MyApp().run()
