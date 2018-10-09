from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

import os
from core import rpi
from glob import glob
from colour import Color
import numpy as np
from threading import Thread
#os.environ['KIVY_WINDOW'] = 'egl_rpi' 

#from kivy.config import Config
#Config.set('graphics', 'width', '800')
#Config.set('graphics', 'height', '480')

#Config.getint('kivy', 'show_fps')




root = Builder.load_string('''
#:import SwapTransition kivy.uix.screenmanager.SwapTransition
#:set spac 20
#:set pad_side 10
#:set pad_bot 30
#:set x_screen 480
#:set y_screen 800
#:set sp_act 100
#:set sp_nor 128
#:set control_axis 'X'
#:set sp_act_control 45
#:set sp_nor_control 60
#:set control_size_hint .3
#:set sp_act_control_btn 50

<MyCheckBox@CheckBox>:
    color: 1, 1, 1, 1
    size_hint: 0.5, 1


<MyLabel@ButtonBehavior+Label>:
    text_size: self.size
    valign: 'center'
    font_size: '17sp'
    color: 1, 1, 1, 1


<MyLabelCheckBox@BoxLayout>:
    mycheckbox: cb
    text: ''
    group: ''

    MyCheckBox:
        id: cb
        group: root.group

    MyLabel:
        on_press: cb._do_press()
        text: root.text

<MyButtonAxis@Button>:
    control_axis:  'X'

<MySlider@Slider>:
    ext_or_bed: True

<MainScreen>:
    screen_main:         sm
    t_e_now:             _id_e_now
    t_e_limit:           _id_e_lim
    t_c_now:             _id_c_now
    t_c_limit:           _id_c_lim
    files_scroll:        _id_files_scroll
    control_check_axis:  _id_control_checkbutton
    control_button_axis: _id_control_button_axis
    slider_temp:         _id_slider_temp
    label_temp:          _id_text_temp
    
    main_button_init:    _id_main_button_init
    main_button_file:    _id_main_button_file
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
                transition: SwapTransition()
                id: sm
                Screen:
                    name: 'init'
                    FloatLayout:
                        pos_hint: {'x': 0.025, 'y': 0.05}
                        canvas.before:
                            Color:
                                rgba: (1,1,1,0.2)
                            Rectangle:
                                source: './imagenes/temperature.png'
                                size: [450, 300]
                                pos: self.pos
                    
                        Label:
                            pos_hint: {'x': -0.20, 'y': -.075}
                            font_size: dp(20)
                            halign: "left"
                            valign: 'middle'
                            text: '[b]Hola! ¿Qué haremos hoy?[/b]'
                            markup: True
                    
                        Label:
                            pos_hint: {'x': 0.165, 'y': -.00975}
                            font_size: dp(20)
                            halign: "left"
                            valign: 'middle'
                            text: '[b]T° Extrusor[/b]'
                            markup: True
                        
                        Label:
                            pos_hint: {'x': 0.165, 'y': -.143}
                            font_size: dp(20)
                            halign: "left"
                            valign: 'middle'
                            text: '[b]T° Cama    [/b]'
                            markup: True
                            
                        Label:
                            id:        _id_e_now
                            pos_hint:  {'x': 0.3, 'y': -.00975}
                            font_size: dp(20)
                            halign:    "left"
                            valign:    'middle'
                            markup:    True
                        Label:
                            pos_hint:  {'x': 0.35, 'y': -.00975}
                            font_size: dp(20)
                            halign:    "left"
                            valign:    'middle'
                            text:      '[b]/[/b]'
                            markup:     True
                        Label:
                            id:        _id_e_lim
                            pos_hint:  {'x': 0.41, 'y': -.00975}
                            font_size: dp(20)
                            halign:    "left"
                            valign:    'middle'
                            markup:    True
                        Label:
                            id:        _id_c_now
                            pos_hint:  {'x': 0.3, 'y': -.143}
                            font_size: dp(20)
                            halign:    "left"
                            valign:    'middle'
                            markup:    True
                        Label:
                            pos_hint:  {'x': 0.35, 'y': -.143}
                            font_size: dp(20)
                            halign:    "left"
                            valign:    'middle'
                            text:      '[b]/[/b]'
                            markup:    True
                        Label:
                            id:        _id_c_lim
                            pos_hint:  {'x': 0.41, 'y': -.143}
                            font_size: dp(20)
                            halign:    "left"
                            valign:    'middle'
                            markup:    True
                        
                Screen:
                    name: 'control'
                    FloatLayout:
                        pos_hint: {'x': 0.02, 'y': 0.025}
                        canvas.before:
                            Color:
                                rgba: (1,1,1,0.2)
                            Rectangle:
                                source: './imagenes/temperature.png'
                                size: [450, 315]
                                pos: self.pos
                    
                    FloatLayout:
                        Label:
                            pos_hint: {'x': -0.20, 'y': .3}
                            font_size: dp(20)
                            halign: "left"
                            valign: 'middle'
                            text: '[b]Movimiento[/b]'
                            markup: True
                        
                        BoxLayout:
                            size_hint: (.4, None)
                            spacing: spac
                            pos_hint: {'x': .1, 'y': .475}
                            id:  _id_control_checkbutton
                                
                            CheckBox:
                                text: ''
                                state: 'down'
                                group: 'control_buttons_axis'
                                on_state: root.control_press_axis_x()
                                allow_no_selection: False
                                canvas:
                                    Color:
                                        rgba: [1,1,1,1]
                                    Rectangle:
                                        source: './imagenes/B_1_inicio_normal.png'
                                        size: (sp(sp_act_control), sp(sp_act_control)) if self.active else (sp(sp_nor_control), sp(sp_nor_control))
                                        pos: (int(self.center_x - sp(sp_act_control // 2)), int(self.center_y - sp(sp_act_control // 2))) if self.active else (int(self.center_x - sp(sp_nor_control / 2)), int(self.center_y - sp(sp_nor_control / 2)))
                            
                            CheckBox:
                                text: ''
                                group: 'control_buttons_axis'
                                on_state: root.control_press_axis_y()
                                allow_no_selection: False
                                canvas:
                                    Color:
                                        rgba: [1,1,1,1]
                                    Rectangle:
                                        source: './imagenes/B_1_inicio_normal.png'
                                        size: (sp(sp_act_control), sp(sp_act_control)) if self.active else (sp(sp_nor_control), sp(sp_nor_control))
                                        pos: (int(self.center_x - sp(sp_act_control // 2)), int(self.center_y - sp(sp_act_control // 2))) if self.active else (int(self.center_x - sp(sp_nor_control / 2)), int(self.center_y - sp(sp_nor_control / 2)))
                            
                            CheckBox:
                                text: ''
                                group: 'control_buttons_axis'
                                on_state: root.control_press_axis_z()
                                allow_no_selection: False
                                canvas:
                                    Color:
                                        rgba: [1,1,1,1]
                                    Rectangle:
                                        source: './imagenes/B_1_inicio_normal.png'
                                        size: (sp(sp_act_control), sp(sp_act_control)) if self.active else (sp(sp_nor_control), sp(sp_nor_control))
                                        pos: (int(self.center_x - sp(sp_act_control // 2)), int(self.center_y - sp(sp_act_control // 2))) if self.active else (int(self.center_x - sp(sp_nor_control / 2)), int(self.center_y - sp(sp_nor_control / 2)))
                            
                            CheckBox:
                                text: ''
                                group: 'control_buttons_axis'
                                on_state: root.control_press_axis_e()
                                allow_no_selection: False
                                canvas:
                                    Color:
                                        rgba: [1,1,1,1]
                                    Rectangle:
                                        source: './imagenes/B_1_inicio_normal.png'
                                        size: (sp(sp_act_control), sp(sp_act_control)) if self.active else (sp(sp_nor_control), sp(sp_nor_control))
                                        pos: (int(self.center_x - sp(sp_act_control // 2)), int(self.center_y - sp(sp_act_control // 2))) if self.active else (int(self.center_x - sp(sp_nor_control / 2)), int(self.center_y - sp(sp_nor_control / 2)))
                            
                        BoxLayout:
                            size_hint: (.4525, 0.275)
                            spacing: 7
                            pos_hint: {'x': 0.07, 'y': .3}
                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_release: root.control_move_left_10()

                                background_color: (0,0,0,0)
                                
                                canvas:
                                    Color:
                                        rgba: (1,1,1,.75)
                                    Rectangle:
                                        size: (sp(sp_act_control_btn), sp(sp_act_control_btn))
                                        pos: (int(self.center_x - sp(sp_act_control_btn // 2)), int(self.center_y - sp(sp_act_control_btn // 2)))
                                        source: './imagenes/left_10.png'
                            
                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_release: root.control_move_left_1()
                                background_color: (0,0,0,0)
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(sp_act_control_btn), sp(sp_act_control_btn))
                                        pos: (int(self.center_x - sp(sp_act_control_btn // 2)), int(self.center_y - sp(sp_act_control_btn // 2)))
                                        source: './imagenes/left_1.png'

                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_release: root.control_move_left_01()

                                background_color: (0,0,0,0)
                                
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(sp_act_control_btn), sp(sp_act_control_btn))
                                        pos: (int(self.center_x - sp(sp_act_control_btn // 2)), int(self.center_y - sp(sp_act_control_btn // 2)))
                                        source: './imagenes/left_01.png'
                            
                            MyButtonAxis:
                                id:        _id_control_button_axis
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_release: root.control_press_home_axis()

                                background_color: (0,0,0,0)
                                
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(sp_act_control_btn), sp(sp_act_control_btn))
                                        pos: (int(self.center_x - sp(sp_act_control_btn // 2)), int(self.center_y - sp(sp_act_control_btn // 2)))
                                        source: './imagenes/home_x.png' if self.control_axis == 'X' else './imagenes/home_y.png' if self.control_axis == 'Y' else './imagenes/home_z.png' if self.control_axis == 'Z' else './imagenes/home_e.png' 
                            
                            
                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_release: root.control_move_right_01()

                                background_color: (0,0,0,0)
                                
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(sp_act_control_btn), sp(sp_act_control_btn))
                                        pos: (int(self.center_x - sp(sp_act_control_btn // 2)), int(self.center_y - sp(sp_act_control_btn // 2)))
                                        source: './imagenes/right_01.png'
                            
                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_release: root.control_move_right_1()

                                background_color: (0,0,0,0)
                                
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(sp_act_control_btn), sp(sp_act_control_btn))
                                        pos: (int(self.center_x - sp(sp_act_control_btn // 2)), int(self.center_y - sp(sp_act_control_btn // 2)))
                                        source: './imagenes/right_1.png'
                                        
                            
                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_release: root.control_move_right_10()

                                background_color: (0,0,0,0)
                                
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(sp_act_control_btn), sp(sp_act_control_btn))
                                        pos: (int(self.center_x - sp(sp_act_control_btn // 2)), int(self.center_y - sp(sp_act_control_btn // 2)))
                                        source: './imagenes/right_10.png'
                    
                    FloatLayout:
                        BoxLayout:
                            size_hint: (.4025, .2)
                            spacing: 20
                            pos_hint: {'x': 0.095, 'y': .125}
                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_press: root.control_home_all()
                                background_color: (0,0,0,0)
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(190), sp(35))
                                        pos: (int(self.center_x - sp(190 // 2)), int(self.center_y - sp(35 // 2)))
                                        source: './imagenes/left_1.png'

                            Button:
                                size_hint: (control_size_hint, .5)
                                text: ''
                                on_press: root.control_motors_off()
                                background_color: (0,0,0,0)
                                canvas:
                                    Color:
                                        rgba: (1,1,1,0.75)
                                    Rectangle:
                                        size: (sp(190), sp(35))
                                        pos: (int(self.center_x - sp(190 // 2)), int(self.center_y - sp(35 // 2)))
                                        source: './imagenes/left_1.png'
                                        
                    FloatLayout:
                        pos_hint: {'x': 0.565, 'y': 0.025}
                        canvas.before:
                            Color:
                                rgba: (1,1,1,0.2)
                            Rectangle:
                                source: './imagenes/temperature.png'
                                size: [325, 315]
                                pos: self.pos
                    
                    FloatLayout:
                        Label:
                            pos_hint: {'x': 0.2725, 'y': .3}
                            font_size: dp(20)
                            halign: "left"
                            valign: 'middle'
                            text: '[b]Temperatura[/b]'
                            markup: True
                        
                        BoxLayout:
                            size_hint: (.25, .2)
                            spacing: 20
                            pos_hint: {'x': 0.65, 'y': .55}
                            CheckBox:
                                state: 'down'
                                text: ''
                                group: 'control_buttons_temp'
                                on_state: root.control_press_temp_extrusor()
                                allow_no_selection: False
                                canvas:
                                    Color:
                                        rgba: [1,1,1,1]
                                    Rectangle:
                                        source: './imagenes/B_1_inicio_normal.png'
                                        size: (sp(sp_act_control), sp(sp_act_control)) if self.active else (sp(sp_nor_control), sp(sp_nor_control))
                                        pos: (int(self.center_x - sp(sp_act_control // 2)), int(self.center_y - sp(sp_act_control // 2))) if self.active else (int(self.center_x - sp(sp_nor_control / 2)), int(self.center_y - sp(sp_nor_control / 2)))
                            
                            CheckBox:
                                text: ''
                                group: 'control_buttons_temp'
                                on_state: root.control_press_temp_bed()
                                allow_no_selection: False
                                canvas:
                                    Color:
                                        rgba: [1,1,1,1]
                                    Rectangle:
                                        source: './imagenes/B_1_inicio_normal.png'
                                        size: (sp(sp_act_control), sp(sp_act_control)) if self.active else (sp(sp_nor_control), sp(sp_nor_control))
                                        pos: (int(self.center_x - sp(sp_act_control // 2)), int(self.center_y - sp(sp_act_control // 2))) if self.active else (int(self.center_x - sp(sp_nor_control / 2)), int(self.center_y - sp(sp_nor_control / 2)))
                        
                        MySlider:
                            id:                _id_slider_temp
                            on_touch_move:     if self.collide_point(*args[1].pos): root.slider_temp_move()
                            on_touch_up:       if self.collide_point(*args[1].pos): root.slider_temp_move()
                            size_hint:         (.325, .1)
                            pos_hint:          {'x': 0.615, 'y': .4}
                            min:               0
                            max:               250 if self.ext_or_bed else 50
                            value:             0
                            orientation:       'horizontal'
                            value_track:       True
                            value_track_color: [0,0,1,1]
                            step:               0.25
                        
                        Label:
                            id:             _id_text_temp
                            font_size:      dp(18)
                            text:           '[b]T:  0°C[/b]'
                            markup:         True
                            pos_hint:       {'x': 0.15, 'y': -.3}
                            
                        Button:
                            size_hint: (0.2, .15)
                            pos_hint:  {'x': .725, 'y': 0.125}
                            text: ''
                            on_press: root.control_ajustar_temp()
                            background_color: (0,0,0,1)
                            canvas:
                                Color:
                                    rgba: (1,1,1,0.75)
                                Rectangle:
                                    size: (sp(190), sp(35))
                                    pos: (int(self.center_x - sp(190 // 2)), int(self.center_y - sp(35 // 2)))
                                    source: './imagenes/left_1.png'
                            
                            
                        
                        

                        
                Screen:
                    name: 'tools'
                    Label:
                        text: 'Tools' 
                Screen:
                    name: 'files'
                    FloatLayout:
                        
                        ScrollView:
                            size_hint: (0.615, 0.6)
                            pos_hint:  {'x':-.025, 'y':.2}
                            id: _id_files_scroll
                        
                        FloatLayout:
                            pos_hint: {'x': 0., 'y': 0.115}
                            canvas.before:
                                Color:
                                    rgba: (1,1,1,0.2)
                                Rectangle:
                                    source: './imagenes/temperature.png'
                                    size: [525, 275]
                                    pos: self.pos
                        Button:
                            canvas:
                                Color:
                                    rgba: (0,0,0,.35)
                                Rectangle:
                                    source: './imagenes/temperature.png'
                                    size: (sp(sp_act) + 100, sp(sp_act)) 
                                    pos: (int(self.center_x - sp(sp_act // 2)) - 50, int(self.center_y - sp(sp_act // 2)))
                            pos_hint: {'x': 0.675, 'y': 0.35}
                            size_hint: (0.3, .3)
                            text: '[b]Imprimir[/b]'
                            markup: True
                            on_release: root.press_imprimir()
                            background_normal: ''
                            background_color: (0,0,0,0)
                            font_size: '17sp'
                            

                Screen:
                    name: 'mode'
                    Label:
                        text: 'mode' 
                
        
        BoxLayout:
            size_hint: (1, 0.35)
            spacing: spac
            padding: [pad_side, 0, pad_side, pad_bot]
            
            CheckBox:
                id: _id_main_button_init
                group: 'buttons'
                text: ""
                on_state: sm.current = 'init'
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
                on_state: sm.current = 'control'
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
                on_state: sm.current = 'tools'
                allow_no_selection: False
                canvas:
                    Color:
                        rgba: self.color
                    Rectangle:
                        source: './imagenes/B_3_herramientas.png'
                        size: (sp(sp_act), sp(sp_act)) if self.active else (sp(sp_nor), sp(sp_nor))
                        pos: (int(self.center_x - sp(sp_act // 2)), int(self.center_y - sp(sp_act // 2))) if self.active else (int(self.center_x - sp(sp_nor / 2)), int(self.center_y - sp(sp_nor / 2)))
                
            CheckBox:
                id:    _id_main_button_file
                group: 'buttons'
                text: ""
                on_state: sm.current = 'files'
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
                on_state: sm.current = 'mode'
                allow_no_selection: False
                canvas:
                    Color:
                        rgba: self.color
                    Rectangle:
                        source: './imagenes/B_5_modo.png'
                        size: (sp(sp_act), sp(sp_act)) if self.active else (sp(sp_nor), sp(sp_nor))
                        pos: (int(self.center_x - sp(sp_act // 2)), int(self.center_y - sp(sp_act // 2))) if self.active else (int(self.center_x - sp(sp_nor / 2)), int(self.center_y - sp(sp_nor / 2)))
''')


