from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '950')
Config.set('graphics', 'height', '590')

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.screen import MDScreen

from datetime import datetime
from time import time

from view.content import DialogContent, CheckContent, Stands, TooltipMDIconButton, TooltipMDRaisedButton, CancelContent, RepairContent
from config.settings import _LITE_GRAY, _GREEN, _WHITE, _HARD_GRAY
from controller.data_base import DataBase
_db = DataBase()


class Menu(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_box = MDFloatLayout()
        menu_box.add_widget(MDRectangleFlatButton(text="Файл", pos_hint = {"center_x": 0.05, "center_y": 0.51} , theme_text_color = "Custom", font_style = "Overline", line_color = (0, 0, 0, 0), text_color = _WHITE, _min_height = "24dp", on_release = lambda x: self.file()))
        menu_box.add_widget(MDRectangleFlatButton(text="Настройки", pos_hint = {"center_x": 0.16, "center_y": 0.51}, theme_text_color = "Custom", font_style = "Overline", line_color = (0, 0, 0, 0), text_color = _WHITE, _min_height = "24dp", on_release = lambda x: self.settings()))
        menu_box.add_widget(MDRectangleFlatButton(text="О программе", pos_hint = {"center_x": 0.29, "center_y": 0.51}, theme_text_color = "Custom", font_style = "Overline", line_color = (0, 0, 0, 0), text_color = _WHITE, _min_height = "24dp", on_release = lambda x: self.about()))
        menu_box.add_widget(MDTextField(font_size = "12sp", height = "30dp", mode = "round", icon_right = "magnify", on_text_validate = lambda x: app.enter_find(), 
                                                                                                                    fill_color_focus = _LITE_GRAY,
                                                                                                                    fill_color_normal = _LITE_GRAY,
                                                                                                                    line_color_normal = _LITE_GRAY,
                                                                                                                    line_color_focus = _GREEN,
                                                                                                                    icon_right_color_focus = "white",
                                                                                                                    icon_right_color_normal = (0.3, 0.3, 0.3, 1),
                                                                                                                    foreground_color = _LITE_GRAY,
                                                                                                                    text_color_normal = (0, 0, 0, 0.5),
                                                                                                                    text_color_focus = "white",
                                                                                                                    size_hint_x = None, width = "200dp", pos_hint = {"center_x": 0.61,"center_y": 0.51}))
        scroll_stands = TooltipMDIconButton(tooltip_text = "Перемотать список", icon="chevron-up", pos_hint = {"center_x": 0.85, "center_y": 0.51}, on_release = lambda x: app.scroll_stands())  
        scroll_stands._default_icon_pad = 9.0
        scroll_stands.rounded_button = False
        scroll_stands._radius = 5.0
        menu_box.add_widget(scroll_stands)

        army = TooltipMDRaisedButton(tooltip_text = "Пятая приемка", text="5П", pos_hint = {"center_x": 0.814, "center_y": 0.51}, on_release = lambda x: app.search_army_stand())  
        army.padding = "5dp"
        army.elevation = 1

        print_stands = TooltipMDIconButton(tooltip_text = "Печать стендов", icon="printer", pos_hint = {"center_x": 0.778, "center_y": 0.51}, on_release = lambda x: app.print_stands())  
        menu_box.add_widget(print_stands)

        sort_stands = TooltipMDIconButton(tooltip_text = "Сортировка по номеру", icon="sort-numeric-descending", pos_hint = {"center_x": 0.742, "center_y": 0.51}, on_release = lambda x: app.sort_stands())  
        menu_box.add_widget(sort_stands)
        menu_box.add_widget(army)

        menu_box.add_widget(MDRectangleFlatButton(text="Добавить стенд", pos_hint = {"right": 1, "center_y": 0.51} , theme_text_color = "Custom", font_style = "Overline",md_bg_color = _GREEN, line_color = (0, 0, 0, 0), text_color = _WHITE, _min_height = "24dp", on_release = lambda x: self.dialog_stand()))

        top_box = MDBoxLayout(orientation = "vertical")
        top_box.add_widget(menu_box)
        self.add_widget(top_box)

    def dialog_stand(self):
        content_cls = DialogContent()
        dialog_set_stand = MDDialog(title = "Карта стенда", type = "custom", content_cls = content_cls, buttons=[MDRectangleFlatButton(text="Добавить", theme_text_color="Custom", text_color="white", md_bg_color = _GREEN, line_color = (0, 0, 0, 0), on_release = lambda x: self.set_stand(dialog_set_stand, content_cls))])
        dialog_set_stand.open()

    def set_stand(self, dialog_set_stand, content_cls):
        if all_id := _db.cursor.execute("SELECT stand_id FROM Stands").fetchall() or None:
            stand_id = int(all_id[-1][0]) + 1
        else:
            stand_id = 1

        name_stand = content_cls.children[1].text
        stand = [content_cls.children[0].children[i].text if content_cls.children[0].children[i].text not in ("", " ") else None for i in range(13, 0, -1)]
        army = "Нет"
        if content_cls.children[0].children[0].children[0].active:
            army = "Есть"

        stand.insert(0, name_stand)
        stand.append(army)

        filter_stands = _db.cursor.execute(f"SELECT * FROM Stands WHERE number_stand = '{stand[2]}' AND invent_number = '{stand[3]}' AND factory_number = '{stand[4]}'").fetchall()
        if filter_stands == []:
            stand.insert(0, stand_id)
            
            if None not in stand:
                _db.cursor.executemany(f"INSERT INTO Stands VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [stand])
                _db.connect.commit()

                dialog_set_stand.dismiss(force = True)
                app.update_stand(stand=stand)
        else:
            self.snackbar_error()
    
    def snackbar_error(self):
        Snackbar(text = "Стенд уже внесен в реестр.", font_size = "18sp", pos_hint = {"center_x": 0.5}, md_bg_color = _HARD_GRAY).open()

    def file(self):
        print("Зашли в меню файла")

    def settings(self):
        print("Зашли в меню настройки")

    def about(self):
        print("Зашли в меню о приложение")


class Info(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_box = MDBoxLayout(orientation = "horizontal", padding = ("0dp", "1dp", "0dp", "0dp"), spacing = "2dp")
        box_info = MDBoxLayout(TwoLineListItem(text = "[color=#ffffff]Название стенда[/color]", secondary_text = "[size=12][color=#ffffff]Номер стенда[/color][/size]"),
                                MDGridLayout(
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Инвентарный №:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Заводской №:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Место хранения:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Ответственный:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Назначение:[/color][/size]", halign = "left", size_hint_x = None, width = "290dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Группа:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Разработчик:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Заказчик:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Версия стенда:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Наличие ПО:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Версия ПО:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Дата запуска в эксплуатацию:[/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Пятая приемка (5П):[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Дата проверки:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Дата следующей проверки:[/color][/size]", halign = "left", size_hint_x = None, width = "290dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Кол-во ремонтов:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Дата последнего ремонта:[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Извещение на доработку (№):[/color][/size]", halign = "left", size_hint_x = None, width = "220dp"),
                                cols = 2, rows = 9, padding = "4dp", spacing = ("40dp", "4dp")),
                                orientation = "vertical", md_bg_color = _LITE_GRAY, size_hint_x = None, width = "570dp")

        box_button = MDFloatLayout(MDRectangleFlatButton(text="КД", theme_text_color = "Custom", font_style = "Overline", text_color = _WHITE, _min_width = "105dp", _min_height = "22dp", line_color = (0, 0, 0, 0), md_bg_color = _GREEN, pos_hint = {"center_x": 0.5, "center_y":0.915}),
                                    MDRectangleFlatButton(text="Изменить", theme_text_color = "Custom", font_style = "Overline", text_color = _WHITE, _min_width = "105dp", _min_height = "22dp", line_color = (0, 0, 0, 0), md_bg_color = _GREEN, pos_hint = {"center_x": 0.5, "center_y":0.75}, on_release = lambda x: app.to_change()),
                                    MDRectangleFlatButton(text="Проверка", theme_text_color = "Custom", font_style = "Overline", text_color = _WHITE, _min_width = "105dp", _min_height = "22dp", line_color = (0, 0, 0, 0), md_bg_color = _GREEN, pos_hint = {"center_x": 0.5, "center_y":0.585}, on_release = lambda x: app.check_stand()),
                                    MDRectangleFlatButton(text="Ремонт", theme_text_color = "Custom", font_style = "Overline", text_color = _WHITE, _min_width = "105dp", _min_height = "22dp", line_color = (0, 0, 0, 0), md_bg_color = _GREEN,pos_hint = {"center_x": 0.5, "center_y":0.420}, on_release = lambda x: app.repair_stand()),
                                    MDRectangleFlatButton(text="Заменить", theme_text_color = "Custom", font_style = "Overline", text_color = _WHITE, _min_width = "105dp", _min_height = "22dp", line_color = (0, 0, 0, 0), md_bg_color = _GREEN,pos_hint = {"center_x": 0.5, "center_y":0.255}),
                                    MDRectangleFlatButton(text="Анулировать", theme_text_color = "Custom", font_style = "Overline", text_color = _WHITE, _min_width = "105dp", _min_height = "22dp", line_color = (0, 0, 0, 0), md_bg_color = _GREEN,pos_hint = {"center_x": 0.5, "center_y":0.09}, on_release = lambda x: app.cancel_stand()),
                                    md_bg_color = _LITE_GRAY, size_hint_x = None, width = "110dp")

        statistics = app.get_statistics()
        box_statistic = MDBoxLayout(MDGridLayout(
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Кол-во стендов: [b]{statistics[0]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Кол-во стендов (5П): [b]{statistics[1]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Кол-во ремонтов: [b]{statistics[2]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Частый ремонт: [b]{statistics[3]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Редкий ремонт: [b]{statistics[4]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Последний ремонт: [b]{statistics[5]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Участок частого ремонта: [b]{statistics[6]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            MDLabel(markup = True, text = f"[size=12][color=#ffffff]Участок редкого ремонта: [b]{statistics[7]}[/b][/color][/size]", halign = "left", size_hint_x = None, width = "260dp"),
                                            cols = 1, rows = 8, padding = "4dp", spacing = ("40dp", "4dp")),
                                orientation = "vertical", md_bg_color = _LITE_GRAY)
        all_box.add_widget(box_info)
        all_box.add_widget(box_button)
        all_box.add_widget(box_statistic)
        self.add_widget(all_box)


class Main(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stand_id = None
        self.press_army = True
        self.sort_stand = True

    def build(self):
        screen = MDScreen(name = "main_sceern")
        box_main = MDBoxLayout(orientation = "vertical")
        
        self.box_menu = Menu(orientation = "horizontal", pos_hint = {"top": 1}, size_hint_y = None, height = "32dp", md_bg_color = _LITE_GRAY)
        self.box_stands = Stands(pos_hint = {"center_x": 0.5, "center_y": 0.5}, md_bg_color = _HARD_GRAY)
        self.box_info = Info(orientation = "horizontal", pos_hint = {"down": 1}, size_hint_y = None, height = "210dp", md_bg_color = (0.5, 0.5, 0.5, 1))
        
        box_main.add_widget(self.box_menu)
        box_main.add_widget(self.box_stands)
        box_main.add_widget(self.box_info)
        screen.add_widget(box_main)

        stands = _db.cursor.execute(f"SELECT * FROM Stands ORDER BY name_stand DESC").fetchall()
        start = time()
        for i, stand in zip(range(1, len(stands) + 1), stands):
            self.update_stand(i, stand=stand)
        print(start - time())
        return screen
    
    def update_stand(self, id=None, stand=None, other=None):
        if other == None:
            stand_id, name_stand, number_stand, invent_number, factory_number, *_ = stand

            card_stand = MDCard(MDGridLayout(
                                            MDLabel(markup = True, text = f"[color=#ffffff][size=12]{id}[/size][/color]", halign = "center", size_hint_x = None, width = "30dp"),
                                            MDLabel(markup = True, text = f"[color=#ffffff][size=12]{number_stand}[/size][/color]", halign = "center", size_hint_x = None, width = "130dp"),
                                            MDLabel(markup = True, text = f"[color=#ffffff][size=12]{invent_number}[/size][/color]", halign = "center", size_hint_x = None, width = "130dp"),
                                            MDLabel(markup = True, text = f"[color=#ffffff][size=12]{factory_number}[/size][/color]", halign = "center", size_hint_x = None, width = "130dp"),
                                            MDLabel(markup = True, text = f"[color=#ffffff][size=12]{name_stand}[/size][/color]", halign = "center"),
                                            pos_hint = {"top": 1}, size_hint_y = None, height = "30dp", cols = 5, rows = 1, padding = "4dp", spacing = "4dp"),
                                on_release = lambda x: self.press_stand(stand_id, card_stand), md_bg_color = _GREEN, elevation = 2, size_hint_y = None, height = "30dp",focus_color = (0.7, 0.6, 0.3, 1), unfocus_color = _GREEN, ripple_behavior = True, focus_behavior = True)

            self.box_stands.children[0].children[0].children[0].add_widget(card_stand)
        else:
            stand_id, name_stand, number_stand, invent_number, factory_number, *_ = stand
            for info, st in zip(other.children[0].children, [name_stand, factory_number, invent_number, number_stand]):
                info.text = f"[color=#ffffff][size=12]{st}[/size][/color]"
        
    def press_stand(self, stand_id, stand):
        self.stand_id = stand_id
        self.stand = stand
        stand_id, name_stand, number_stand, *stand_info = _db.cursor.execute(f"SELECT * FROM Stands WHERE stand_id = '{stand_id}'").fetchone()
        data_check = _db.cursor.execute(f"SELECT data_check, data_next_check FROM CheckStands WHERE stand_id = '{stand_id}'").fetchall()

        if data_check != []:
            data_check = data_check[0]
        else:
            data_check = ["-", "-"]

        self.box_info.children[0].children[2].children[1].text = f"[b][color=#ffffff]{name_stand}[/color][/b]"
        self.box_info.children[0].children[2].children[1].secondary_text = f"[b][color=#ffffff][size=14]{number_stand}[/size][/color][/b]"
        headr_table = ("Инвентарный №", "Заводской №", "Место хранения", "Ответственный", "Назначение", "Группа", "Разработчик", "Заказчик", "Версия стенда", "Наличие ПО", "Версия ПО",
                        "Дата запуска в эксплуатацию",  "Пятая приемка (5П)", "Дата проверки", "Дата следующей проверки", "Кол-во ремонтов", "Дата последнего ремонта", "Извещение на доработку (№)")

        for header, info, i in zip(headr_table[:13], stand_info, range(17, -1, -1)):
            self.box_info.children[0].children[2].children[0].children[i].text = f"[size=12][color=#ffffff]{header}:[/color][/b] [b][size=12][color=#ffffff]{info}[/color][/size][/b]"

        for header, info, i in zip(headr_table[13:15], data_check, range(4, -1, -1)):
            self.box_info.children[0].children[2].children[0].children[i].text = f"[size=12][color=#ffffff]{header}:[/color][/b] [b][size=12][color=#ffffff]{info}[/color][/size][/b]"

    def to_change(self):
        if self.stand_id:
            stand = _db.cursor.execute(f"SELECT * FROM Stands WHERE stand_id = '{self.stand_id}'").fetchone()
            content_cls = DialogContent(stand)
            dialog_set_stand = MDDialog(title = "Карта стенда", type = "custom", content_cls = content_cls, buttons=[MDRectangleFlatButton(text="Изменить", theme_text_color="Custom", text_color="white", md_bg_color = _GREEN, line_color = (0, 0, 0, 0), on_release = lambda x: self.set_stand(self.stand_id, dialog_set_stand, content_cls))])
            dialog_set_stand.open()
        else:
            Snackbar(text = "Выберите стенд.", font_size = "18sp", pos_hint = {"center_x": 0.5}, md_bg_color = _HARD_GRAY).open()

    def repair_stand(self):
        if self.stand_id:
            stand = _db.cursor.execute(f"SELECT * FROM Stands WHERE stand_id = '{self.stand_id}'").fetchone()
            content_cls = RepairContent(stand)
            dialog_set_stand = MDDialog(title = "Заявка на ремонт", type = "custom", content_cls = content_cls, buttons=[MDRectangleFlatButton(text="Принять", theme_text_color="Custom", text_color="white", md_bg_color = _GREEN, line_color = (0, 0, 0, 0), on_release = lambda x: self.set_repair_stand(self.stand_id, dialog_set_stand, content_cls))])
            dialog_set_stand.open()
        else:
            Snackbar(text = "Выберите стенд.", font_size = "18sp", pos_hint = {"center_x": 0.5}, md_bg_color = _HARD_GRAY).open()

    def set_repair_stand(self, stand_id, dialog_set_stand, content_cls):
        stand = [content_cls.children[0].children[i].text if content_cls.children[0].children[i].text not in ("", " ") else content_cls.children[0].children[i].hint_text for i in range(7, -1, -1)]
        stand.insert(0, stand_id)

        if all_id :=  _db.cursor.execute("SELECT repair_stand_id FROM RepairStands").fetchall() or None:
            repair_stand_id = int(all_id[-1][0]) + 1
        else:
            repair_stand_id = 1
        stand.insert(0, repair_stand_id)

        if None not in stand:
            _db.cursor.executemany(f"INSERT INTO RepairStands VALUES (?,?,?,?,?,?,?,?,?,?)", [stand])
            _db.connect.commit()

            dialog_set_stand.dismiss(force = True)
            app.update_stand(stand)

            self.snackbar_complet()

        statistics = app.get_statistics()
        app.update_info(statistics)

    def set_stand(self, stand_id, dialog_set_stand, content_cls):
        name_stand = content_cls.children[1].text
        if name_stand in ("", " "):
            name_stand = content_cls.children[1].hint_text

        stand = [content_cls.children[0].children[i].text if content_cls.children[0].children[i].text not in ("", " ") else content_cls.children[0].children[i].hint_text for i in range(13, 0, -1)]
        
        army = "Нет"
        if content_cls.children[0].children[0].children[0].active:
            army = "Есть"

        stand.insert(0, name_stand)
        stand.append(army)
        stand.insert(0, stand_id)

        if None not in stand:
            _db.cursor.executemany(f"UPDATE Stands SET stand_id = ?, name_stand = ?, number_stand = ?, invent_number = ?, factory_number = ?, storage_place = ?, responsible = ?, target = ?, team = ?, name_create = ?, name_client = ?, version_stand = ?, software = ?, version_software = ?, date_of_creation = ?, army = ? WHERE stand_id = '{stand_id}'", [stand])
            _db.connect.commit()

            dialog_set_stand.dismiss(force = True)
            app.update_stand(stand=stand, other=self.stand)
            app.press_stand(self.stand_id, stand)
            self.snackbar_complet()
    
    def snackbar_complet(self, text="Данные обновлены."):
        Snackbar(text = text, font_size = "18sp", pos_hint = {"center_x": 0.5}, md_bg_color = _HARD_GRAY).open()

    def set_item(self, text_item):
        self.screen.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def get_statistics(self):
        dict_repair_stands = dict()
        _max, _min = 0, 1
        max_repair_stand, min_repair_stand = None, None
        max_place_repair_stand, min_place_repair_stand = None, None

        stands = _db.cursor.execute(f"SELECT * FROM Stands").fetchall()
        repair_stands = _db.cursor.execute(f"SELECT * FROM RepairStands").fetchall()
        army_stands = _db.cursor.execute(f"SELECT * FROM Stands WHERE army = 'Есть'").fetchall()

        quantity_stand = 0
        quantity_repair_stand = 0
        quantity_army_stand = 0
        last_repair_stand = None

        if stands:
            quantity_stand = len(stands)

        if army_stands:
            quantity_army_stand = len(army_stands)

        if repair_stands:
            quantity_repair_stand = len(repair_stands)
            last_repair_stand = repair_stands[-1][3]

            for stand in repair_stands:
                if stand[1] not in dict_repair_stands:
                    dict_repair_stands[stand[1]] = 1
                else:
                    dict_repair_stands[stand[1]] = dict_repair_stands.get(stand[1]) + 1

            for key, val in dict_repair_stands.items():
                stand = [stand for stand in repair_stands if stand[1] == key]

                if stand != []:
                    stand = stand[0]
                    if val >= _max:
                        _max = val
                        max_repair_stand = f"{stand[3]} ({_max} раз-(а))"
                        max_place_repair_stand = stand[6]
                    
                    if val <= _min:
                        _min = val
                        min_repair_stand = f"{stand[3]} ({_min} раз-(а))"
                        min_place_repair_stand = stand[6]
        return quantity_stand, quantity_army_stand, quantity_repair_stand, max_repair_stand, min_repair_stand, last_repair_stand, max_place_repair_stand, min_place_repair_stand

    def update_info(self, data_info):
        headers = ["Кол-во стендов", "Кол-во стендов (5П)", "Кол-во ремонтов", "Частый ремонт", "Редкий ремонт","Последний ремонт", "Участок частого ремонта", "Участок редкого ремонта"]
        for info, i, header in zip(data_info, range(len(data_info) - 1, 0, -1), headers):
            self.box_info.children[0].children[0].children[0].children[i].text = f"[size=12][color=#ffffff]{header}: [b]{info}[/b][/color][/size]"
    
    def enter_find(self):
        text_find = self.box_menu.children[0].children[0].children[5].text
        if text_find == "":
            stands = _db.cursor.execute(f"SELECT * FROM Stands").fetchall()
        else:
            stands = _db.cursor.execute(f"SELECT * FROM Stands WHERE number_stand = '{text_find}' OR name_stand = '{text_find}' OR invent_number = '{text_find}'").fetchall()

        self.box_stands.children[0].children[0].children[0].clear_widgets()

        for i, stand in zip(range(1, len(stands) + 1), stands):
            self.update_stand(i, stand)
        self.box_menu.children[0].children[0].children[3].icon = "chevron-down"
        self.box_stands.children[0].children[0].scroll_y = 1

    def scroll_stands(self):
        scroll_status = self.box_stands.children[0].children[0].scroll_y
        if scroll_status == 0:
            self.box_stands.children[0].children[0].scroll_y = 1
            self.box_menu.children[0].children[0].children[4].icon = "chevron-down"
        else:
            self.box_stands.children[0].children[0].scroll_y = 0
            self.box_menu.children[0].children[0].children[4].icon = "chevron-up"

    def sort_stands(self):
        if self.sort_stand:
            stands = _db.cursor.execute(f"SELECT * FROM Stands ORDER BY number_stand DESC").fetchall()
            self.sort_stand = False
            self.box_menu.children[0].children[0].children[2].icon = "sort-alphabetical-descending"
            self.box_menu.children[0].children[0].children[2].tooltip_text = "Сортировка по названию"
        else:
            stands = _db.cursor.execute(f"SELECT * FROM Stands ORDER BY name_stand DESC").fetchall()
            self.sort_stand = True
            self.box_menu.children[0].children[0].children[2].icon = "sort-numeric-descending"
            self.box_menu.children[0].children[0].children[2].tooltip_text = "Сортировка по номеру"

        self.box_stands.children[0].children[0].children[0].clear_widgets()
        for i, stand in zip(range(1, len(stands) + 1), stands):
            self.update_stand(i, stand)

    def search_army_stand(self):
        if self.press_army:
            stands = _db.cursor.execute(f"SELECT * FROM Stands WHERE army = 'Есть'").fetchall()
            self.press_army = False
        else:
            stands = _db.cursor.execute(f"SELECT * FROM Stands").fetchall()
            self.press_army = True
        
        self.box_stands.children[0].children[0].children[0].clear_widgets()
        for i, stand in zip(range(1, len(stands) + 1), stands):
            self.update_stand(i, stand=stand)
            
        self.box_menu.children[0].children[0].children[4].icon = "chevron-down"
        self.box_stands.children[0].children[0].scroll_y = 1

    def set_check_stand(self, stand_id, dialog_set_stand, content_cls):
        name_stand = content_cls.children[1].text
        stand = [content_cls.children[0].children[i].text if content_cls.children[0].children[i].text not in ("", " ") else None for i in range(9, 0, -1)]
        stand.append(content_cls.children[0].children[0].children[0].active)
        stand.append(datetime.today().strftime("%d.%m.%Y"))
        stand.insert(0, name_stand)
        stand.insert(0, stand_id)
        
        if all_id :=  _db.cursor.execute("SELECT check_stand_id FROM CheckStands").fetchall() or None:
            check_stand_id = int(all_id[-1][0]) + 1
        else:
            check_stand_id = 1
        stand.insert(0, check_stand_id)

        if None not in stand:
            _db.cursor.executemany(f"INSERT INTO CheckStands VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [stand])
            _db.connect.commit()

            dialog_set_stand.dismiss(force = True)
            self.snackbar_complet()

        statistics = app.get_statistics()
        app.update_info(statistics)

    def check_stand(self):
        if self.stand_id:
            stand = _db.cursor.execute(f"SELECT * FROM Stands WHERE stand_id = '{self.stand_id}'").fetchone()
            content_cls = CheckContent(stand)
            dialog_set_stand = MDDialog(title = "Протокол проверки", type = "custom", content_cls = content_cls, buttons=[MDRectangleFlatButton(text="Принять", theme_text_color="Custom", text_color="white", md_bg_color = _GREEN, line_color = (0, 0, 0, 0), on_release = lambda x: self.set_check_stand(self.stand_id, dialog_set_stand, content_cls))])
            dialog_set_stand.open()
        else:
            Snackbar(text = "Выберите стенд.", font_size = "18sp", pos_hint = {"center_x": 0.5}, md_bg_color = _HARD_GRAY).open()

    def print_stands(self):
        with open("stands.txt", "w", encoding="UTF-8") as file:
            stands = self.box_stands.children[0].children[0].children[0].children
            for i, stand in zip(range(1, len(stands)), stands):
                result = f"{stand.children[0].children[0].text} {stand.children[0].children[3].text} {stand.children[0].children[2].text} {stand.children[0].children[1].text}\n".replace("[color=#ffffff][size=12]", "")
                result = result.replace("[/size][/color]", "")
                file.write(f"{i} {result}")
        app.snackbar_complet(text = "Файл stand.doc сгенерирован.")

    def cancel_stand(self):
        if self.stand_id:
            stand = _db.cursor.execute(f"SELECT * FROM Stands WHERE stand_id = '{self.stand_id}'").fetchone()
            content_cls = CancelContent(stand)
            dialog_set_stand = MDDialog(title = "Анулировать стенд?", type = "custom", content_cls = content_cls, buttons=[MDRectangleFlatButton(text="Анулировать", theme_text_color="Custom", text_color="white", md_bg_color = _GREEN, line_color = (0, 0, 0, 0), on_release = lambda x: self.cancel(self.stand_id, dialog_set_stand, content_cls))])
            dialog_set_stand.open()
        else:
            Snackbar(text = "Выберите стенд.", font_size = "18sp", pos_hint = {"center_x": 0.5}, md_bg_color = _HARD_GRAY).open()

    def cancel(self, stand_id, dialog_set_stand, content_cls):
        stand = [content_cls.children[1].children[i].text if content_cls.children[1].children[i].text not in ("", " ") else content_cls.children[1].children[i].hint_text for i in range(3, -1, -1)]
        if all_id :=  _db.cursor.execute("SELECT cancel_id FROM CancelStands").fetchall() or None:
            cancel_id = int(all_id[-1][0]) + 1
        else:
            cancel_id = 1
        
        name_stand = content_cls.children[2].text
        if name_stand in ("", " "):
            name_stand = content_cls.children[2].hint_text

        stand.insert(0, name_stand)
        stand.insert(0, cancel_id)
        bottom = content_cls.children[0].text
        stand.append(bottom)

        _db.cursor.executemany(f"INSERT INTO CancelStands VALUES (?,?,?,?,?,?,?)", [stand])
        _db.cursor.execute(f"DELETE FROM Stands WHERE stand_id = '{stand_id}'").fetchone()
        _db.cursor.execute(f"DELETE FROM RepairStands WHERE stand_id = '{stand_id}'").fetchone()
        _db.cursor.execute(f"DELETE FROM CheckStands WHERE stand_id = '{stand_id}'").fetchone()
        _db.connect.commit()

        self.box_stands.children[0].children[0].children[0].remove_widget(self.stand)
        dialog_set_stand.dismiss(force = True)
        Snackbar(text = "Стенд анулирован.", font_size = "18sp", pos_hint = {"center_x": 0.5}, md_bg_color = _HARD_GRAY).open()


if __name__ == "__main__":
    app = Main()
    app.run()