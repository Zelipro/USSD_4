from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.list import TwoLineAvatarListItem,ImageLeftWidget,OneLineListItem,MDList
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton,MDFlatButton
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
import webbrowser
import re
import os
from kivymd.uix.dialog import MDDialog
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.uix.image import Image
from kivymd.uix.gridlayout import MDGridLayout

class ImageButton(MDCard, RectangularRippleBehavior):
    """Bouton personnalisé avec image et texte"""
    
    def __init__(self, image_source, text, callback=None, List=None, **kwargs):
        super().__init__(**kwargs)
        
        # Propriétés de la carte
        self.elevation = 2
        self.radius = [15]
        self.md_bg_color = (1, 1, 1, 1)  # Blanc
        self.size_hint_y = None
        self.height = dp(120)
        self.ripple_behavior = True
        
        # Layout principal
        main_layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(8),
            padding=[dp(10), dp(15), dp(10), dp(10)]
        )
        
        # Image avec gestion d'erreur
        try:
            img = Image(
                source=image_source if os.path.exists(image_source) else "Logo.png",
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                pos_hint={'center_x': 0.5}
            )
        except:
            img = Image(
                source="Logo.png",
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                pos_hint={'center_x': 0.5}
            )
        
        # Label
        label = MDLabel(
            text=text,
            theme_text_color="Primary",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(30),
            font_style="Caption"
        )
        
        main_layout.add_widget(img)
        main_layout.add_widget(label)
        self.add_widget(main_layout)
        
        # Callback
        if callback:
            if not List:
                self.bind(on_release=lambda x: callback(text))
            else:
                self.bind(on_release=lambda x: callback(text, *List))

