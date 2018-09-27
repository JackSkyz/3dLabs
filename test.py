from kivy.app import App
from kivy.lang import Builder

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')


root = Builder.load_string('''
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:set spac 20
#:set pad_side 10
#:set pad_bot 30
#:set x_screen 480
#:set y_screen 800
#:set sp_act 100
#:set sp_nor 128

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
        padding: [pad_side, 0, pad_side, pad_bot]
        
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
                    source: './imagenes/B_1_inicio_normal.png'
                    size: (sp(sp_act), sp(sp_act)) if self.active else (sp(sp_nor), sp(sp_nor))
                    pos: (int(self.center_x - sp(sp_act // 2)), int(self.center_y - sp(sp_act // 2))) if self.active else (int(self.center_x - sp(sp_nor / 2)), int(self.center_y - sp(sp_nor / 2)))
        
        CheckBox:
            group: 'buttons'
            text: ""
            on_state: sm.current = 'settings'
            allow_no_selection: False
            canvas:
                Color:
                    rgba: self.color
                Rectangle:
                    source: './imagenes/B_2_control_normal.png'
                    size: (sp(sp_act), sp(sp_act)) if self.active else (sp(sp_nor), sp(sp_nor))
                    pos: (int(self.center_x - sp(sp_act // 2)), int(self.center_y - sp(sp_act // 2))) if self.active else (int(self.center_x - sp(sp_nor / 2)), int(self.center_y - sp(sp_nor / 2)))
        
        
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
                    size: (sp(sp_act), sp(sp_act)) if self.active else (sp(sp_nor), sp(sp_nor))
                    pos: (int(self.center_x - sp(sp_act // 2)), int(self.center_y - sp(sp_act // 2))) if self.active else (int(self.center_x - sp(sp_nor / 2)), int(self.center_y - sp(sp_nor / 2)))
            
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
                    size: (sp(sp_act), sp(sp_act)) if self.active else (sp(sp_nor), sp(sp_nor))
                    pos: (int(self.center_x - sp(sp_act // 2)), int(self.center_y - sp(sp_act // 2))) if self.active else (int(self.center_x - sp(sp_nor / 2)), int(self.center_y - sp(sp_nor / 2)))
            
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
                    size: (sp(sp_act), sp(sp_act)) if self.active else (sp(sp_nor), sp(sp_nor))
                    pos: (int(self.center_x - sp(sp_act // 2)), int(self.center_y - sp(sp_act // 2))) if self.active else (int(self.center_x - sp(sp_nor / 2)), int(self.center_y - sp(sp_nor / 2)))


    

''')



class MyApp(App):

    def build(self):
        return root
    
    def init_on_state(self):
        self.sm.current = 'game'


MyApp().run()