class MyLabelCheckBox(BoxLayout):
    pass

class MainScreen(Screen):
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.Rpi = rpi()
        self.paths = []
        self.to_print = ''
        red  = Color('red')
        blue = Color('blue')
        self.colors_ext = list(blue.range_to(red, 251))
        self.colors_bed = list(blue.range_to(red, 51))
        self.past_value_ext = 0
        self.past_value_bed = 0
        self.slider_temp.flag_event_ext_bed = False
        self.ext_or_bed = True
        
        self.layout_for_scrolls = GridLayout(cols=1, spacing=1, size_hint_y=None)
        self.layout_for_scrolls.bind(minimum_height=self.layout_for_scrolls.setter('height'))
        
        self.files_scroll.add_widget(self.layout_for_scrolls)
        
        
    
    def ArduinoRead(self, dt):
        self.Rpi._ArduinoRead()
    
    def ArduinoWrite(self, dt):
        self.Rpi._ArduinoWrite()
        
    def requestTemperature(self, dt):
        self.Rpi._requestTemperature()

    def update_temperature(self, dt):
        t_e_now, t_e_limit, t_c_now, t_c_limit = self.Rpi.get_temp()
#        t_e_now, t_e_limit, t_c_now, t_c_limit = [37,0,200,200]
        
        self.t_e_now.text   = '[b]{t:}[/b]'.format(t=t_e_now)
        self.t_e_limit.text = '[b]{t:}[/b]'.format(t=t_e_limit)
        self.t_c_now.text   = '[b]{t:}[/b]'.format(t=t_c_now)
        self.t_c_limit.text = '[b]{t:}[/b]'.format(t=t_c_limit)
    
    def check_usb(self, dt):
        paths = sorted(glob('/media/usb*/*.gcode', recursive=True))
        if set(paths) != set(self.paths):
            self.paths = paths
            # hubo una variacion entre los paths, antiguo y nuevo
            # la limpio de los children para actualizar
            self.layout_for_scrolls.clear_widgets()
            # suposicion: usb unico
            multiple_usb = False
            if len(paths) > 0:
                # verifica si los gcode estan en un solo usb
                verify = set()
                for path in paths:
                    verify.add(os.path.dirname(path))
                    
                
                if len(list(verify)) > 1:
                    # es con mutiples usbs
                    multiple_usb = True
                for path in paths:
                    if multiple_usb:
                        p = os.path.basename(os.path.dirname(path)) + '/' + os.path.basename(path)[:-6]
                    else:
                        p = os.path.basename(path)[:-6]
                        
                    btn                 = MyLabelCheckBox()
                    btn.size_hint_y     = None
                    btn.height          = 40
                    btn.mycheckbox.path = path
                    btn.group           = 'scrolls'
                    btn.text            = str(p[:35])
                    btn.mycheckbox.text = p[:35]
                    
                    btn.mycheckbox.bind(active=self.press_scrolls)
                    #btn.background_radio_down
                    #with btn.canvas:
                        #Color((0.25,0.25,0.25,0.65))
                        #btn.rect = Rectangle(source='./images/arrow_top.png', pos=(btn.center_x, btn.center_y))
                        
                    #btn.canvas.before.Color.rgba = (0.25,0.25,0.25,0.65)
                    #Color:
                        #rgba: (0.25,0.25,0.25,0.65)
                    #Rectangle:
                        #pos: (0, x_screen - 30)
                        #size: self.size
                    self.layout_for_scrolls.add_widget(btn)
            
    def press_scrolls(self, instance, value):
        self.to_print = instance.path

    def press_imprimir(self):
        if len(self.to_print) > 0 and os.path.isfile(self.to_print):
            self.main_button_init.state = 'down'
            self.main_button_file.state = 'normal'
            self.screen_main.current = 'init'
            self.Rpi.parameters['Imprimiendo']['archivo'] = self.to_print
            self.Rpi.parameters['status'] = 'priting'