class USSD(MDApp):
    isGrid = True
    
    def build(self):
        try:
            main = Builder.load_file("main.kv")
            return main
        except Exception as e:
            print(f"Erreur lors du chargement du fichier KV: {e}")
            return MDLabel(text=f"Erreur: {e}")
    
    def on_start(self):
        try:
            Clock.schedule_once(lambda dt: self.Next(), 1)
            self.Flags_charger()
        except Exception as e:
            print(f"Erreur lors du démarrage: {e}")
            self.show_info(title="Erreur", text=f"Erreur de démarrage: {e}")
    
    def Back(self):
        try:
            Pge = self.root.ids.cr.current
            self.root.ids.cr.current = f"{Pge[:-1]}{str(int(Pge[-1])-1)}"
        except Exception as e:
            print(f"Erreur Back: {e}")

    def Next(self):
        try:
            Pge = self.root.ids.cr.current
            self.root.ids.cr.current = f"{Pge[:-1]}{str(int(Pge[-1])+1)}"
        except Exception as e:
            print(f"Erreur Next: {e}")

    def Changer(self, instance):
        try:
            self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        except Exception as e:
            print(f"Erreur changement thème: {e}")
    
    def Back_with_instance(self, instance):
        self.Back()
    
    def return_Dic(self):
        """Retourne le dictionnaire des pays avec gestion d'erreur"""
        dic = {}
        try:
            # Vérifier si le fichier existe
            if not os.path.exists("Reseau.txt"):
                print("Fichier Reseau.txt introuvable")
                return {"Exemple": "Pays d'exemple"}
            
            with open("Reseau.txt", encoding='utf-8') as fil:
                Tous = fil.read()
            
            if not Tous.strip():
                return {"Exemple": "Pays d'exemple"}
                
            Tous = Tous.split("\n\n")
            for elmt in Tous:
                if not elmt.strip():
                    continue
                try:
                    elmt1 = elmt.split("\n")[0].split(":")
                    if len(elmt1) >= 2:
                        if elmt1[1] not in dic.keys():
                            dic[elmt1[1]] = elmt1[0]
                        else:
                            dic[elmt1[1]] = dic[elmt1[1]] + ";" + elmt1[0]
                except Exception as e:
                    print(f"Erreur parsing ligne: {e}")
                    continue
        except Exception as e:
            print(f"Erreur lecture fichier: {e}")
            return {"Erreur": "Impossible de charger les données"}
        
        return dic if dic else {"Exemple": "Pays d'exemple"}
    
    def Flags_charger_List(self):
        try:
            Pgee = self.root.ids.flags
            Pgee.clear_widgets()
            Pge = MDList()
            Pgee.add_widget(Pge)
            Liste = self.return_Dic()
            for i, elmt in enumerate(Liste.keys()):
                Two = TwoLineAvatarListItem(
                    text=elmt,
                    secondary_text=Liste.get(elmt),
                    on_release=self.appui_List,
                )
                # Vérifier si l'image existe
                img_path = f"Flags/{i+1}.jpg"
                if not os.path.exists(img_path):
                    img_path = "Logo.png"
                
                Img = ImageLeftWidget(source=img_path)
                Two.add_widget(Img)
                Pge.add_widget(Two)
        except Exception as e:
            print(f"Erreur Flags_charger_List: {e}")
            self.show_info(title="Erreur", text=f"Erreur chargement liste: {e}")

    def Changer_forme(self, instance):
        try:
            Icon = ""
            if self.isGrid:
                self.Flags_charger_List()
                Icon = "view-grid"
            else:
                self.Flags_charger()
                Icon = "view-list"
            self.root.ids.Pge_Flags.right_action_items = [
                [Icon, lambda x: self.Changer_forme(x)],
                ["weather-night-partly-cloudy", lambda x: self.Changer(x)]
            ]
            self.isGrid = not self.isGrid
        except Exception as e:
            print(f"Erreur changement forme: {e}")
        
    def Flags_charger(self):
        try:
            Pgee = self.root.ids.flags
            Pgee.clear_widgets()
            Pge = MDGridLayout(
                cols=2,
                adaptive_height=True,
                spacing=dp(10),
                padding=dp(15)
            )
            Pgee.add_widget(Pge)
            Pge.clear_widgets()
            Liste = self.return_Dic()
            for i, elmt in enumerate(Liste.keys()):
                # Vérifier si l'image existe
                img_path = f"Flags/{i+1}.jpg"
                if not os.path.exists(img_path):
                    img_path = "Logo.png"
                
                Two = ImageButton(img_path, elmt, self.appui)
                Pge.add_widget(Two)
        except Exception as e:
            print(f"Erreur Flags_charger: {e}")
            self.show_info(title="Erreur", text=f"Erreur chargement drapeaux: {e}")
    
    def appui(self, text):
        try:
            self.title = text
            self.root.ids.Page2_Top.title = self.title
            self.root.ids.cr.current = "Page2"
            
            if not os.path.exists("Reseau.txt"):
                self.show_info(title="Error", text="Fichier de données introuvable !")
                return
            
            with open("Reseau.txt", encoding='utf-8') as fil:
                Tous = fil.read()
            
            Tous = Tous.split("\n\n")
            Tous2 = [elmt for elmt in Tous if elmt.split("\n")[0].split(":")[1] == text]
            
            if not Tous2:
                self.show_info(title="Error", text="Non disponible pour le moment !")
            else:
                Pgee = self.root.ids.List2
                Pgee.clear_widgets()
                Pge = MDGridLayout(
                    cols=2,
                    adaptive_height=True,
                    spacing=dp(10),
                    padding=dp(15)
                )
                Pgee.add_widget(Pge)
                dic = {}
                for elmt in Tous2:
                    elmt = elmt.split("\n")
                    Title = elmt[0].split(":")[0]
                    dic[Title] = elmt[1:]
                    
                    # Vérifier si l'image existe
                    img_path = f"Reso/{Title}.png"
                    if not os.path.exists(img_path):
                        img_path = "Logo.png"
                    
                    One = ImageButton(
                        text=Title,
                        image_source=img_path,
                        callback=self.appui2,
                        List=[dic],
                    )
                    Pge.add_widget(One)
        except Exception as e:
            print(f"Erreur appui: {e}")
            self.show_info(title="Erreur", text=f"Erreur: {e}")
    
    def appui_List(self, instance):
        try:
            self.title = instance.text
            self.root.ids.Page2_Top.title = self.title
            self.root.ids.cr.current = "Page2"
            
            if not os.path.exists("Reseau.txt"):
                self.show_info(title="Error", text="Fichier de données introuvable !")
                return
            
            with open("Reseau.txt", encoding='utf-8') as fil:
                Tous = fil.read()
            
            Tous = Tous.split("\n\n")
            Tous2 = [elmt for elmt in Tous if elmt.split("\n")[0].split(":")[1] == instance.text]
            
            if not Tous2:
                self.show_info(title="Error", text="Non disponible pour le moment !")
            else:
                Pgee = self.root.ids.List2
                Pgee.clear_widgets()
                Pge = MDList()
                Pgee.add_widget(Pge)
                dic = {}
                for elmt in Tous2:
                    elmt = elmt.split("\n")
                    Title = elmt[0].split(":")[0]
                    dic[Title] = elmt[1:]
                    One = OneLineListItem(
                        text=Title,
                        on_release=lambda x, dic=dic: self.appui2_List(x, dic)
                    )
                    Pge.add_widget(One)
        except Exception as e:
            print(f"Erreur appui_List: {e}")
            self.show_info(title="Erreur", text=f"Erreur: {e}")
    
    def appui2_List(self, instance, dic):
        try:
            Things = dic.get(instance.text)
            self.title += "/" + instance.text
            self.root.ids.Page3_Top.title = self.title
            self.root.ids.cr.current = "Page3"
            self.root.ids.List3.clear_widgets()
            for elmt in Things:
                Box = self.copi_in(elmt.split(':')[1], elmt.split(':')[0])
                self.root.ids.List3.add_widget(Box)
        except Exception as e:
            print(f"Erreur appui2_List: {e}")
            self.show_info(title="Erreur", text=f"Erreur: {e}")

    def copi_in(self, text, motif):
        try:
            Box = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(60)
            )
            Entry = MDTextField(
                text=text,
                hint_text=motif,
                mode="rectangle",
                readonly=True,
                halign="center",
                icon_right="eye",
            )
            Box.add_widget(Entry)

            But = MDIconButton(
                icon="content-copy",
                on_release=lambda x, xx=Entry: self.Copie(x, xx),
            )
            Box.add_widget(But)

            But = MDIconButton(
                icon="phone",
                on_release=lambda x, xx=Entry, xxx=text: self.Contacter(x, xx, xxx),
            )
            Box.add_widget(But)

            return Box
        except Exception as e:
            print(f"Erreur copi_in: {e}")
            return MDLabel(text=f"Erreur: {e}")
    
    def Copie(self, instance, text):
        try:
            Clipboard.copy(text.text)
            text.icon_right = "check"
            Clock.schedule_once(lambda dt: self.Page2_entry_icon(text), 1)
        except Exception as e:
            print(f"Erreur copie: {e}")
    
    def Contacter(self, instance, text, numero_telephone):
        """Lance l'application de téléphone avec le numéro spécifié."""
        try:
            if not numero_telephone:
                self.show_info(title="Erreur", text="Numéro de téléphone manquant")
                return
            
            # Nettoyer le numéro
            numero_nettoye = re.sub(r'[^\d+\-\s\(\)*#]', '', str(numero_telephone).strip())
            
            if not numero_nettoye:
                self.show_info(title="Erreur", text="Numéro de téléphone invalide")
                return
            
            if platform == "android":
                try:
                    from jnius import autoclass
                    Intent = autoclass('android.content.Intent')
                    Uri = autoclass('android.net.Uri')
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    
                    intent = Intent(Intent.ACTION_DIAL)
                    intent.setData(Uri.parse(f"tel:{numero_nettoye}"))
                    
                    current_activity = PythonActivity.mActivity
                    current_activity.startActivity(intent)
                except Exception as e:
                    print(f"Erreur Android: {e}")
                    self.show_info(title="Erreur", text=f"Impossible d'ouvrir le téléphone: {e}")
                    
            elif platform == "ios":
                webbrowser.open(f"tel:{numero_nettoye}")
            else:
                self.show_info(
                    title="Non supporté",
                    text=f"Appel non supporté sur cette plateforme.\nNuméro: {numero_nettoye}"
                )
                
        except Exception as e:
            print(f"Erreur Contacter: {e}")
            self.show_info(title="Erreur", text=f"Erreur lors de l'appel: {e}")

    def Page2_entry_icon(self, entry):
        try:
            entry.icon_right = "eye"
        except:
            pass
    
    def show_info(self, title, text, fonct=None):
        try:
            self.MD = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="[b]Ok[/b]",
                        on_release=lambda x: self.Close(x, fonct),
                    )
                ]
            )
            self.MD.open()
        except Exception as e:
            print(f"Erreur dialog: {e}")
    
    def Close(self, instance, fonct):
        try:
            self.MD.dismiss()
            if fonct:
                fonct()
        except Exception as e:
            print(f"Erreur Close: {e}")
    
    def appui2(self, text, dic):
        try:
            Things = dic.get(text)
            self.title += "/" + text
            self.root.ids.Page3_Top.title = self.title
            self.Next()
            self.root.ids.List3.clear_widgets()
            for elmt in Things:
                Box = self.copi_in(elmt.split(':')[1], elmt.split(':')[0])
                self.root.ids.List3.add_widget(Box)
        except Exception as e:
            print(f"Erreur appui2: {e}")
            self.show_info(title="Erreur", text=f"Erreur: {e}")
    
    def appui3(self, instance):
        try:
            dic = {
                "Changer de font": self.change_font,
                "A propos de nous": self.infos,
                "Quitter": self.stopp
            }
            func = dic.get(instance.text[3:-4])
            if func:
                func(instance)
        except Exception as e:
            print(f"Erreur appui3: {e}")
    
    def infos(self, instance):
        try:
            Info = "[b][color=000000]Objectif :[/color][/b] Centraliser tous les codes USSD d'Afrique dans une application simple et accessible. Un clic, et c'est parti !\n[b][color=000000]Public :[/color][/b] Tous les Africains équipés d'un smartphone (et bientôt le monde entier) !\n[b][color=000000]Auteur :[/color][/b] [color=ff0000]Elisée ATIKPO[/color], passionné par la création d'applications cross-platform.\n[b][color=000000]Version :[/color][/b] 1.3\n[b][color=000000]Contact :[/color][/b] [color=00ff00]eliseeatikpo10@gmail.com[/color] – Vos suggestions sont les bienvenues !"
            self.show_info(title="Information", text=Info)
        except Exception as e:
            print(f"Erreur infos: {e}")

    def stopp(self, instance):
        try:
            self.show_info(title="Quitter", text="Vous êtes sur le point de quitter ! Bye !", fonct=self.stop)
        except Exception as e:
            print(f"Erreur stopp: {e}")
    
    def change_font(self, instance):
        try:
            List = []
            col = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 
                   'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 
                   'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
            for elmt in col:
                things = {
                    "text": elmt,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=elmt: self.appui4(x)
                }
                List.append(things)
            self.MD2 = MDDropdownMenu(
                caller=instance,
                items=List,
            )
            self.MD2.open()
        except Exception as e:
            print(f"Erreur change_font: {e}")
    
    def appui4(self, text):
        try:
            self.theme_cls.primary_palette = text
            self.MD2.dismiss()
        except Exception as e:
            print(f"Erreur appui4: {e}")

if __name__ == '__main__':
    USSD().run()
