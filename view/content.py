from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from datetime import datetime, timedelta
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.tooltip import MDTooltip

from config.settings import _GREEN, _GRAY, _LITE_GRAY, _WHITE, _HELPERS_TEXT_CONT, _HEADS_TABLE_STAND, _HELPERS_TEXT_STAND, _HELPERS_TEXT_CANTHEL, _HELPER_TEXT_REPAIR


class DialogContent(MDFloatLayout):
    def __init__(self, stand = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.size = ("100dp", "380dp")
        self.on_start(stand)

    def on_start(self, stand):
        name_stand = MDTextField(font_size = "12sp", helper_text = "Название стенда",  helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "530dp", pos_hint = {"center_x": 2.55, "center_y": 1.0})
        top_box = MDGridLayout(cols = 2, rows = 7, padding = ("10dp", "0dp", "0dp", "10dp"), spacing = ("30dp", "-10dp"), pos_hint = {"center_x": 0.3, "center_y": 0.43})
        
        for helper_text in _HELPERS_TEXT_STAND:
            top_box.add_widget(MDTextField(font_size = "12sp", helper_text = helper_text,  helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "250dp"))
        
        top_box.add_widget(MDFloatLayout(MDLabel(text = "Пятая приемка (5П):", theme_text_color = "Custom", text_color = (0.6, 0.6, 0.6, 1), pos_hint = {'center_x': 0.5, 'center_y': 0.9}),
                            MDSwitch(pos_hint = {'center_x': 0.9, 'center_y': 0.9}, thumb_color_active = _LITE_GRAY, track_color_active = (0.29, 0.46, 0.24, 0.5)), size_hint = (None, None),  size = ("250dp", "30dp")))
        if stand != None:
            self.defult_text(top_box, name_stand, stand)
            
        self.add_widget(name_stand)
        self.add_widget(top_box)

    def defult_text(self, instance, name_stand, stand):
        if stand[-1] == "Есть":
            instance.children[0].children[0].active = True
        else:
            instance.children[0].children[0].active = False
        
        name_stand.helper_text = name_stand.hint_text
        name_stand.hint_text = str(stand[1])
        for box, info in zip(instance.children[1:], stand[-2::-1]):
            box.text = str(info)


class CheckContent(MDFloatLayout):
    def __init__(self, stand=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.size = ("100dp", "280dp")
        self.on_start(stand)

    def on_start(self, stand):
        top_box = MDGridLayout(cols = 2, rows = 5, padding = ("10dp", "0dp", "0dp", "10dp"), spacing = ("30dp", "-10dp"), pos_hint = {"center_x": 0.3, "center_y": 0.43})
        name_stand = MDTextField(font_size = "12sp", helper_text = "Название стенда", helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "530dp", pos_hint = {"center_x": 2.55, "center_y": 1.0})
        
        for helper_text, text in _HELPERS_TEXT_CONT.items():
            top_box.add_widget(MDTextField(font_size = "12sp", text = text, helper_text = helper_text, helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "250dp"))

        top_box.add_widget(MDFloatLayout(MDLabel(text = "Негоден/Годен", theme_text_color = "Custom", text_color = (0.6, 0.6, 0.6, 1), pos_hint = {'center_x': 0.5, 'center_y': 0.9}),
                                         MDSwitch(pos_hint = {'center_x': 0.9, 'center_y': 0.9}, thumb_color_active = _LITE_GRAY, track_color_active = (0.29, 0.46, 0.24, 0.5)), size_hint = (None, None),  size = ("250dp", "30dp")))
        
        if stand != None:          
            self.defult_text(top_box, name_stand, stand)
            
        self.add_widget(name_stand)
        self.add_widget(top_box)
    
    def defult_text(self, instance, name_stand, stand):
        name_stand.text = str(stand[1])
        
        for i, info in zip(range(8, 4, -1), stand[2:-5]):
            if i == 5:
                instance.children[i].text = (datetime.today() + timedelta(days=365)).strftime("%d.%m.%Y")
            else:
                instance.children[i].text = str(info)


class Stands(MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        top_box = MDGridLayout(pos_hint = {"top": 1}, size_hint_y = None, height ="30dp", cols = 5, rows = 1, md_bg_color = _GRAY, padding = "4dp", spacing = "4dp")
        for head, width in _HEADS_TABLE_STAND.items():
            top_box.add_widget(MDLabel(markup = True, text = f"[color=#ffffff][size=12]{head}[/size][/color]", halign = "center", size_hint_x = None, width = width))
                            
        stands = MDList(spacing = "4dp")
        scroll_stands = RecycleView(scroll_wheel_distance = "40sp")
        scroll_stands.add_widget(stands)
        scroll_stands.scroll_y = 0

        scroll_box = MDBoxLayout(orientation = "vertical", size_hint_y = None, height = "320dp", pos_hint = {"center_x": 0.5, "center_y": 0.45})
        scroll_box.add_widget(scroll_stands)

        self.add_widget(top_box)
        self.add_widget(scroll_box)


class TooltipMDIconButton(MDIconButton, MDTooltip):
    _default_icon_pad = 9.0
    rounded_button = False
    _radius = 5.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._min_height = "24dp"
        self.theme_icon_color = "Custom"
        self.icon_color = _WHITE
        self.icon_size = "19dp"
        self.md_bg_color = _GREEN


class TooltipMDRaisedButton(MDRaisedButton, MDTooltip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_size = "14sp"
        self.theme_text_color = "Custom"
        self.text_color = _WHITE
        self._min_width = "28dp"
        self._min_height = "28dp"
        self.md_bg_color = _GREEN


class CancelContent(MDFloatLayout):
    def __init__(self, stand=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None, None)
        self.size = ("100dp", "180dp")
        self.on_start(stand)

    def on_start(self, stand):
        name_stand = MDTextField(font_size = "12sp", helper_text = "Название стенда",  helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "530dp", pos_hint = {"center_x": 2.55, "center_y": 1.0})
        top_box = MDGridLayout(cols = 2, rows = 5, padding = ("10dp", "0dp", "0dp", "10dp"), spacing = ("30dp", "-10dp"), pos_hint = {"center_x": 0.3, "center_y": 0.43})
        for helper_text in _HELPERS_TEXT_CANTHEL:
            top_box.add_widget(MDTextField(font_size = "12sp", helper_text = helper_text,  helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "250dp"))

        bottom = MDTextField(font_size = "12sp", helper_text = "Причина анулирования",  helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "530dp", pos_hint = {"center_x": 2.55, "center_y": 0.25})
        self.add_widget(name_stand)
        self.add_widget(top_box)
        self.add_widget(bottom)

        if stand != None:
            self.defult_text(top_box, name_stand, stand)

    def defult_text(self, instance, name_stand, stand):
        stand_1 = stand[1:6]
        name_stand.text = str(stand[1])
        for box, info in zip(instance.children[:4], stand_1[5:0:-1]):
            box.text = str(info)


class RepairContent(MDFloatLayout):
    def __init__(self, stand = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = ("100dp", "250dp")
        self.on_start(stand)
    
    def on_start(self, stand):
        top_box = MDGridLayout(cols = 2, rows = 5, padding = ("10dp", "5dp", "0dp", "10dp"), spacing = ("30dp", "0dp"), pos_hint = {"center_x": 0.3, "center_y": 0.65})
        for helper_text in _HELPER_TEXT_REPAIR:
            top_box.add_widget(MDTextField(font_size = "12sp", helper_text = helper_text,  helper_text_mode = "persistent", line_color_focus = _GREEN, helper_text_color_focus = _GREEN, text_color_focus = _GREEN, size_hint_x = None, width = "250dp"))

        if stand != None:
            self.defult_text(top_box, stand)

        self.add_widget(top_box)  

    def defult_text(self, instance, stand):
        stand_1 = stand[1:7]
        for box, info in zip(instance.children[2:], stand_1[::-1]):
            box.text = str(info)


if __name__ == "__main__":
    pass