#            self.Rpi.functionExec.put_nowait('imprime')
            Thread(target=self.Rpi.Priting).start()
#            Clock.schedule_once(self.Rpi.Priting, .6)
            
            # ahora hay que bloquear los demas parametros y modificar el label del inicio
            pass
            
    def control_press_axis_x(self):
        self.control_button_axis.control_axis = 'X'
        #global_idmap['control_axis'] = 'X'
    def control_press_axis_y(self):
        self.control_button_axis.control_axis = 'Y'
        #global_idmap['control_axis'] = 'Y'
    def control_press_axis_z(self):
        self.control_button_axis.control_axis = 'Z'
        #global_idmap['control_axis'] = 'Z'
    def control_press_axis_e(self):
        self.control_button_axis.control_axis = 'E'
        #global_idmap['control_axis'] = 'E'
    
    def control_press_home_axis(self):
        print('home\t{}'.format(self.control_button_axis.control_axis))
        self.Rpi.control_wo_print('home', self.control_button_axis.control_axis)
    def control_move_left_10(self):
        print('mover_{}\t-10'.format(self.control_button_axis.control_axis.lower()))
        self.Rpi.control_wo_print('mover_{}'.format(self.control_button_axis.control_axis.lower()), -10)
    def control_move_left_1(self):
        print('mover_{}\t-1'.format(self.control_button_axis.control_axis.lower()))
        self.Rpi.control_wo_print('mover_{}'.format(self.control_button_axis.control_axis.lower()), -1)
    def control_move_left_01(self):
        print('mover_{}\t-.1'.format(self.control_button_axis.control_axis.lower()))
        self.Rpi.control_wo_print('mover_{}'.format(self.control_button_axis.control_axis.lower()), -.1)
    def control_move_right_10(self):
        print('mover_{}\t10'.format(self.control_button_axis.control_axis.lower()))
        self.Rpi.control_wo_print('mover_{}'.format(self.control_button_axis.control_axis.lower()), 10)
    def control_move_right_1(self):
        print('mover_{}\t1'.format(self.control_button_axis.control_axis.lower()))
        self.Rpi.control_wo_print('mover_{}'.format(self.control_button_axis.control_axis.lower()), 1)
    def control_move_right_01(self):
        print('mover_{}\t.1'.format(self.control_button_axis.control_axis.lower()))
        self.Rpi.control_wo_print('mover_{}'.format(self.control_button_axis.control_axis.lower()), .1)
    def control_home_all(self):
        print('home\tall')
        self.Rpi.control_wo_print('home', 'all')
    def control_motors_off(self):
        print('apagar_motores')
        self.Rpi.control_wo_print('apagar_motores')
        
    def control_press_temp_extrusor(self):
        if not self.slider_temp.ext_or_bed:
            self.past_value_bed             = self.slider_temp.value
            self.slider_temp.value          = self.past_value_ext
            self.slider_temp.ext_or_bed     = True
            self.slider_temp_move()
        
    
    def control_press_temp_bed(self):
        if self.slider_temp.ext_or_bed:
            self.past_value_ext             = self.slider_temp.value
            self.slider_temp.value          = self.past_value_bed
            self.slider_temp.ext_or_bed     = False
            self.slider_temp_move()
    
    def slider_temp_move(self):
        if self.slider_temp.ext_or_bed:
            color_now = self.colors_ext[int(self.slider_temp.value + .5)]
        else:
            color_now = self.colors_bed[int(self.slider_temp.value + .5)]

        a = [0,0,0,1]
        a[:-1] = color_now.rgb
        self.slider_temp.value_track_color = a
        
        self.label_temp.text = '[b]T:  {t}°C[/b]'.format(t=int(self.slider_temp.value + .5))
    
    def control_ajustar_temp(self):
        #extrusor
        if self.slider_temp.ext_or_bed:
            print('calentar_boq\t{}'.format(int(self.slider_temp.value + .5)))
#            self.Rpi.control_wo_print('calentar_boq', int(self.slider_temp.value + .5))
        else:
            print('calentar_cama\t{}'.format(int(self.slider_temp.value + .5)))
#            self.Rpi.control_wo_print('calentar_cama', int(self.slider_temp.value + .5))
        
        
    def on_stops(self):
        pass
#        
#        for thread in self.Rpi.thread:
#            thread.join()
#        del self.Rpi
    
            

class MyApp(App):

    def build(self):
        self.My = MainScreen()

        return self.My
    
    def on_start(self):
        
        Clock.schedule_interval(self.My.update_temperature, 0.5)
        Clock.schedule_interval(self.My.check_usb, 0.5)
        
        Clock.schedule_interval(self.My.ArduinoRead, 1/25)
        Clock.schedule_interval(self.My.ArduinoWrite, 1/25)
        Clock.schedule_interval(self.My.requestTemperature, .25)
        
    
    def on_stop(self):
        print('now exit')
        self.My.on_stops()
        
        
    

MyApp().run()
