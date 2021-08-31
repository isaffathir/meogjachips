from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, NoTransition, SlideTransition, FadeTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import json

#Window.size = (310, 580)



class Qtime(MDApp):
    def build(self):
        Window.bind(on_keyboard=self.on_key)
        Clock.schedule_once(self.check_logged)
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("assets/kv/main.kv"))
        sm.add_widget(Builder.load_file("assets/kv/login.kv"))
        sm.add_widget(Builder.load_file("assets/kv/signup.kv"))
        sm.add_widget(Builder.load_file("assets/kv/home.kv"))
        return sm

    def on_key(self, window, key, *args):
        if key == 27:
            if self.root.current_screen.name == "main":
                return True
            elif self.root.current_screen.name == "login":
                self.root.transition = SlideTransition(direction="right")
                self.root.current = "main"
                return True
            elif self.root.current_screen.name == "signup":
                self.root.transition = SlideTransition(direction = "right")
                self.root.current = "main"
                return True
            elif self.root.current_screen.name == "home":
                self.root.current = "home"
                return True

    def get_data(self):
        f = open("data.json", "rb")
        f_data = f.read().decode()
        data = json.loads(f_data)
        f.close()
        return data

    def get_akun(self):
        x = open("akun.json", "rb")
        x_akun = x.read().decode()
        akun = json.loads(x_akun)
        x.close()
        return akun

    def set_data(self, key, value):
        data = self.get_data()
        data[key] = value
        f = open("data.json", "wb")
        f.write(json.dumps(data).encode())

    def set_akun(self, key, value):
        akun = self.get_akun()
        akun[key] = value
        x = open("data.json", "wb")
        x.write(json.dumps(akun).encode())

    def check_logged(self, *args):
        data = self.get_data()
        if data['logged'] == "True":
            self.root.transition = NoTransition()
            self.root.current = "home"
        else:
            self.root.transition = SlideTransition()

    def doLogin(self, tem, pw, reslog):
        akun = self.get_akun()
        if akun['email'] == tem and akun['pw'] == pw:
            self.root.current = "home"
            self.set_data("logged", "True")
        else:
            print("Gagal")
            reslog.text = "AKUN TIDAK TERDAFTAR"

    def doLogout(self):
        self.root.transition = FadeTransition()
        self.root.current = "main"
        self.set_data("logged", "False")
        self.check_logged()


if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="assets/font/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="assets/font/Poppins-SemiBold.ttf")

    Qtime().run()
